export const meta = {
  name: 'wth-story-build-review',
  description: 'Stage a WealthTech Horizon film from its storyboard (Story API + kit), render it with and without captions, review it (mute viewer + 3 critics + mute-eval on idees_cles), fix in up to maxRounds rounds, then run QA and the final mute check',
  whenToUse: 'Full Story film of one video once its voice and storyboard are final (skill wth-story-build). args: {id: "V07", root: "<repo>/wth-videos", parts?: 3 | [["S01","S06"], ...], maxRounds?: 2, verify?: true, from?: "start" | "review" | "verify"}',
  phases: [
    { title: 'Prepare', detail: 'storyboard check, cast and parts plan, new entities only if needed' },
    { title: 'Author', detail: 'scene parts written in parallel (2 at a time)' },
    { title: 'Integrate', detail: 'whole-film props, seam stills, full render, review sheets' },
    { title: 'Review', detail: 'mute viewer + 3 critics, then mute-eval against idees_cles' },
    { title: 'Fix', detail: 'blocker and major findings, re-render' },
    { title: 'Verify', detail: 'QA, then the final mute check (mute-verify.wf.js)' },
  ],
}

// ---------- parameters ----------
const A = args && typeof args === 'object' ? args : {}
if (!A.id || !A.root) {
  throw new Error('build-review.wf.js: args {id: "V07", root: "/abs/path/wth-videos"} are required')
}
const ID = String(A.id)
const ROOT = String(A.root).replace(/\/+$/, '')
const REPO = A.repo ? String(A.repo).replace(/\/+$/, '') : ROOT.replace(/\/wth-videos$/, '')
const SKILL = `${REPO}/.claude/skills/wth-story-build`
const SB_SKILL = `${REPO}/.claude/skills/wth-storyboard`
const MAX_ROUNDS = Number.isInteger(A.maxRounds) && A.maxRounds >= 0 ? A.maxRounds : 2
const VERIFY = A.verify !== false
const FROM = ['start', 'review', 'verify'].includes(A.from) ? A.from : 'start'
const PARTS_LIST = Array.isArray(A.parts) ? A.parts : null
const N_PARTS = Number.isInteger(A.parts) && A.parts >= 1 ? A.parts : 3

const SB = `${ROOT}/scripts/storyboards/${ID}.json`
const SB_MD = `${ROOT}/scripts/storyboards/${ID}.md`
const SPEC = `${ROOT}/scripts/story/${ID}`
const OUT = `${ROOT}/output/WTH-${ID}.mp4`
const NOCAP = `${ROOT}/build/${ID}/story/film_sans_sous_titres.mp4`
const REV = `${ROOT}/build/${ID}/review/film`
const REV_NOCAP = `${ROOT}/build/${ID}/review/film_nocap`
const MUTE_VERIFY = `${SKILL}/workflows/mute-verify.wf.js`
// The approved V01 sheet still shows six defects that the excerpt's mute check found and that became rules since.
const SHEET_DEFECTS = `That sheet shows six defects that are rules now; do NOT copy them: (1) AI and human ticks of the same shape, differing only by colour (#125 grey, #438 cyan): the AI's tick takes variant "ai"; (2) line L5 breaks on « fausse » with no one's gesture (#146): the advisor's pen must cause it; (3) ambiguous dates « 09/2025 », « 03/2026 » (#258 on): write « sept. 2025 »; (4) lines greyed to about 50 % in S13 (#300, #362), which read as "rejected"; (5) VALIDÉ stamped while the « ? » is still open (#469): mark it « à poser au RDV »; (6) the bottom 40 % of the frame left empty: use it down to y≈1250.`

const CTX = `
CONTEXT
- Brand: "WealthTech Horizon", a faceless French media explaining finance and wealth-tech on TikTok, Instagram and Facebook. Vertical 1080x1920 video at 30 fps, 45 s to 3 min (no 60 s limit since 21/10: the script opens on the problem, announces what the video shows, and puts context in the transitions).
- Method "Story", validated by the user on V01 ("C'est absolument parfait"): an ivory scene graph of persistent entities; one narrative thread; every scene = initial state -> visible action -> result; events on word onsets; readable with the sound off.
  - The user's success criterion, verbatim: « en masquant les sous-titres, je dois pouvoir comprendre l’action principale et percevoir ce qui change ».
  - His 7 rules, verbatim: ${SB_SKILL}/references/brief-utilisateur.md.
- Video ${ID}. Run every command in ${ROOT}.
  - Canonical storyboard: ${SB}, French readable version ${SB_MD}. It holds the thread, objet_fil, the cast with each element's evolution, the style, and the scenes (etat_initial / action / resultat / transition, beats {t, mot, evenement}, lecture_sans_son). It also holds idees_cles, the ideas the mute check scores.
  - Final voice: build/${ID}/words.json (word onsets) and build/${ID}/audio.wav. Script: scripts/scripts.json, id "${ID}".
  - Staging spec (a package): ${SPEC}/__init__.py (cast + build) and parts p1.py, p2.py...
- Follow the skill ${SKILL}/SKILL.md. Read the references it points to when you need them:
  - writing: references/story-api.md, references/kit.md, references/entities.md;
  - reviewing: references/review-lenses.md;
  - QA: references/qa-checklist.md;
  - any error: references/troubleshooting.md.
  The visual target is ${SKILL}/assets/v01_reference_sheet.jpg (the approved V01 excerpt): match its legibility, density and finish, NOT its details. ${SHEET_DEFECTS}
- Hard rules:
  - Renders: only one Remotion render at a time on this 4-CPU machine. Render ONLY through make (story, story-stills, review-sheets) or "python3 -m pipeline.story", which wait on build/.render.lock. Never call npx remotion yourself and never delete the lock file.
  - Disk: never extract full-resolution frames of the film; use the outputs of make review-sheets. An extra frame, when a detail really needs it, goes to build/${ID}/review/frames/ as JPEG, at most 6 per agent. Run "make clean-tmp" after renders.
  - Off-limits: do NOT git commit or push. Do NOT touch cache/tts, config.yaml, scripts/scripts.json, Cloudinary, Metricool or Google Drive.
  - Storyboard: never change its texte, idees_cles or scene boundaries. A beat may move to a neighbouring word only if the scene cannot work otherwise; then "make storyboard-check ID=${ID}" must still pass, and you list it as a deviation.
  - Shared code (motion/src/story, pipeline/story*.py, geometry.json) serves every film and the approved V01 excerpt. Any new behaviour must be opt-in (a new type, parameter or variant) with defaults unchanged, and "make story-check" must pass.
  - On-screen text is in French, with correct accents and French typography. Dates are written out (« sept. 2025 »).
`

// ---------- schemas ----------
const CAST = {
  type: 'object',
  properties: {
    ok: { type: 'boolean', description: 'false if the storyboard or the voice is not ready' },
    storyboard_check: { type: 'string' },
    parts: { type: 'array', items: { type: 'object', properties: {
      name: { type: 'string', description: 'p1, p2...' },
      scenes: { type: 'array', items: { type: 'string' } },
      first_frame: { type: 'integer', description: 'film frame of the first scene start' },
      last_frame: { type: 'integer', description: 'last film frame of the part (next part first_frame - 1, or the film end)' },
      entry_state: { type: 'string', description: 'state pinned at first_frame - 1, from the etat_initial of its first scene' },
      brief: { type: 'string', description: 'what the part must show scene by scene, the cast ids it uses, the hand-over into the next part' } },
      required: ['name', 'scenes', 'first_frame', 'last_frame', 'entry_state', 'brief'] } },
    cast_ids: { type: 'array', items: { type: 'string' } },
    layout: { type: 'string', description: 'shared constants and screen places written in __init__.py' },
    new_entities: { type: 'array', items: { type: 'object', properties: {
      type: { type: 'string' }, why: { type: 'string', description: 'why no existing type or combination works' },
      params: { type: 'string' }, tracks: { type: 'string' }, look: { type: 'string' } },
      required: ['type', 'why', 'params', 'tracks', 'look'] } },
    files_changed: { type: 'array', items: { type: 'string' } },
    problems: { type: 'array', items: { type: 'string' } },
  },
  required: ['ok', 'parts', 'cast_ids', 'new_entities', 'problems'],
}

const SIMPLE = {
  type: 'object',
  properties: {
    ok: { type: 'boolean' },
    files_changed: { type: 'array', items: { type: 'string' } },
    notes: { type: 'string' },
  },
  required: ['ok', 'files_changed', 'notes'],
}

const PART_REPORT = {
  type: 'object',
  properties: {
    ok: { type: 'boolean', description: 'true when every beat of the part is staged, with no kit warning and clean stills' },
    part: { type: 'string' },
    scene_by_scene: { type: 'string', description: 'per scene and beat: what is visible and what happens, as implemented' },
    shared_additions: { type: 'array', items: { type: 'string' }, description: 'anything added to __init__.py' },
    deviations_from_storyboard: { type: 'array', items: { type: 'string' } },
    known_issues: { type: 'array', items: { type: 'string' } },
  },
  required: ['ok', 'part', 'scene_by_scene', 'known_issues'],
}

const BUILD_REPORT = {
  type: 'object',
  properties: {
    ok: { type: 'boolean', description: 'true when the complete film was rendered (output and no-caption version)' },
    output: { type: 'string' },
    output_no_captions: { type: 'string' },
    review_dirs: { type: 'array', items: { type: 'string' } },
    qa_ok: { type: 'boolean' },
    qa_failed: { type: 'array', items: { type: 'string' }, description: 'failed QA checks with their values' },
    files_changed: { type: 'array', items: { type: 'string' } },
    scene_by_scene: { type: 'string', description: 'per scene and beat: what is visible and what happens, as implemented' },
    deviations_from_storyboard: { type: 'array', items: { type: 'string' } },
    fixes: { type: 'array', items: { type: 'object', properties: {
      finding: { type: 'string' }, done: { type: 'boolean' }, change: { type: 'string' } },
      required: ['finding', 'done', 'change'] } },
    known_issues: { type: 'array', items: { type: 'string' } },
  },
  required: ['ok', 'output', 'output_no_captions', 'qa_ok', 'files_changed', 'scene_by_scene', 'known_issues'],
}

const FINDING = {
  type: 'object',
  properties: {
    severity: { type: 'string', enum: ['blocker', 'major', 'minor'] },
    scene: { type: 'string' },
    time_s: { type: 'string' },
    problem: { type: 'string' },
    evidence: { type: 'string', description: 'which sheet, strip or frame shows it' },
    fix: { type: 'string', description: 'concrete change in entities, kit macros, layout or timing' },
  },
  required: ['severity', 'problem', 'evidence', 'fix'],
}

const FINDINGS = {
  type: 'object',
  properties: {
    lens: { type: 'string' },
    verdict: { type: 'string', enum: ['ship', 'fix-then-ship', 'not-ready'] },
    findings: { type: 'array', items: FINDING },
    strengths: { type: 'array', items: { type: 'string' } },
  },
  required: ['lens', 'verdict', 'findings'],
}

const MUTE_VIEW = {
  type: 'object',
  properties: {
    beats: { type: 'array', items: { type: 'object', properties: {
      t: { type: 'string' }, action: { type: 'string' }, acteurs: { type: 'string' },
      changement: { type: 'string' }, ambiguite: { type: 'string' } },
      required: ['t', 'action', 'changement'] } },
    message: { type: 'string', description: 'what the video is trying to say, 4-6 sentences' },
    ambiguites: { type: 'array', items: { type: 'string' } },
  },
  required: ['beats', 'message', 'ambiguites'],
}

const SCORE = {
  type: 'object',
  properties: {
    id: { type: 'string' },
    idee: { type: 'string' },
    principale: { type: 'boolean' },
    score: { type: 'string', enum: ['GOT', 'PARTIAL', 'MISSED'] },
    preuve: { type: 'string' },
  },
  required: ['id', 'idee', 'principale', 'score', 'preuve'],
}

const MUTE_EVAL = {
  type: 'object',
  properties: {
    lens: { type: 'string' },
    verdict: { type: 'string', enum: ['ship', 'fix-then-ship', 'not-ready'] },
    scores: { type: 'array', items: SCORE },
    findings: { type: 'array', items: FINDING },
  },
  required: ['lens', 'verdict', 'scores', 'findings'],
}

const QA_REPORT = {
  type: 'object',
  properties: {
    ok: { type: 'boolean', description: 'final "make qa" result' },
    checks: { type: 'array', items: { type: 'object', properties: {
      check: { type: 'string' }, ok: { type: 'boolean' }, value: { type: 'string' } },
      required: ['check', 'ok', 'value'] } },
    failed: { type: 'array', items: { type: 'string' } },
    fixed: { type: 'array', items: { type: 'string' } },
    rerendered: { type: 'boolean' },
  },
  required: ['ok', 'checks', 'failed', 'rerendered'],
}

// ---------- review lenses (see references/review-lenses.md) ----------
const SEVERITY = `Severity:
- blocker: defeats the user's request (his criterion or one of his 7 rules) or would embarrass the brand;
- major: clearly visible, or the meaning of a scene is unclear or wrong;
- minor: polish.`

const CRITICS = [
  ['reference-continuity', `Mise-en-scène against the storyboard, the user's 7 rules and the reference motion grammar (${SB_SKILL}/references/motion-grammar.md). Use the beat strips ${REV}/beats/*.jpg, one per beat. Each strip shows frames f-3 to f+12, and its title gives the scene, the word and the intended event. Use also the sheets ${REV}/sheets/*.jpg, against ${SB}. Check scene by scene:
- elements really INTERACT and TRANSFORM (they meet obstacles, approach, separate, become something else) rather than appear, zoom or fade in sequence;
- each scene shows its etat_initial -> action -> resultat, and hands over to the next one as its transition says;
- the same entities persist along the thread (objet_fil); nothing is replaced when it could evolve;
- hold then burst: still between beats, one burst per beat, 1-4 active elements;
- every event lands on its word (strip frame +0 is the word onset);
- the AI and the human are unmistakably distinct: the shape of their marks, tools only in the human's hand, the AI acting through dotted beams. The human's tool CAUSES the change, and the proof comes before the verdict;
- the full meaning of each sentence is shown, not just its keyword.`],
  ['visual-brand', `Visual quality and identity on ivory, at phone size first. Use these sources:
- the phone sheets ${REV}/phone/phone_*.jpg: re-encoded at 2 Mb/s and 360 px wide, this is what viewers see;
- the half-resolution sheets ${REV}/sheets/*.jpg;
- at most 6 full-resolution frames, extracted into build/${ID}/review/frames/visual-brand/ as JPEG, only where a detail must be checked.
Compare with the approved level, ${SKILL}/assets/v01_reference_sheet.jpg: match its legibility and density, NOT its six superseded defects (see CONTEXT); report any of them you find in this film as a finding. Check:
- legibility at phone size (text at least 32 px at scale 1, short lines), typographic hierarchy, French spelling and typography;
- colour discipline: ivory, ink, a single cyan accent, deep cyan for the human; red only for the alert element; no 50 % greyed lines that read as "rejected";
- simplicity: 1-4 active elements and about 8 primitives at most at phone size; calm and premium, like the reference;
- composition: action centred around y≈800 and using the frame down to y≈1250, with no empty bottom 40 %. Safe zones empty: top 160 px, bottom 380 px, x > 940. No collision with the caption line (y 1280-1380);
- PNG compositing on ivory: fringes, leftover glow, shadows (a contact shadow is preferred);
- alignment of wires, boxes and stickers; wires start on the text they prove; the last frame of each scene has no collision;
- banding or mush after the re-encode.`],
  ['sync-technical', `Sync and technical. Use these sources:
- the beat strips ${REV}/beats/*.jpg;
- the holds report ${REV}/holds.json;
- the props build/${ID}/story/props_film.json: meta.beats, meta.beats_off_onset, meta.storyboard_beats_missing, meta.beats_snapped_to_attack and captions;
- the QA report output/qa/${ID}.json, written by make story. Re-run "make qa ID=${ID}" only if that report is older than ${OUT}.
Check:
- every beat event starts on its word-onset frame (strip frame +0); nothing important starts mid-word or on a hold beat;
- holds: no frozen picture over 3.5 s except the end card, and no hold that feels dead even under 3.5 s;
- karaoke: the highlighted word changes on the exact onset; caption groups read naturally (2-3 words, at most 760 px); alert words are red only where intended;
- QA: list every failed check with its value. "Version sans sous-titres conforme" must pass;
- the code of the staging package:
  - beat or word lookups (kit.at, S.word_after) instead of magic frame numbers;
  - no keys on figures outside the Figure rig;
  - every part ends before the next one starts;
  - no "attention (kit)" warning in the output of "make story-props ID=${ID}".`],
]

// ---------- stages ----------
function castPrompt() {
  const partsRule = PARTS_LIST
    ? `Use exactly these parts (scene ranges, inclusive): ${JSON.stringify(PARTS_LIST)}.`
    : `Split the scenes into ${N_PARTS} contiguous parts of similar weight: count beats and seconds. Cut at scene boundaries where the composition changes, ideally on a morph.`
  return `${CTX}
TASK (cast and plan): prepare the staging package of ${ID}. Other agents will write the parts in parallel from your plan.
1. Check the inputs:
   - run "make storyboard-check ID=${ID}";
   - check that build/${ID}/tts.json and words.json exist.
   If the check fails or the voice is missing, stop and return ok=false with the errors in problems. The storyboard belongs to the wth-storyboard skill and the voice to wth-video: do not fix them here.
2. Read the inputs:
   - ${SKILL}/SKILL.md, then references/story-api.md, kit.md and entities.md;
   - the storyboard JSON and Markdown in full;
   - the reference sheet ${SKILL}/assets/v01_reference_sheet.jpg (look at it).
   If a spec already exists, read it and reuse what works for the scenes it covers. The two forms cannot coexist: a single-file scripts/story/${ID}.py must be migrated into the package (git mv, then split).
3. Plan the parts. ${partsRule} For each part, give:
   - its scenes;
   - its first and last film frames (frame = round(t * 30));
   - its entry state, the etat_initial of its first scene, which the author pins at first_frame - 1;
   - a precise brief: scene by scene, what must be visible and happen, the cast ids used, and the hand-over into the next part.
4. Decide the new entity types. Only when no existing type or combination of types (entities.md, kit.md) can do the job; at most 3, each simple. Give each one's API: type name, params, tracks, look.
5. Write the package, following the template in SKILL.md (section "Procédure", steps 1 and 2):
   - ${SPEC}/__init__.py:
     - PARTS; ALERT_WORDS; ACOUSTIC_SNAP = {"gap": 0.2, "window": 0.08}; CAPTION_GROUPS only if a caption group would otherwise be wrong;
     - the shared layout constants: action column, ground line, places of the persistent objects;
     - cast(S, kit), which declares EVERY entity of the film at its frame-0 state (later arrivals with scale=0, figures with Figure(..., show=False) when they enter later). It returns a SimpleNamespace with the figures, sheets and ids that the parts need;
     - build(S), with the WTH_PARTS isolation.
     Declare the planned new entity types with S.add under their planned name and params: props build without the TSX.
   - One stub per part, ${SPEC}/pN.py, with a docstring (scenes, entry state, brief) and "def part(S, kit, c): pass".
6. Run "make story-props ID=${ID} ALLOW_PARTIAL=1". It must build with no Python error and no "attention (kit)" line. Unstaged-scene warnings are expected at this stage.
Return the plan.`
}

function entitiesPrompt(list) {
  return `${CTX}
TASK (new entities): implement these entity types for ${ID}, exactly with this API: ${JSON.stringify(list)}.
Follow SKILL.md, section "Ajouter une entité":
- draw each type in motion/src/story/entities_kit.tsx, centred on its origin, in the flat style: ink outline 4-5 px, hard shadow via Hard, colours via usePalette(), tracks read with r.get(track, default);
- register it in KIT and add its name to the Entity.type comment in types.ts;
- add a Python declaration Kit.<type> in pipeline/story_kit.py, modelled on Kit.gauge;
- put any geometry that Python needs in geometry.json;
- put on-screen text in the text, title or labels keys, which QA spell-checks.
Never change an existing type's defaults.
Then:
- "make story-check" must pass;
- render stills that show each new entity in its key states. Temporary keys in the cast are fine if you remove them afterwards. Run 'make story-stills ID=${ID} ALLOW_PARTIAL=1 FRAMES="..."' and LOOK at the PNGs;
- document each type in ${SKILL}/references/entities.md, in the same format as the others.`
}

function authorPrompt(p, next) {
  const end = next ? `frame ${next.first_frame}, where ${next.name} starts` : 'the end of the film'
  return `${CTX}
TASK (author ${p.name}): write ${SPEC}/${p.name}.py, the staging of scenes ${p.scenes.join(', ')} (film frames ${p.first_frame}-${p.last_frame}).
Cast and shared layout are in ${SPEC}/__init__.py: read it. Another author writes another part at the same time, so never rewrite __init__.py. If an entity or a constant is missing, add it with a minimal Edit and report it.
Brief: ${p.brief}
Entry state, to pin at ${p.first_frame - 1}: ${p.entry_state}
Rules:
- Signature: "def part(S, kit, c)". Open with kit.pin(${p.first_frame} - 1, {...}) from the entry state. Never pin a figure: place figures with walk or enter.
- A figure that entered in an earlier part is invisible when your part is built alone (WTH_PARTS). Guard it as in SKILL.md, step 2: if S.val(id, "scale", f0 - 1) == 0, then fig.enter(f0 - 10, at=...). In the full film this does nothing.
- Place every storyboard beat of your scenes: kit.at for an event, kit.hold for a deliberate hold. The "what" must describe the visible event, because reviewers read it.
- Follow each scene: etat_initial -> action -> resultat, each beat's evenement on its word, and the transition into the next scene. Elements persist and transform (rule 5).
- Apply SKILL.md, section "Grammaire de mise en scène":
  - durations, hold then burst, 1-4 active elements;
  - layout down to y≈1250 within x 40-940 / y 160-1270;
  - colours; AI versus human (the AI's tick has variant "ai"; only the human holds tools);
  - the human's tool causes the change; no VALIDÉ while a question is open; written-out dates; a legend on the 1-2-3 marker.
- Everything you start ends before ${end}.
- Write in time order: fly, path, the macros and the Figure rig read the state at f - 1 when you call them.
Check, in ${ROOT}:
1. Run 'WTH_PARTS=${p.name} make story-props ID=${ID} ALLOW_PARTIAL=1'. Required:
   - no Python error;
   - none of your scenes listed under "temps forts du storyboard sans événement" or "scènes sans aucun temps fort";
   - no "attention (kit)" line from your part, except "(saut)" pin warnings, which are expected in an isolated run;
   - no frame under "temps forts hors début de mot".
2. Run 'WTH_PARTS=${p.name} make story-stills ID=${ID} ALLOW_PARTIAL=1 FRAMES="..."' for your scene starts + 2, each beat's result (beat frame + 12) and your last frame, at most 16 frames per call. With WTH_PARTS your props (build/${ID}/story/props_film_partiel_${p.name}*.json) and stills are your own: read only the PNGs of the frames you asked for, in build/${ID}/story/stills/${p.name}/ (sNNNN.png). Fix overlaps, illegible text, elements outside the safe area, more than one main action at a time, and an empty bottom of the frame. Do at most 3 still passes.
3. If another part breaks a full build while you work, it is not yours: keep using WTH_PARTS.
Report what you implemented, scene by scene.`
}

function integratePrompt(cast, parts) {
  return `${CTX}
TASK (integrate and render): assemble and render the full film of ${ID}.
Parts plan: ${JSON.stringify((cast && cast.parts) || []).slice(0, 4000)}
Author reports: ${JSON.stringify(parts).slice(0, 8000)}
A part whose author failed or left issues is yours to finish now, following ${SKILL}/SKILL.md.
1. Run "make story-props ID=${ID}" without ALLOW_PARTIAL. It must pass with:
   - no beat without an event and no unstaged scene;
   - no "attention (kit)" warning, in particular no "(saut)" at the part seams (fix the end state of the earlier part, or the pin);
   - no beat off its word onset.
2. Seams: run 'make story-stills ID=${ID} FRAMES="..."' at each part boundary (first_frame - 3, first_frame, first_frame + 12) and at each scene start + 2. Read the PNGs and fix jumps, duplicates and collisions.
3. If motion/src/story or pipeline changed, run "make story-check".
4. Render with "make story ID=${ID}": both versions take about 4 min, then QA about 2 min. Exit code 1 may only mean that QA failed while the film was rendered. Read output/qa/${ID}.json and report the failed checks.
5. Make the review sheets: "make review-sheets ID=${ID}", then 'make review-sheets ID=${ID} REVIEW="--nocap --sheets --phone"', then "make clean-tmp".
6. Read the captioned sheets ${REV}/sheets/*.jpg end to end. Fix anything obviously broken, then re-render and redo step 5.
Report scene by scene what the film shows.`
}

function inspectPrompt() {
  return `${CTX}
TASK (resume at review): the film of ${ID} is already rendered. Check that build/${ID}/story_render.json, ${OUT} and ${NOCAP} exist. If they are missing, return ok=false.
Then:
- regenerate the review sheets: "make review-sheets ID=${ID}" and 'make review-sheets ID=${ID} REVIEW="--nocap --sheets --phone"';
- read output/qa/${ID}.json (the last QA) and report its failed checks;
- summarise scene by scene what the sheets ${REV}/sheets/*.jpg show.`
}

function criticPrompt(round, b, lens, brief) {
  return `${CTX}
You are a demanding critic reviewing the FULL film of ${ID} (review round ${round}) through ONE lens. Do not modify project files. The review sheets are already made: do not extract frames beyond what your lens allows.
Film: ${OUT} (with captions) and ${NOCAP} (without). Build report: ${b ? JSON.stringify(b).slice(0, 6000) : '(not available)'}
LENS "${lens}": ${brief}
${SEVERITY}
For each finding, give:
- the scene id, the timecode and the film frame;
- the evidence: which sheet, strip or frame shows it;
- a concrete fix, in terms of entities, kit macros, layout or timing.
List the strengths to keep too.`
}

function mutePrompt(round) {
  return `You are a first-time viewer of a short vertical video, muted and WITHOUT captions. You do not know its topic or its script.
Look ONLY at the images below. Do not open any other file of the repository: no storyboard, script, spec, props or report. Reading them would spoil the test.
1. First, the phone-size sheets, in order, to get the flow: ${REV_NOCAP}/phone/phone_*.jpg (what a phone shows, 2 images per second).
2. Then the detail sheets, all of them, in order: ${REV_NOCAP}/sheets/sheet_*.jpg (6 images per second, half resolution). Each frame is labelled "scene id, time, film frame #".
Describe, beat by beat with timestamps:
- the main action;
- who acts: what each character or object seems to be;
- what changes.
Then say in 4-6 sentences what the video is trying to say.
Be honest about what was ambiguous or misleading, and about what you understood only thanks to written words on screen. (Round ${round}.)`
}

function muteEvalPrompt(mute) {
  return `${CTX}
Compare what a first-time MUTED viewer (no captions, no script) understood from the full film of ${ID} with the INTENDED meaning. Read the storyboard ${SB}:
- its idees_cles: {id, idee, scenes}, plus principale when present;
- the scenes' texte and lecture_sans_son.
Score each idee_cle once, in storyboard order:
- GOT: understood as intended;
- PARTIAL: vague, incomplete, or understood only through written labels;
- MISSED: absent or wrong.
Quote the viewer's report as evidence.
Mark the main ideas (principale = true): those marked so in the storyboard. If none is marked, take the ideas that carry the video's thesis, its numbered steps and its closing line.
Then, for every idea that is not GOT, add a finding with a concrete visual fix in that idea's scenes:
- blocker if a main idea is MISSED;
- major if any idea is MISSED or a main idea is PARTIAL;
- minor otherwise.
MUTED VIEWER REPORT: ${JSON.stringify(mute)}`
}

function fixPrompt(round, serious, minors) {
  return `${CTX}
TASK: fix the film of ${ID} after review round ${round}.
Fix ALL the blocker and major findings below. When critics conflict, favour readability without captions and simplicity: that is the user's criterion.
${JSON.stringify(serious, null, 1)}
Fix these minors when cheap and safe:
${JSON.stringify(minors, null, 1)}
Then:
1. "make story-props ID=${ID}" must stay clean: no missing beats, no kit warnings.
2. Take stills around every change ('make story-stills ID=${ID} FRAMES="..."') and LOOK at them.
3. Re-render: "make story ID=${ID}".
4. Regenerate the sheets: "make review-sheets ID=${ID}" and 'make review-sheets ID=${ID} REVIEW="--nocap --sheets --phone"', then "make clean-tmp".
5. Read the sheets around each change to confirm each fix.
Report, per finding, what you changed, or why not.`
}

function qaPrompt() {
  return `${CTX}
TASK (QA): run "make qa ID=${ID}" in ${ROOT}: story mode, about 2 min. Read ${SKILL}/references/qa-checklist.md.
If every check passes, report them.
If a check fails:
- fix its cause in the staging. Never loosen a threshold or edit config.yaml: a longer maximum duration needs the user's approval, so report it;
- re-render with "make story ID=${ID}", which re-runs QA;
- regenerate 'make review-sheets ID=${ID} REVIEW="--nocap --sheets --phone"', then "make clean-tmp".
Make one fix attempt only. Report every check with its final value.`
}

function muteFixPrompt(mv) {
  return `${CTX}
TASK: the final mute check of ${ID} is below the threshold: at least 85 % of idees_cles GOT, no main idea MISSED, and "oui" to the user's criterion.
Make ONE targeted fix round on the scenes of the ideas that are not GOT. Make the visible action carry the meaning:
- a clearer visual verb;
- a stronger before/after;
- a longer hold on the key moment;
- fewer competing elements.
Keep the thread and the cast.
Mute check result: ${JSON.stringify(mv).slice(0, 8000)}
Then:
- "make story-props ID=${ID}" must be clean;
- take stills around each change;
- re-render with "make story ID=${ID}";
- regenerate "make review-sheets ID=${ID}" and 'make review-sheets ID=${ID} REVIEW="--nocap --sheets --phone"', then "make clean-tmp".
Report per weak point what you changed.`
}

const safe = (p) => p.catch((e) => { log(`agent failed: ${String((e && e.message) || e).slice(0, 200)}`); return null })

async function review(round, b) {
  const muteChain = safe(agent(mutePrompt(round), { label: `r${round}:mute-viewer`, phase: 'Review', schema: MUTE_VIEW }))
    .then((m) => (m
      ? safe(agent(muteEvalPrompt(m), { label: `r${round}:mute-eval`, phase: 'Review', schema: MUTE_EVAL })).then((e) => ({ m, e }))
      : { m: null, e: null }))
  const critics = CRITICS.map(([lens, brief]) =>
    safe(agent(criticPrompt(round, b, lens, brief), { label: `r${round}:${lens}`, phase: 'Review', schema: FINDINGS }))
      .then((r) => (r ? { ...r, lens } : null)))
  const [mm, ...crit] = await Promise.all([muteChain, ...critics])
  const reviews = [mm.e ? { ...mm.e, lens: 'mute-eval' } : null, ...crit].filter(Boolean)
  return { mute: mm.m, scores: mm.e ? mm.e.scores : [], reviews }
}

async function runMuteVerify() {
  try {
    return await workflow({ scriptPath: MUTE_VERIFY }, { id: ID, root: ROOT, repo: REPO })
  } catch (e) {
    log(`mute-verify not run from here (${String((e && e.message) || e).slice(0, 160)}): run ${MUTE_VERIFY} next with {id: "${ID}", root: "${ROOT}"}`)
    return null
  }
}

// ---------- run ----------
let cast = null
let build = null
const partReports = []

if (FROM === 'start') {
  phase('Prepare')
  cast = await safe(agent(castPrompt(), { label: 'cast', phase: 'Prepare', schema: CAST }))
  if (!cast || !cast.ok) {
    const problems = cast ? cast.problems : ['cast agent failed']
    log(`${ID}: not ready for staging: ${problems.join('; ').slice(0, 300)}`)
    return { id: ID, ok: false, stage: 'prepare', problems, status: {} }   // nothing written: the status stays as it was
  }
  log(`${ID}: ${cast.parts.length} parts, ${cast.cast_ids.length} cast entities, ${cast.new_entities.length} new entity types`)
  if (cast.new_entities.length) {
    const ent = await safe(agent(entitiesPrompt(cast.new_entities), { label: 'entities', phase: 'Prepare', schema: SIMPLE }))
    if (!ent || !ent.ok) log(`${ID}: new entities incomplete: ${ent ? ent.notes.slice(0, 200) : 'agent failed'}`)
  }

  phase('Author')
  const reports = await parallel(cast.parts.map((p, i) => () =>
    safe(agent(authorPrompt(p, cast.parts[i + 1]), { label: `author:${p.name}`, phase: 'Author', schema: PART_REPORT }))))
  cast.parts.forEach((p, i) => partReports.push(reports[i] || { ok: false, part: p.name, scene_by_scene: '', known_issues: ['author failed: write this part'] }))
  const weak = partReports.filter((r) => !r.ok).map((r) => r.part)
  if (weak.length) log(`${ID}: parts to finish at integration: ${weak.join(', ')}`)

  phase('Integrate')
  build = await safe(agent(integratePrompt(cast, partReports), { label: 'integrate', phase: 'Integrate', schema: BUILD_REPORT }))
  if (!build || !build.ok) {
    log(`${ID}: the full film did not render`)
    return { id: ID, ok: false, stage: 'integrate', cast, parts: partReports, build, status: { spec: 'partial', render: 'fail', review: 'pending', mute_verify: 'pending', qa: 'pending' } }
  }
} else if (FROM === 'review') {
  phase('Integrate')
  build = await safe(agent(inspectPrompt(), { label: 'inspect', phase: 'Integrate', schema: BUILD_REPORT }))
  if (!build || !build.ok) {
    return { id: ID, ok: false, stage: 'inspect', build, status: { render: 'pending' } }   // no rendered film to review
  }
}

const rounds = []
if (FROM !== 'verify') {
  for (let round = 1; round <= MAX_ROUNDS; round++) {
    phase('Review')
    const { mute, scores, reviews } = await review(round, build)
    const tag = (r) => (f) => ({ lens: r.lens, ...f })
    const serious = reviews.flatMap((r) => r.findings.filter((f) => f.severity !== 'minor').map(tag(r)))
    const minors = reviews.flatMap((r) => r.findings.filter((f) => f.severity === 'minor').map(tag(r)))
    const got = scores.filter((s) => s.score === 'GOT').length
    rounds.push({
      round,
      mute_message: mute ? mute.message : null,
      idees_got: `${got}/${scores.length}`,
      verdicts: reviews.map((r) => ({ lens: r.lens, verdict: r.verdict })),
      serious,
      minors,
    })
    log(`${ID} round ${round}: ${serious.length} blocker/major, ${minors.length} minor, idées-clés ${got}/${scores.length} GOT`)
    if (serious.length === 0) break
    phase('Fix')
    const fixed = await safe(agent(fixPrompt(round, serious, minors), { label: `fix-r${round}`, phase: 'Fix', schema: BUILD_REPORT }))
    if (fixed) build = fixed
    else log(`${ID}: fix round ${round} failed; the film is unchanged`)
  }
}

phase('Verify')
let qa = await safe(agent(qaPrompt(), { label: 'qa', phase: 'Verify', schema: QA_REPORT }))
let mv = VERIFY ? await runMuteVerify() : null
// mute-verify returns {ran: false, problem} when it could not score (no sheets, no idees_cles, evaluator failed):
// that is not a failed check, and a blind fix round would change the film for nothing.
if (mv && !mv.ran) log(`${ID}: mute check did not run: ${mv.problem || 'unknown reason'}`)
if (mv && mv.ran && !mv.pass) {
  phase('Fix')
  const fixed = await safe(agent(muteFixPrompt(mv), { label: 'fix-mute', phase: 'Fix', schema: BUILD_REPORT }))
  if (fixed) build = fixed
  phase('Verify')
  qa = await safe(agent(qaPrompt(), { label: 'qa-2', phase: 'Verify', schema: QA_REPORT }))
  mv = await runMuteVerify()
}

const last = rounds[rounds.length - 1]
const unfixed = ((build && build.fixes) || []).filter((f) => !f.done).map((f) => f.finding)
const openIssues = [
  ...unfixed,
  ...((last && last.serious.length && !(build && build.fixes)) ? last.serious.map((f) => `${f.lens}: ${f.problem}`) : []),
  ...(qa && !qa.ok ? qa.failed.map((c) => `QA: ${c}`) : []),
  ...(mv && mv.ran && !mv.pass ? (mv.points_faibles || []).map((p) => `sans son : ${p}`) : []),
  ...(mv && !mv.ran ? [`sans son : contrôle non fait (${mv.problem || 'raison inconnue'}) ; relancer mute-verify.wf.js`] : []),
  ...((build && build.known_issues) || []),
]
const qaState = qa ? (qa.ok ? 'done' : 'fail') : 'pending'
const mvState = mv && mv.ran ? (mv.pass ? 'done' : 'fail') : 'pending'
const reviewState = !last ? 'pending' : last.serious.length === 0 ? 'done' : unfixed.length ? 'open' : 'fixed'
// from "verify": the film was rendered earlier; QA ("Rendu Story à jour") checks that it matches the current sources.
const rendered = FROM === 'verify' || !!(build && build.ok)
// Status to merge as is (status.py merge): only the stages this run actually did. A run from "verify" leaves spec,
// render and review as they were and APPENDS its issues (open_issues_add), so the review's open issues survive.
const status = {}
if (FROM === 'start') status.spec = 'done'
if (FROM !== 'verify') {
  status.render = rendered ? 'done' : 'fail'
  status.review = reviewState
}
status.qa = qaState
if (mv && mv.ran) status.mute_verify = { state: mvState, got: `${mv.got}/${mv.total}`, critere: mv.critere_oui ? 'oui' : 'non' }
else if (FROM !== 'verify') status.mute_verify = 'pending'   // a new render voids an earlier mute check
if (FROM === 'verify') status.open_issues_add = openIssues
else status.open_issues = openIssues
return {
  id: ID,
  ok: rendered && qaState === 'done' && (mvState === 'done' || (!VERIFY && mvState === 'pending')),
  status,
  outputs: { mp4: OUT, nocap: NOCAP, review: REV, review_nocap: REV_NOCAP },
  parts: partReports.map((r) => ({ part: r.part, ok: r.ok, issues: r.known_issues })),
  rounds: rounds.map((r) => ({ round: r.round, idees_got: r.idees_got, verdicts: r.verdicts, serious: r.serious.length, minors: r.minors.length, mute_message: r.mute_message })),
  qa,
  mute_verify: mv,
  next: mvState === 'pending' && VERIFY ? `run ${MUTE_VERIFY} with {id: "${ID}", root: "${ROOT}"}` : null,
  open_issues: openIssues,
}
