export const meta = {
  name: 'wth-storyboard-revise',
  description: 'Révision ciblée d’un storyboard Story existant (quelques scènes, points faibles d’une revue ou consignes de l’utilisateur), puis test muet, évaluation des idées-clés et contrôle --check',
  whenToUse: 'Corriger des scènes d’un scripts/storyboards/Vxx.json existant sans tout réécrire. args: {id: "V01", root: "<abs>/wth-videos", notes: "points à corriger", scenes?: ["S11","S13"], version?: "v3", muteRounds?}',
  phases: [
    { title: 'Revise', detail: 'scènes visées + continuité, version montée, --check' },
    { title: 'Mute test', detail: '2 lecteurs indépendants sans le texte' },
    { title: 'Evaluate', detail: 'idées-clés GOT / PARTIAL / MISSED, correction ciblée' },
    { title: 'Check', detail: 'pipeline.story --check + soft_check.py' },
  ],
}

// ---------- paramètres ----------
// args: { id: 'V01', root: '/abs/.../wth-videos',
//         notes: 'ce qu’il faut corriger (texte, ou liste de points faibles : revue, contrôle sans son, utilisateur)',
//         scenes?: ['S11', 'S13']  (défaut : celles que les notes désignent),
//         version?: 'v3'           (défaut : version suivante),
//         muteRounds?: 1           (tours test muet + évaluation, 1 ou 2),
//         repo?: racine du dépôt }
const A = args || {}
if (!A.id || !A.root || !A.notes) throw new Error('args requis : {id: "V01", root: "/abs/wth-videos", notes: "points à corriger"} ; options : scenes, version, muteRounds, repo')
const ID = String(A.id)
const ROOT = String(A.root).replace(/\/+$/, '')
const REPO = A.repo ? String(A.repo).replace(/\/+$/, '') : ROOT.replace(/\/wth-videos$/, '')
const SK = `${REPO}/.claude/skills/wth-storyboard`
const REF = `${SK}/references`
const KIT_REF = `${REPO}/.claude/skills/wth-story-build/references`
const WORK = `${ROOT}/build/${ID}/storyboard`
const SB_JSON = `${ROOT}/scripts/storyboards/${ID}.json`
const SB_MD = `${ROOT}/scripts/storyboards/${ID}.md`
const NOTES = Array.isArray(A.notes) ? A.notes.map((n, i) => `${i + 1}. ${n}`).join('\n') : String(A.notes)
const TARGET = Array.isArray(A.scenes) && A.scenes.length ? A.scenes.join(', ') : 'the scenes the notes point to'
const MUTE_ROUNDS = Math.max(1, Math.min(2, Number(A.muteRounds || 1)))

const RULES = `
RULES OF THE SERIES (read the files; each rule cost a review round on V01):
- ${REF}/brief-utilisateur.md: the user's 7 rules, verbatim, and the success criterion « en masquant les sous-titres, je dois pouvoir comprendre l’action principale et percevoir ce qui change ».
- ${REF}/lessons-v01.md, ${REF}/series-bible.md, ${REF}/visual-verbs.md (entities and kit macros: ${KIT_REF}/entities.md, kit.md), ${REF}/style.md, ${REF}/motion-grammar.md.
- ${REF}/storyboard-schema.md: fields and constraints. Scene boundaries and beats sit on exact word onsets (${WORK}/words.tsv); joined scene texts equal the script; 6-10 idees_cles {id, idee, scenes, principale}; objet_fil {id, description}.`

const VISIBLE = {
  type: 'array', items: { type: 'object', properties: {
    id: { type: 'string' }, t_start: { type: 'number' }, t_end: { type: 'number' }, elements: { type: 'string' },
    etat_initial: { type: 'string' }, action: { type: 'string' }, resultat: { type: 'string' }, transition: { type: 'string' } },
    required: ['id', 't_start', 't_end', 'elements', 'etat_initial', 'action', 'resultat', 'transition'] } }
const IDEES = { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, idee: { type: 'string' }, scenes: { type: 'array', items: { type: 'string' } }, principale: { type: 'boolean' } }, required: ['id', 'idee', 'scenes'] } }

// ---------- 1. Revise ----------
phase('Revise')
const rev = await agent(`You revise the existing storyboard of video ${ID} ("WealthTech Horizon", French finance media, Story method validated by the user on V01).
${RULES}

1. Run \`python3 ${SK}/scripts/prep.py ${ID} --root ${ROOT} --no-sheet\` (refreshes ${WORK}/words.tsv and prep.json). If it fails, or ${SB_JSON} does not exist, return ok=false with the reason.
2. Read ${SB_JSON} (it is the reference; ${SB_MD} is its French Markdown twin).
3. Apply these notes to ${TARGET}:
${NOTES}
   Rework only what the notes require, with the series' visual verbs: a visible cause, a clearer before/after, fewer elements. Then keep continuity: adjust the neighbouring scenes' etat_initial / transition and the cast's evolution where the change propagates, and nothing else. Keep the scene boundaries unless a note requires moving them; every beat stays on an exact word onset.
4. If the storyboard lacks objet_fil or idees_cles (older versions), add them (see ${REF}/storyboard-schema.md §4 and the V01 example in ${REF}/exemple-V01.md). Update idees_cles if the revision changes what a muted viewer must understand.
5. Set version to ${A.version ? `"${A.version} · révision ciblée"` : 'the next version number (v2 → v3…) followed by « · révision ciblée »'} and append {version, scenes, pourquoi} to "revisions".
6. Update ${SB_JSON} and ${SB_MD} (same changes; add or extend a « Révisions » section listing, per scene, what changed and why).
7. Run \`python3 -m pipeline.story ${ID} --check\` from ${ROOT} and fix what it reports.
Do not commit and do not touch other files.
Return the version, the changed scenes (before → after, in French), the visible fields of ALL scenes as they now are in the file, and the idees_cles.`, { label: `revise:${ID}`, phase: 'Revise', schema: {
  type: 'object', properties: {
    ok: { type: 'boolean' }, reason: { type: 'string' }, version: { type: 'string' },
    changed: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, avant: { type: 'string' }, apres: { type: 'string' } }, required: ['id', 'avant', 'apres'] } },
    visible: VISIBLE, idees_cles: IDEES, check_output: { type: 'string' } },
  required: ['ok', 'version', 'changed', 'visible', 'idees_cles'] } })
if (!rev || !rev.ok) {
  log(`${ID} : révision impossible : ${rev ? rev.reason : 'agent sans réponse'}`)
  return { ok: false, id: ID, stage: 'revise', rev }
}
log(`${ID} : ${rev.version} : ${rev.changed.map(c => c.id).join(', ')} révisées`)

// ---------- 2-3. Mute test + Evaluate ----------
let visible = rev.visible
let idees = rev.idees_cles
let evaluation = null
const viewersMessages = []
for (let round = 1; round <= MUTE_ROUNDS; round++) {
  phase('Mute test')
  const viewers = (await parallel([0, 1].map(i => () => agent(`You are viewer #${i + 1}, watching a muted vertical video with no captions from a French channel about money and finance. Below is ONLY what is visible on screen in each scene: no voice, no captions, no title. Do not open any file: answer from this description alone.

For each scene, write in French what you understand happens, who each character or object seems to be, and what changed. Then reconstruct the overall message in 4-6 sentences. Be honest: say what you would wrongly guess where a scene is ambiguous, and what you only understand thanks to written words on screen.

SCENES: ${JSON.stringify(visible)}`, { label: `mute-viewer-${i + 1}:r${round}`, phase: 'Mute test', schema: {
    type: 'object', properties: {
      scenes: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, compris: { type: 'string' }, ambigu: { type: 'string' } }, required: ['id', 'compris'] } },
      message_reconstruit: { type: 'string' } }, required: ['scenes', 'message_reconstruit'] } })))).filter(Boolean)
  if (!viewers.length) break
  viewersMessages.push(...viewers.map(v => v.message_reconstruit))

  phase('Evaluate')
  evaluation = await agent(`Two independent muted viewers read the visible description of the storyboard of ${ID} (no voice, no captions). Their reports are below.
${RULES}

1. Score each idee_cle below as GOT, PARTIAL or MISSED from the two reports, with evidence (quote them). Pay special attention to the revised scenes (${rev.changed.map(c => c.id).join(', ')}): did the revision land, and did it create a new misreading?
2. Answer the user's criterion in French: « en masquant les sous-titres, je dois pouvoir comprendre l’action principale et percevoir ce qui change » (oui / non, nuancé).
3. If an idea is MISSED, a main idea (principale) is PARTIAL, or a revised scene is misread: make ONE targeted fix to the scenes concerned in ${SB_JSON} and ${SB_MD} (the file is the reference), keeping beats on exact word onsets, then run \`python3 -m pipeline.story ${ID} --check\` from ${ROOT} and fix what it reports. Otherwise change nothing in the scenes.
4. In both files, update test_sans_son: message_reconstruit (quote one viewer), idees (your scores), bilan, changements (scene, lecture, changement) — keep earlier entries and add the new ones.
Do not commit.
Return the scores, the criterion answer, the fixes made, and the visible fields of ALL scenes as they now are in the file.

IDEES_CLES: ${JSON.stringify(idees)}
VIEWERS: ${JSON.stringify(viewers)}`, { label: `evaluate:r${round}`, phase: 'Evaluate', schema: {
    type: 'object', properties: {
      scores: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, score: { type: 'string', enum: ['GOT', 'PARTIAL', 'MISSED'] }, preuve: { type: 'string' } }, required: ['id', 'score', 'preuve'] } },
      critere: { type: 'string' }, fixes: { type: 'array', items: { type: 'string' } }, visible: VISIBLE },
    required: ['scores', 'critere', 'fixes', 'visible'] } })
  if (!evaluation) break
  visible = evaluation.visible
  const weak = evaluation.scores.filter(s => s.score !== 'GOT').map(s => `${s.id}:${s.score}`)
  log(`${ID} : test muet r${round} : ${evaluation.scores.length - weak.length}/${evaluation.scores.length} idées GOT${weak.length ? ` (${weak.join(', ')})` : ''} ; ${evaluation.fixes.length} correction(s)`)
  if (!evaluation.fixes.length) break
}

// ---------- 4. Check ----------
phase('Check')
const check = await agent(`Validate the revised storyboard of ${ID} (${SB_JSON} and ${SB_MD}). From ${ROOT}:
1. Run \`python3 -m pipeline.story ${ID} --check\`; fix every error with minimal edits (exact word onsets from ${WORK}/words.tsv, texts equal to the script, idees_cles) and mirror them in the .md; re-run until "storyboard OK".
2. Run \`python3 ${SK}/scripts/soft_check.py ${ID} --root ${ROOT}\`; fix every ✘; fix ! alerts when the fix is small and keeps the meaning, otherwise report them.
3. Check that the .md matches the JSON (scenes, times, beats, idees_cles, version, Révisions, Test sans son).
Do not change the meaning of scenes, do not commit.
Return both outputs and a 3-line French summary of what this revision changed and what the mute test says.`, { label: 'check', phase: 'Check', schema: {
  type: 'object', properties: {
    ok: { type: 'boolean' }, check_output: { type: 'string' }, soft_output: { type: 'string' },
    fixes: { type: 'array', items: { type: 'string' } }, alerts_left: { type: 'array', items: { type: 'string' } }, resume_fr: { type: 'string' } },
  required: ['ok', 'check_output', 'soft_output', 'fixes', 'resume_fr'] } })

return {
  ok: Boolean(check && check.ok),
  id: ID,
  files: [SB_JSON, SB_MD],
  version: rev.version,
  changed: rev.changed,
  mute: viewersMessages,
  scores: evaluation ? evaluation.scores : null,
  critere: evaluation ? evaluation.critere : null,
  check,
}
