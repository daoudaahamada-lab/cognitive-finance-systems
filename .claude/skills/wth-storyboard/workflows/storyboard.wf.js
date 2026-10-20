export const meta = {
  name: 'wth-storyboard',
  description: 'Storyboard Story d’une vidéo WealthTech Horizon (méthode A) : préparation, 3 brouillons, 3 juges, synthèse, test du spectateur muet, révision, contrôle --check',
  whenToUse: 'Écrire scripts/storyboards/Vxx.json et Vxx.md quand la voix de Vxx est finale. args: {id: "V05", root: "<abs>/wth-videos", notes?, overwrite?, excerpt?, muteRounds?}',
  phases: [
    { title: 'Prep', detail: 'phrases minutées, segments, PNG utilisables, public, chiffres' },
    { title: 'Draft', detail: '3 storyboards complets sous 3 angles' },
    { title: 'Judge', detail: '3 juges, une lentille chacun' },
    { title: 'Synthesize', detail: 'gagnant + meilleures idées ; écrit Vxx.json et Vxx.md' },
    { title: 'Mute test', detail: 'un lecteur sans le texte reconstruit le message ; révision' },
    { title: 'Check', detail: 'pipeline.story --check + soft_check.py, corrections' },
  ],
}

// ---------- paramètres ----------
// args: { id: 'V05', root: '/abs/.../wth-videos',
//         notes?: 'consignes propres à cette vidéo (de l’utilisateur ou de la session)',
//         overwrite?: false   (un storyboard existant n’est jamais écrasé sans ce drapeau : utiliser revise.wf.js),
//         excerpt?: false     (recommander un extrait de 10-15 s),
//         muteRounds?: 1      (tours test muet + révision, 1 ou 2),
//         repo?: racine du dépôt (défaut : root sans /wth-videos) }
const A = args || {}
if (!A.id || !A.root) throw new Error('args requis : {id: "V05", root: "/abs/wth-videos"} ; options : notes, overwrite, excerpt, muteRounds, repo')
const ID = String(A.id)
const ROOT = String(A.root).replace(/\/+$/, '')
const REPO = A.repo ? String(A.repo).replace(/\/+$/, '') : ROOT.replace(/\/wth-videos$/, '')
const SK = `${REPO}/.claude/skills/wth-storyboard`
const REF = `${SK}/references`
const KIT_REF = `${REPO}/.claude/skills/wth-story-build/references`
const WORK = `${ROOT}/build/${ID}/storyboard`
const SB_JSON = `${ROOT}/scripts/storyboards/${ID}.json`
const SB_MD = `${ROOT}/scripts/storyboards/${ID}.md`
const MUTE_ROUNDS = Math.max(1, Math.min(2, Number(A.muteRounds || 1)))

// ---------- schémas ----------
const BEAT = { type: 'object', properties: { t: { type: 'number' }, mot: { type: 'string' }, evenement: { type: 'string' } }, required: ['t', 'mot', 'evenement'] }
const SCENE = {
  type: 'object',
  properties: {
    id: { type: 'string' }, segment: { type: 'string' }, t_start: { type: 'number' }, t_end: { type: 'number' }, texte: { type: 'string' },
    elements: { type: 'string', description: 'cast ids visible in the scene' },
    etat_initial: { type: 'string' }, action: { type: 'string' }, resultat: { type: 'string' }, transition: { type: 'string' },
    beats: { type: 'array', items: BEAT },
    lecture_sans_son: { type: 'string', description: 'what a muted viewer understands (French)' },
  },
  required: ['id', 't_start', 't_end', 'texte', 'elements', 'etat_initial', 'action', 'resultat', 'transition', 'beats', 'lecture_sans_son'],
}
const SB_SCHEMA = {
  type: 'object',
  properties: {
    version: { type: 'string' },
    angle: { type: 'string', description: 'parti pris + « Réponse aux 7 points », one line per rule (French)' },
    thread: { type: 'string', description: 'the narrative thread in 3-6 sentences (French)' },
    objet_fil: { type: 'object', properties: { id: { type: 'string' }, description: { type: 'string' } }, required: ['id', 'description'] },
    cast: { type: 'array', items: { type: 'object', properties: {
      id: { type: 'string' }, name_fr: { type: 'string' }, look: { type: 'string' }, source: { type: 'string', description: 'PNG file name, "code" or "PNG + code"' },
      entite: { type: 'string', description: 'Story entity type + kit macro, or "NOUVEAU : …"' },
      evolution: { type: 'string', description: 'how this element transforms across scenes' } }, required: ['id', 'name_fr', 'look', 'source', 'evolution'] } },
    style: { type: 'string' },
    scenes: { type: 'array', items: SCENE },
    idees_cles: { type: 'array', items: { type: 'object', properties: {
      id: { type: 'string' }, idee: { type: 'string' }, scenes: { type: 'array', items: { type: 'string' } }, principale: { type: 'boolean' } },
      required: ['id', 'idee', 'scenes', 'principale'] } },
    entites_nouvelles: { type: 'array', items: { type: 'object', properties: { nom: { type: 'string' }, description: { type: 'string' }, pourquoi: { type: 'string' } }, required: ['nom', 'description', 'pourquoi'] } },
    test_sans_son: { type: 'object', properties: {
      message_reconstruit: { type: 'string' },
      idees: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, score: { type: 'string', enum: ['GOT', 'PARTIAL', 'MISSED'] }, preuve: { type: 'string' } }, required: ['id', 'score'] } },
      bilan: { type: 'string' },
      changements: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, lecture: { type: 'string' }, changement: { type: 'string' } }, required: ['id', 'lecture', 'changement'] } } },
      required: ['message_reconstruit', 'bilan', 'changements'] },
    excerpt: { type: 'object', properties: { t_start: { type: 'number' }, t_end: { type: 'number' }, why: { type: 'string' } }, required: ['t_start', 't_end', 'why'] },
    risks: { type: 'array', items: { type: 'string' } },
  },
  required: ['version', 'angle', 'thread', 'objet_fil', 'cast', 'style', 'scenes', 'idees_cles'],
}

// ---------- 0. Prep ----------
phase('Prep')
const prep = await agent(`You prepare the storyboard of video ${ID} of the French media "WealthTech Horizon". Do not write anything outside ${WORK}/.

1. Run: python3 ${SK}/scripts/prep.py ${ID} --root ${ROOT}
   It prints the timed sentences and segments, and writes ${WORK}/prep.json, ${WORK}/words.tsv and ${WORK}/pngs.jpg (sheet of the PNGs this video may use: its own carousel set + the generics). Exit code 1 = a prerequisite is missing (no script or no final voice): then return ok=false with the reason.
   If it warns that build/${ID}/audio.wav is missing, run \`python3 -m pipeline.story ${ID} --audio\` from ${ROOT} (rebuilds it from the cached voice, no ElevenLabs call), then run prep.py again: the last scene must end at the real audio duration.
2. Read ${WORK}/prep.json and the script entry "${ID}" in ${ROOT}/scripts/scripts.json (texte, segments, notes_prononciation). If the carousel file ${ROOT}/data/carousels/<source>.json exists, read its slide titles.
3. LOOK at ${WORK}/pngs.jpg with Read. For each carousel PNG (and each generic that could plausibly serve this topic), describe its subject in a few words and how it could serve as a place or object in this video (or "aucun usage").
4. Decide who "Toi" is: the advisor (CGP) if the script talks to a wealth adviser about "ton client", "ton dossier", "ton cabinet"; otherwise the viewer.
5. List every number, amount, percentage, date, acronym and regulatory term of the script, with how it must be written on screen (French typography: « 4 600 € », « 3,5 % », « sept. 2025 »).
6. If the script has numbered steps, traps or errors, propose the legend words of the 1-2-3 marker (one word of 10 letters max per step).
7. Existing storyboard: prep.json has "storyboard_existant", null when there is none, else its version (prep.py prints « storyboard existant : non » or the version). Set storyboard_existant = true exactly when that value is not null, and copy the version into storyboard_version ("" when there is none).
Copy sentences and segments exactly from prep.json (seconds, 3 decimals). Report every problem from prep.json.`, { label: `prep:${ID}`, phase: 'Prep', schema: {
  type: 'object', properties: {
    ok: { type: 'boolean' }, problemes: { type: 'array', items: { type: 'string' } },
    titre: { type: 'string' }, source: { type: 'string' }, duree: { type: 'number' }, mots: { type: 'number' }, debit: { type: 'number' },
    audience: { type: 'string', description: 'who the video addresses and who "Toi" is' },
    phrases: { type: 'array', items: { type: 'object', properties: { t_start: { type: 'number' }, t_end: { type: 'number' }, texte: { type: 'string' } }, required: ['t_start', 't_end', 'texte'] } },
    segments: { type: 'array', items: { type: 'object', properties: { partie: { type: 'string' }, t_start: { type: 'number' }, t_end: { type: 'number' } }, required: ['partie', 't_start', 't_end'] } },
    pngs: { type: 'array', items: { type: 'object', properties: { nom: { type: 'string' }, sujet: { type: 'string' }, usage: { type: 'string' } }, required: ['nom', 'sujet', 'usage'] } },
    chiffres: { type: 'array', items: { type: 'string' } },
    marqueur: { type: 'string', description: 'proposed 1-2-3 marker legend, or "aucun"' },
    cadence: { type: 'string' },
    storyboard_existant: { type: 'boolean', description: 'true when prep.json storyboard_existant is not null' },
    storyboard_version: { type: 'string', description: 'version of the existing storyboard, verbatim from prep.json, or ""' },
  }, required: ['ok', 'problemes', 'titre', 'duree', 'audience', 'phrases', 'segments', 'pngs', 'storyboard_existant'] } })

if (!prep || !prep.ok) {
  log(`${ID} : préparation impossible : ${prep ? prep.problemes.join(' ; ') : 'agent sans réponse'}`)
  return { ok: false, id: ID, stage: 'prep', prep }
}
// Boolean, not free text: a wording such as « aucun » or « absent » must not read as an existing storyboard.
if (prep.storyboard_existant === true && !A.overwrite) {
  const version = prep.storyboard_version || 'sans version'
  log(`${ID} : un storyboard existe déjà (${version}). Révision ciblée : revise.wf.js ; réécriture complète : overwrite: true`)
  return { ok: false, id: ID, stage: 'prep', reason: 'storyboard existant', version }
}
for (const p of prep.problemes || []) log(`${ID} : attention : ${p}`)

const fmt = x => Number(x).toFixed(2).padStart(6)
const SENTENCES = prep.phrases.map(s => `  ${fmt(s.t_start)}-${fmt(s.t_end)} | ${s.texte}`).join('\n')
const SEGMENTS = prep.segments.map(s => `${s.partie} ${Number(s.t_start).toFixed(2)}-${Number(s.t_end).toFixed(2)}`).join(' · ')
const PNGS = prep.pngs.map(p => `  - ${p.nom}: ${p.sujet} → ${p.usage}`).join('\n')

const CTX = `
CONTEXT
- Brand: "WealthTech Horizon", a faceless French media explaining money, finance and wealth-tech on TikTok, Instagram and Facebook. Vertical 1080x1920, 30 fps. Audience of this video and who "Toi" is: ${prep.audience}.
- The whole series uses ONE method, called Story, that the user validated on V01 ("C'est absolument parfait"): flat vector elements on an ivory grid that INTERACT (meet obstacles, approach, separate, transform), one narrative thread, every scene = initial state → visible action → result, synced to word onsets, understandable with the sound off.
- Video ${ID}, « ${prep.titre} », ${prep.duree} s, ${prep.mots} words (${prep.debit} words/s). The voice is FINAL. Sentences with exact timecodes (s):
${SENTENCES}
  Segments: ${SEGMENTS}.
  Word onsets: ${WORK}/words.tsv (i, debut, fin, mot, segment), from ${ROOT}/build/${ID}/words.json. Script: ${ROOT}/scripts/scripts.json, id "${ID}".
  Numbers, dates and terms to show correctly: ${(prep.chiffres || []).join(' ; ') || 'none'}.
  Step-marker legend proposal: ${prep.marqueur || 'none'}. Target cadence: ${prep.cadence || 'about 15-20 compositions and one motion event per second'}.
- THE USER'S BRIEF (verbatim in ${REF}/brief-utilisateur.md, read it):
  1. un fil conducteur; 2. pour chaque scène un état initial, une action visible et un résultat; 3. illustrer le sens complet des phrases; 4. distinguer clairement l'IA et le conseiller (« Toi »); 5. faire évoluer les mêmes éléments entre les scènes; 6. les PNG seulement quand ils servent la mise en scène, les processus animés en code (un zoom sur un PNG ne suffit pas); 7. la simplicité de la référence, ivoire + cyan + typographie lisible, peu d'accents.
  Success criterion: « en masquant les sous-titres, je dois pouvoir comprendre l’action principale et percevoir ce qui change ».
- READ these references before writing (each is short and each rule in them cost a review round on V01):
  - ${REF}/series-bible.md: the recurring cast and rules of the 15 films (ink figure "Toi" is the only one holding tools and deciding; the AI = AI.png acting only through dotted beams and dotted 'ai' ticks, still when it errs; cyan thread object that becomes the « S’abonner » button; 1-2-3 marker WITH a legend; standard end card).
  - ${REF}/lessons-v01.md: review findings turned into rules (proof before verdict and the cause triggered by "Toi"'s gesture; AI vs human ticks differ by shape; the other person arrives on its word, faces "Toi" and stays; never « VALIDÉ » while a question is open; use the frame down to y≈1250; dates « sept. 2025 »; no 50 % grey; light opening).
  - ${REF}/visual-verbs.md: the visual verbs and the Story entity + kit macro that performs each. Stay inside this vocabulary; at most 3 simple new entities.
  - ${REF}/motion-grammar.md and ${REF}/style.md: measured timing, cadence and layout of the reference; series colour tokens, zones, typography.
  - ${REF}/storyboard-schema.md: every field and its constraints. ${REF}/exemple-V01.md: the target level of precision.
  - Entity catalogue if you need detail: ${KIT_REF}/entities.md and ${KIT_REF}/kit.md.
- PNGs this video may use (own carousel + generics only; the code refuses any other):
${PNGS}
  Sheet: ${WORK}/pngs.jpg. PNGs can be moved, scaled, rotated, masked, never deformed or used as a zoom that tells the story.
- Production: the film is built in code (Remotion "Story" composition): flat vector entities with ink outlines and hard shadows, moved by Python macros, frame-exact on word onsets.
- Layout: action between y 250 and 1250 and x 40 to 940; nothing in the top 160 px, the bottom 380 px or right of x 940; centre of composition around y 760-800. Karaoke captions sit at y≈1350 and are handled by the pipeline.
${A.notes ? `- Notes for this video (from the user or the session; they override the defaults): ${A.notes}\n` : ''}`

const REQUIREMENTS = `
Requirements (the storyboard is rejected by \`python3 -m pipeline.story ${ID} --check\` otherwise):
- Cover the whole timeline with 14-22 contiguous scenes, one per sentence or idea; the last scene is the call to action alone (« Abonne-toi pour comprendre ton argent. »), staged as the standard end card (series-bible.md). S01 starts at 0. Each scene's t_start is the exact start of its first word (from words.tsv, 3 decimals). Each t_end equals the next t_start; the last t_end is ${prep.duree}.
- texte: the exact spoken words; all texte fields joined with spaces must equal the script text exactly (same punctuation, ’ apostrophes, … ellipsis).
- beats: at least one per scene; each {t: exact start of the word in words.tsv, mot: the word as in words.tsv, evenement}. One main action per beat, 1-4 active elements, never two beats on the same word in one scene, never more than 3 s without a beat. Every beat will be staged, so only list beats you want to see; a deliberate hold is « Tenue : rien ne bouge ». Write each evenement with a visual verb, the elements, positions (x, y at 1080x1920), sizes, durations and easing.
- etat_initial / action / resultat / transition: precise enough to stage without guessing; each scene starts from the previous result.
- cast: id, name_fr, look (exact shape, size, colour tokens, text shown), source, entite (Story entity + macro, or « NOUVEAU : … »), evolution scene by scene.
- objet_fil {id, description}: the thread object, present in nearly every scene, ending as the « S’abonner » button.
- idees_cles: 6-10 {id, idee, scenes, principale}. Each idea is what a muted viewer must understand, phrased as something visible. principale = true for the ideas of point1, point2, point3 and the chute (at least one each).
- entites_nouvelles: at most 3 simple new entities, only if nothing in the catalogue works ([] otherwise).
- angle: your stance, then « Réponse aux 7 points » with one concrete line per rule.
- version: "v1".${A.excerpt ? '\n- excerpt: recommend a 10-15 s excerpt starting and ending on sentence boundaries that best shows the method.' : ''}
- All user-facing strings in French, correct accents, French number typography.`

// ---------- 1. Draft ----------
const ANGLES = [
  ['objets-persistants', `Angle "persistent objects". Maximise continuity: a small cast follows the thread object from the first frame to the end card, and every element seen later was born earlier (a document becomes a source, a piece of information becomes a line, a doubtful item becomes a question, a time bar becomes the step marker...). Prefer transforming objects over replacing them; nothing appears from nowhere.`],
  ['grammaire-reference', `Angle "reference grammar". Stay as close as possible to the reference's minimal motion language (motion-grammar.md): flat primitives (cards, dots, bars, lines, a protagonist circle or pill) that meet obstacles, get closer, split apart, merge and transform, with hold-then-burst timing and morph handovers. Use the PNGs only as a few anchor places or objects where they add meaning. Keep each composition very simple: 1-3 elements on stage.`],
  ['lisible-sans-son', `Angle "readable with the sound off". Design every scene from the success criterion: with captions hidden, a viewer grasps the main action and sees what changed. Use unmistakable visual verbs (visual-verbs.md): enter, blocked by a wall, extract, stack, link with a thread to a source, crack, strike, stamp, fill, drain, tilt, count, compare before/after. Strong before/after contrasts; no abstract symbolism that needs the voice; labels only confirm what the action already shows.`],
]
phase('Draft')
const drafts = (await parallel(ANGLES.map(([key, brief], i) => () => agent(`${CTX}
TASK: write a COMPLETE storyboard for ${ID} (0 to ${prep.duree} s) from this angle:
${brief}
${REQUIREMENTS}
Do not write any file: return the storyboard.`, { label: `draft:${key}`, phase: 'Draft', schema: SB_SCHEMA })
  .then(d => d ? { label: `D${i + 1}`, angle_key: key, ...d } : null)))).filter(Boolean)
if (!drafts.length) return { ok: false, id: ID, stage: 'draft' }
log(`${ID} : ${drafts.length} brouillons (${drafts.map(d => `${d.label} ${d.angle_key}, ${d.scenes.length} scènes`).join(' ; ')})`)

// ---------- 2. Judge ----------
const LENSES = [
  ['muet', 'Comprehension with captions hidden. For each scene, would a muted viewer grasp the action and the change? Penalise scenes that rely on labels or the voice, abstract symbolism, ambiguous roles, more than one main action at a time, more than about 8 shapes on screen at phone size, and any misreading listed in lessons-v01.md (effect without visible cause, AI that seems to flag its own error, grey that reads as rejected).'],
  ['reference-simplicite', 'Fidelity to the reference motion grammar and simplicity (motion-grammar.md, style.md). Elements interact (obstacle, approach, separation, transformation); hold-then-burst; 1-4 active elements; morph handovers, the stage never empty; one accent (cyan), red only for the alert; continuity with the same elements evolving; series consistency (series-bible.md: cast, places, marker with legend, end card).'],
  ['sens-faisabilite', `Faithfulness to the full meaning of each sentence (rule 3), rules 4 and 5 exactly, and correctness for the audience (financial and regulatory accuracy, numbers equal to the script, French typography, no implicit personal advice). Feasibility with the existing entity catalogue (${KIT_REF}/entities.md, ${KIT_REF}/kit.md, ${REF}/visual-verbs.md): a draft that needs more than 3 new simple entities, or anything beyond flat shapes and the Figure rig (3D, liquids, particles, character animation), loses points. Check also the hard constraints: contiguous scenes on word onsets, beats on exact onsets, no gap over 3 s.`],
]
phase('Judge')
const judged = (await parallel(LENSES.map(([lens, q]) => () => agent(`${CTX}
You are a judge. Score the ${drafts.length} storyboards below from 0 to 10 through ONE lens, "${lens}": ${q}
Use exactly the draft labels ${drafts.map(d => d.label).join(', ')} in "scores". For each draft, list its best ideas worth keeping and its weakest scenes, with scene ids and a concrete fix. Do not write any file.

DRAFTS:
${JSON.stringify(drafts)}`, { label: `judge:${lens}`, phase: 'Judge', schema: {
  type: 'object', properties: {
    lens: { type: 'string' },
    scores: { type: 'array', items: { type: 'object', properties: { draft: { type: 'string' }, score: { type: 'number' } }, required: ['draft', 'score'] } },
    best: { type: 'string' },
    keep: { type: 'array', items: { type: 'string' } },
    weak: { type: 'array', items: { type: 'string' } } },
  required: ['lens', 'scores', 'best', 'keep', 'weak'] } })))).filter(Boolean)

const totals = {}
for (const d of drafts) totals[d.label] = 0
for (const j of judged) for (const s of j.scores) {
  const m = String(s.draft).match(/D\d/)
  if (m && m[0] in totals) totals[m[0]] += Number(s.score) || 0
}
const ranking = Object.entries(totals).sort((a, b) => b[1] - a[1])
const winner = ranking[0][0]
log(`${ID} : notes cumulées ${ranking.map(([k, v]) => `${k} ${v}`).join(', ')} → gagnant ${winner}`)

// ---------- 3. Synthesize ----------
phase('Synthesize')
let final = await agent(`${CTX}
TASK: produce the storyboard of ${ID} by synthesising the drafts and the judges' verdicts. Start from the overall winner, ${winner} (summed scores: ${JSON.stringify(totals)}), graft the best ideas the judges listed for the others, and fix every weak scene they flagged.
The result must form ONE coherent thread around one thread object, read clearly without sound, respect the 7 rules, the series bible and the V01 lessons, and stay buildable with the entity catalogue. Keep the cast small and consistent.
${REQUIREMENTS}

WRITE two files:
- ${SB_JSON}: the storyboard (this schema; UTF-8, ensure_ascii off, 1-space or 2-space indentation).
- ${SB_MD}: the French Markdown version following the template in ${REF}/storyboard-schema.md §6 (title, criterion, Fil conducteur + objet du fil, Idées-clés, Parti pris et réponse aux 7 corrections, Distribution, Style, Storyboard scène par scène with one table per scene and its Temps forts and Sans le son, Entités nouvelles, Risques et replis${A.excerpt ? ', Extrait recommandé' : ''}). Leave the « Test sans son » section as « à venir ».
Then run \`python3 -m pipeline.story ${ID} --check\` from ${ROOT} and fix what it reports (scene boundaries and beats must be exact word onsets from ${WORK}/words.tsv; joined texts must equal the script). Return exactly the final content of ${SB_JSON}, after these fixes.

DRAFTS: ${JSON.stringify(drafts)}
JUDGES: ${JSON.stringify(judged)}`, { label: 'synthesis', phase: 'Synthesize', schema: SB_SCHEMA })
if (!final) return { ok: false, id: ID, stage: 'synthesis', judges: judged.map(j => ({ lens: j.lens, scores: j.scores, best: j.best })) }

// ---------- 4. Mute test + revision ----------
phase('Mute test')
const muteReports = []
for (let round = 1; round <= MUTE_ROUNDS; round++) {
  const visible = final.scenes.map(s => ({ id: s.id, t_start: s.t_start, t_end: s.t_end, elements: s.elements, etat_initial: s.etat_initial, action: s.action, resultat: s.resultat, transition: s.transition }))
  const mute = await agent(`You are a viewer watching a muted vertical video with no captions, from a French channel about money and finance. Below is ONLY what is visible on screen in each scene: no voice, no captions, no title. Do not open any file: answer from this description alone.

For each scene, write in French what you understand happens and what changed. Then reconstruct the overall message of the video in 4-6 sentences.
Be honest: when a scene is ambiguous, say what you would wrongly guess; say what you only understand thanks to written words on screen; say who you think each character or object is.

SCENES: ${JSON.stringify(visible)}`, { label: `mute-viewer:r${round}`, phase: 'Mute test', schema: {
    type: 'object', properties: {
      scenes: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, compris: { type: 'string' }, ambigu: { type: 'string' } }, required: ['id', 'compris'] } },
      message_reconstruit: { type: 'string' } }, required: ['scenes', 'message_reconstruit'] } })
  if (!mute) break
  muteReports.push(mute.message_reconstruit)

  const revised = await agent(`${CTX}
TASK: revise the storyboard of ${ID} using a mute-viewer test (round ${round}). The file ${SB_JSON} is the reference version (the JSON below may predate its last --check fixes): edit the file, and at the end return exactly its final content.
1. Score each idee_cle as GOT, PARTIAL or MISSED from what the muted viewer understood, with evidence.
2. Compare the viewer's reading of each scene with its intended meaning (texte, lecture_sans_son). For every scene read wrong, vague, or where the change is missed, rework the visible action: a clearer visual verb (visual-verbs.md), a stronger before/after, fewer elements, a visible cause. Treat any wrong guess as a contresens to remove. Keep the thread, cast and timings consistent; keep beats on exact word onsets.
3. Fill test_sans_son: message_reconstruit (quote the viewer), idees (the scores), bilan (contresens and blurs), changements (scene, lecture, changement).
4. Set version to "v1 · révisé après le test sans son"${round > 1 ? ` (round ${round})` : ''}.
5. Update ${SB_JSON} and ${SB_MD} (fill the « Test sans son » section: the reconstructed message as a quote, the bilan, a table Scène | Lecture muette | Ce qui change).
6. Run \`python3 -m pipeline.story ${ID} --check\` from ${ROOT} and fix what it reports.

CURRENT STORYBOARD: ${JSON.stringify(final)}
MUTE VIEWER: ${JSON.stringify(mute)}`, { label: `revise:r${round}`, phase: 'Mute test', schema: SB_SCHEMA })
  if (revised) final = revised
  const scores = (final.test_sans_son && final.test_sans_son.idees) || []
  const missed = scores.filter(s => s.score !== 'GOT').map(s => `${s.id}:${s.score}`)
  log(`${ID} : test muet r${round} : ${scores.length - missed.length}/${scores.length} idées GOT${missed.length ? ` (${missed.join(', ')})` : ''}`)
  if (!missed.length) break
}

// ---------- 5. Check ----------
phase('Check')
const check = await agent(`Validate the storyboard of ${ID} written in ${SB_JSON} and ${SB_MD}. From ${ROOT}:
1. Run \`python3 -m pipeline.story ${ID} --check\`. Fix every error with minimal edits to the JSON (scene boundaries and beats on exact word onsets from ${WORK}/words.tsv; joined scene texts equal to the script in ${ROOT}/scripts/scripts.json; 6-10 idees_cles whose scenes exist) and mirror each fix in the .md. Re-run until it prints "storyboard OK".
2. Run \`python3 ${SK}/scripts/soft_check.py ${ID} --root ${ROOT}\`. Fix every ✘ (schema, two beats on the same word in a scene). For each ! alert (more than 3 s without a beat, thread object missing from scenes, a point without a main idea), fix it when the fix is small and keeps the meaning (add a beat on a word with a real visual event, add the thread object to elements, set principale); otherwise leave it and report it.
3. Check that the .md matches the JSON (same scenes, times, beats, idees_cles, version).
Do not change the meaning of scenes, do not commit, do not touch other files.
Return the final outputs of both commands and a 3-line French summary of the storyboard for the user (the thread, the key visual idea of each point, what the mute test changed).`, { label: 'check', phase: 'Check', schema: {
  type: 'object', properties: {
    ok: { type: 'boolean', description: 'true if --check prints "storyboard OK" and soft_check has no ✘' },
    check_output: { type: 'string' }, soft_output: { type: 'string' },
    fixes: { type: 'array', items: { type: 'string' } }, alerts_left: { type: 'array', items: { type: 'string' } },
    resume_fr: { type: 'string' } }, required: ['ok', 'check_output', 'soft_output', 'fixes', 'resume_fr'] } })

return {
  ok: Boolean(check && check.ok),
  id: ID,
  files: [SB_JSON, SB_MD],
  version: final.version,
  scenes: final.scenes.length,
  winner,
  totals,
  judges: judged.map(j => ({ lens: j.lens, scores: j.scores, best: j.best })),
  mute: muteReports,
  test_sans_son: final.test_sans_son ? { idees: final.test_sans_son.idees, bilan: final.test_sans_son.bilan } : null,
  entites_nouvelles: final.entites_nouvelles || [],
  check,
}
