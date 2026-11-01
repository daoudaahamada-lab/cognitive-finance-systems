export const meta = {
  name: 'wth-mute-verify',
  description: 'Final mute check of a WealthTech Horizon film: independent first-time viewers watch the no-caption film through its review sheets, then an evaluator scores each storyboard idee_cle GOT/PARTIAL/MISSED and answers the user criterion',
  whenToUse: 'After the full Story film of a video is rendered (skill wth-story-build). args: {id: "V07", root: "<repo>/wth-videos", viewers?: 2, threshold?: 0.85}',
  phases: [
    { title: 'Prepare', detail: 'no-caption review sheets (phone + half resolution), idees_cles list' },
    { title: 'Mute test', detail: 'independent first-time viewers: no sound, no captions, no script' },
    { title: 'Evaluate', detail: 'score idees_cles, answer the criterion, weak points' },
  ],
}

// ---------- parameters ----------
const A = args && typeof args === 'object' ? args : {}
if (!A.id || !A.root) {
  throw new Error('mute-verify.wf.js: args {id: "V07", root: "/abs/path/wth-videos"} are required')
}
const ID = String(A.id)
const ROOT = String(A.root).replace(/\/+$/, '')
const REPO = A.repo ? String(A.repo).replace(/\/+$/, '') : ROOT.replace(/\/wth-videos$/, '')
const SKILL = `${REPO}/.claude/skills/wth-story-build`
const N_VIEWERS = Number.isInteger(A.viewers) && A.viewers >= 1 ? A.viewers : 2
const THRESHOLD = typeof A.threshold === 'number' ? A.threshold : 0.85
const SB = `${ROOT}/scripts/storyboards/${ID}.json`
const NOCAP = `${ROOT}/build/${ID}/story/film_sans_sous_titres.mp4`
const REV_NOCAP = `${ROOT}/build/${ID}/review/film_nocap`
const CRITERION = '« en masquant les sous-titres, je dois pouvoir comprendre l’action principale et percevoir ce qui change »'

// ---------- schemas ----------
const PREP = {
  type: 'object',
  properties: {
    ok: { type: 'boolean' },
    problem: { type: 'string' },
    film: { type: 'string' },
    duration_s: { type: 'number' },
    phone_sheets: { type: 'array', items: { type: 'string' } },
    sheets: { type: 'array', items: { type: 'string' } },
    idees: { type: 'array', items: { type: 'object', properties: {
      id: { type: 'string' }, idee: { type: 'string' }, scenes: { type: 'array', items: { type: 'string' } },
      principale: { type: 'boolean', description: 'as marked in the storyboard; false when the field is absent' } },
      required: ['id', 'idee', 'scenes', 'principale'] } },
    principale_marked: { type: 'boolean', description: 'true if the storyboard marks at least one idea principale' },
  },
  required: ['ok', 'phone_sheets', 'sheets', 'idees', 'principale_marked'],
}

const VIEW = {
  type: 'object',
  properties: {
    beats: { type: 'array', items: { type: 'object', properties: {
      t: { type: 'string' }, action: { type: 'string' }, acteurs: { type: 'string' }, changement: { type: 'string' } },
      required: ['t', 'action', 'changement'] } },
    message: { type: 'string', description: 'what the video is trying to say, 4-6 sentences' },
    ambiguites: { type: 'array', items: { type: 'string' } },
    lu_seulement: { type: 'array', items: { type: 'string' }, description: 'what was understood only thanks to written words on screen' },
  },
  required: ['beats', 'message', 'ambiguites'],
}

const EVAL = {
  type: 'object',
  properties: {
    scores: { type: 'array', items: { type: 'object', properties: {
      id: { type: 'string' }, idee: { type: 'string' }, principale: { type: 'boolean' },
      score: { type: 'string', enum: ['GOT', 'PARTIAL', 'MISSED'] },
      preuve: { type: 'string', description: 'in French, quoting the viewers' } },
      required: ['id', 'idee', 'principale', 'score', 'preuve'] } },
    critere_oui: { type: 'boolean' },
    critere_atteint: { type: 'string', description: 'in French: oui / non, with nuance' },
    points_faibles: { type: 'array', items: { type: 'object', properties: {
      scenes: { type: 'array', items: { type: 'string' } }, probleme: { type: 'string' }, correction: { type: 'string' } },
      required: ['scenes', 'probleme', 'correction'] } },
  },
  required: ['scores', 'critere_oui', 'critere_atteint', 'points_faibles'],
}

// ---------- prompts ----------
const prepPrompt = `Prepare the final mute check of the WealthTech Horizon film ${ID}. Work in ${ROOT}.
1. Check that build/${ID}/story_render.json and ${NOCAP} exist (the full film was rendered by "make story ID=${ID}"). If they are missing, return ok=false with the problem.
2. Regenerate the no-caption review outputs: 'make review-sheets ID=${ID} REVIEW="--nocap --sheets --phone"'. This takes about a minute and waits on the render lock if a render is running.
3. Return:
   - the sorted absolute paths of ${REV_NOCAP}/phone/phone_*.jpg and ${REV_NOCAP}/sheets/sheet_*.jpg;
   - the film duration (ffprobe);
   - from the storyboard ${SB}, the list of idees_cles {id, idee, scenes, principale}, with principale false when the field is absent, and whether any idea is marked principale.
Do not describe the film.`

function viewerPrompt(i, prep) {
  const order = i % 2 === 0
    ? 'First read the phone-size sheets, in order, to get the flow as a phone shows it. Then read the detail sheets, in order.'
    : 'First read the detail sheets, in order. Then read the phone-size sheets to check what still reads at phone size.'
  return `You are a first-time viewer of a short vertical video (${Math.round(prep.duration_s || 0)} s), muted and WITHOUT captions. You know nothing about its topic or its script beyond what you see.
Look ONLY at the images listed below. Do not open any other file of the repository: no storyboard, script, spec, props, report or other review folder. Reading them would invalidate the test.
- Phone-size sheets (2 images per second, 360 px wide, after platform-like compression): ${JSON.stringify(prep.phone_sheets)}
- Detail sheets (6 images per second, half resolution; each frame is labelled with a scene id, its time and its frame number): ${JSON.stringify(prep.sheets)}
${order}
Then:
- describe, beat by beat with timestamps: the main action, who acts (what each character or object seems to be), and what changes;
- say in 4-6 sentences what the video is trying to say;
- list what was ambiguous or misleading, and what you understood only thanks to written words on screen.
(Viewer ${i + 1}.)`
}

function evalPrompt(prep, viewers) {
  const mainRule = prep.principale_marked
    ? 'The main ideas are those marked principale = true.'
    : 'No idea is marked principale in the storyboard: mark as main the ideas that carry the thesis of the video, its numbered steps and its closing line, and say so in their preuve.'
  return `${viewers.length} independent first-time viewers watched the muted, caption-less film ${ID} of WealthTech Horizon, a French finance and wealth-tech explainer. Their reports are below.
The intended ideas (idees_cles of the storyboard ${SB}, in order) are: ${JSON.stringify(prep.idees)}
You may read the storyboard (scene texte, lecture_sans_son) to understand each idea; judge only from the viewers' reports.
Score EVERY idea once, with its id, from the viewers' combined reports:
- GOT: every viewer understood it as intended;
- PARTIAL: only one viewer got it, or the viewers got it vaguely, incompletely or only through written labels;
- MISSED: no viewer got it, or they read it wrongly.
Give the evidence in French, quoting the viewers. ${mainRule}
Then answer the user's success criterion: ${CRITERION}. Set critere_oui (true or false) and explain in French, with nuance.
Finally, list the remaining weak points as concrete visual fixes, in French, each with the scene ids it concerns.
VIEWERS: ${JSON.stringify(viewers)}`
}

// ---------- run ----------
phase('Prepare')
const prep = await agent(prepPrompt, { label: 'prepare', phase: 'Prepare', schema: PREP, effort: 'low' })
if (!prep || !prep.ok || !prep.sheets.length) {
  const problem = prep ? (prep.problem || 'no review sheets') : 'prepare agent failed'
  log(`${ID}: mute check not possible: ${problem}`)
  return { id: ID, pass: false, ran: false, problem }
}
if (!prep.idees.length) {
  log(`${ID}: the storyboard has no idees_cles: the mute check cannot be scored (make storyboard-check ID=${ID})`)
  return { id: ID, pass: false, ran: false, problem: 'idees_cles absent du storyboard' }
}

phase('Mute test')
const viewers = (await parallel(Array.from({ length: N_VIEWERS }, (_, i) => () =>
  agent(viewerPrompt(i, prep), { label: `viewer-${i + 1}`, phase: 'Mute test', schema: VIEW })))).filter(Boolean)
if (!viewers.length) {
  return { id: ID, pass: false, ran: false, problem: 'no viewer report' }
}
if (viewers.length < N_VIEWERS) log(`${ID}: only ${viewers.length}/${N_VIEWERS} viewers reported`)

phase('Evaluate')
const ev = await agent(evalPrompt(prep, viewers), { label: 'evaluate', phase: 'Evaluate', schema: EVAL })
if (!ev) {
  return { id: ID, pass: false, ran: false, problem: 'evaluator failed', viewers: viewers.map((v) => v.message) }
}

// Every idea of the storyboard is scored; an idea the evaluator skipped counts as MISSED.
const byId = {}
for (const s of ev.scores) byId[s.id] = s
const scores = prep.idees.map((idea) => {
  const s = byId[idea.id]
  if (!s) return { id: idea.id, idee: idea.idee, principale: idea.principale, score: 'MISSED', preuve: 'non notée par l’évaluateur' }
  return { ...s, principale: prep.principale_marked ? idea.principale : s.principale }
})
const skipped = prep.idees.filter((idea) => !byId[idea.id]).map((idea) => idea.id)
if (skipped.length) log(`${ID}: ideas not scored by the evaluator, counted as MISSED: ${skipped.join(', ')}`)

const total = scores.length
const got = scores.filter((s) => s.score === 'GOT').length
const ratio = total ? got / total : 0
const missedMain = scores.filter((s) => s.principale && s.score === 'MISSED').map((s) => s.id)
const pass = ratio >= THRESHOLD && missedMain.length === 0 && ev.critere_oui === true
log(`${ID}: ${got}/${total} GOT (${Math.round(ratio * 100)} %), main ideas missed: ${missedMain.join(', ') || 'none'}, critère : ${ev.critere_oui ? 'oui' : 'non'} -> ${pass ? 'PASS' : 'FAIL'}`)

return {
  id: ID,
  ran: true,
  pass,
  got,
  total,
  ratio: Math.round(ratio * 1000) / 1000,
  threshold: THRESHOLD,
  missed_main: missedMain,
  critere_oui: ev.critere_oui,
  critere: ev.critere_atteint,
  scores,
  points_faibles: ev.points_faibles.map((p) => `${(p.scenes || []).join(', ')} : ${p.probleme} -> ${p.correction}`),
  weak_points: ev.points_faibles,
  viewers: viewers.map((v) => v.message),
  sheets: REV_NOCAP,
}
