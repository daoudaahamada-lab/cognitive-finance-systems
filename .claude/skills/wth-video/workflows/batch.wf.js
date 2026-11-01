export const meta = {
  name: 'wth-video-batch',
  description: 'Produce several WealthTech Horizon Story films in a row: preflight, storyboard (the next one prepared ahead), build + reviews, final mute check with one targeted fix round, status, clean-up and optional commit per video',
  whenToUse: 'Unattended production of several WTH videos whose voice is final (skill wth-video, batch mode). Never generates voices. args: {ids: ["V02","V03"], root: "<repo>/wth-videos", stages?: ["storyboard","build","verify"], lookahead?: 1, notes?: {V02: "..."}, revise?: {V01: {notes: [...], scenes?, version?}}, from?: {V02: "review"}, parts?: 3 | {V02: 3}, maxRounds?: 2, muteRounds?: 1, commit?: "<attribution lines>", allowBeforeV01?: false}',
  phases: [
    { title: 'Preflight', detail: 'status, V01 checkpoint and preflight of every video; safe fixes only (make voice, clean-tmp, illustrations)' },
    { title: 'Storyboard', detail: 'wth-storyboard workflows; the next video is prepared while the current one is built' },
    { title: 'Build', detail: 'wth-story-build/build-review.wf.js with verify: false' },
    { title: 'Verify', detail: 'wth-story-build/mute-verify.wf.js; below threshold: one targeted fix, QA, second check' },
    { title: 'Record', detail: 'production_status.json, clean-up, optional commit and push' },
  ],
}

// ---------- parameters ----------
// args: { ids: ['V02', 'V03'] (or "V02 V03"), root: '/abs/.../wth-videos',
//         stages?: ['storyboard', 'build', 'verify']   (default: all three; voices are never made here),
//         lookahead?: 1        (1: the next storyboard runs while the current film is built; 0: strictly one at a time),
//         notes?: {V07: '…'}   (per-video instructions for storyboard.wf.js),
//         revise?: {V01: {notes: ['…'], scenes?: ['S11'], version?: 'v3'}}   (revise an existing storyboard),
//         from?: {V07: 'start' | 'review' | 'verify' | 'done'}   (override the status-driven start of the build),
//         parts?: 3 | {V07: 3 | [['S01','S06'], …]},  maxRounds?: 2,  muteRounds?: 1,
//         commit?: '<the session attribution lines>'   (given: each step is committed and pushed; absent: no commit),
//         allowBeforeV01?: false   (true only if the user explicitly asked to start before approving V01),
//         repo?: repository root (default: root without /wth-videos) }
const A = args && typeof args === 'object' ? args : {}
const IDS = Array.isArray(A.ids) ? A.ids.map(String) : typeof A.ids === 'string' ? A.ids.split(/[\s,]+/).filter(Boolean) : []
if (!IDS.length || !A.root) {
  throw new Error('batch.wf.js: args {ids: ["V02", "V03"], root: "/abs/path/wth-videos"} are required')
}
const BAD = IDS.filter((id) => !/^V\d{2,3}$/.test(id))
if (BAD.length) throw new Error(`batch.wf.js: invalid video ids ${BAD.join(', ')} (expected "V07")`)
const ROOT = String(A.root).replace(/\/+$/, '')
const REPO = A.repo ? String(A.repo).replace(/\/+$/, '') : ROOT.replace(/\/wth-videos$/, '')
const SK = `${REPO}/.claude/skills`
const WF = {
  storyboard: `${SK}/wth-storyboard/workflows/storyboard.wf.js`,
  revise: `${SK}/wth-storyboard/workflows/revise.wf.js`,
  build: `${SK}/wth-story-build/workflows/build-review.wf.js`,
  verify: `${SK}/wth-story-build/workflows/mute-verify.wf.js`,
}
const STATUS = `python3 ${SK}/wth-video/scripts/status.py`
const PREFLIGHT = `python3 ${SK}/wth-video/scripts/preflight.py`
const ALL_STAGES = ['storyboard', 'build', 'verify']
const STAGES = Array.isArray(A.stages) && A.stages.length ? A.stages.filter((s) => ALL_STAGES.includes(s)) : ALL_STAGES
const LOOKAHEAD = A.lookahead === 0 || A.lookahead === false ? 0 : 1
const COMMIT = typeof A.commit === 'string' && A.commit.trim() ? A.commit.trim() : null
const PASSED = ['done', 'fixed', 'open', 'skipped']
const per = (key, id) => {
  const v = A[key]
  return v && typeof v === 'object' && !Array.isArray(v) ? v[id] : undefined
}
const partsFor = (id) => {
  const p = per('parts', id)
  if (p !== undefined) return p
  return Number.isInteger(A.parts) ? A.parts : undefined
}

const CTX = `
CONTEXT
- Repository ${REPO}; video pipeline ${ROOT} (run make and "python3 -m pipeline..." from there). "WealthTech Horizon" is a faceless French finance media; its vertical films use the Story method validated by the user on V01.
- You are one step of the batch workflow of the skill ${SK}/wth-video (its SKILL.md has the context if you need it).
- Production status: ${ROOT}/scripts/production_status.json. Change it ONLY through ${STATUS} (schema: ${SK}/wth-video/references/status-schema.md).
- Hard rules:
  - never generate a voice and never call ElevenLabs: credits need a human check;
  - render only through make or "python3 -m pipeline.story" (one Remotion render at a time, build/.render.lock); never delete the lock;
  - never commit MP4s, build/ or cache/tts here; never touch config.yaml, scripts/scripts.json, Cloudinary, Metricool;
  - keep 4 GB of free disk ("make clean-tmp").
`

// ---------- schemas ----------
const PRE = {
  type: 'object',
  properties: {
    v01_approved: { type: 'boolean', description: 'checkpoints.v01_full_approved.state == "done"' },
    env_ok: { type: 'boolean', description: 'no blocking environment check left (Remotion, browser, tools, disk)' },
    env_blocking: { type: 'array', items: { type: 'string' } },
    fixed: { type: 'array', items: { type: 'string' } },
    videos: { type: 'array', items: { type: 'object', properties: {
      id: { type: 'string' },
      ready: { type: 'boolean', description: 'voice cached and prepared, nothing blocking left' },
      voice: { type: 'boolean' },
      storyboard: { type: 'string', enum: ['absent', 'ok', 'refused'] },
      storyboard_version: { type: 'string' },
      storyboard_pending: { type: 'string', description: 'the "pending" text of the storyboard stage, or ""' },
      stages: { type: 'object', properties: {
        storyboard: { type: 'string' }, spec: { type: 'string' }, render: { type: 'string' }, review: { type: 'string' },
        mute_verify: { type: 'string' }, qa: { type: 'string' } } },
      blocking: { type: 'array', items: { type: 'string' } } },
      required: ['id', 'ready', 'voice', 'storyboard', 'stages', 'blocking'] } },
  },
  required: ['v01_approved', 'env_ok', 'fixed', 'videos'],
}
const REC = {
  type: 'object',
  properties: {
    status_updated: { type: 'boolean' },
    cleaned: { type: 'boolean' },
    committed: { type: 'boolean' },
    commit: { type: 'string', description: 'short sha, or ""' },
    pushed: { type: 'boolean' },
    notes: { type: 'string' },
  },
  required: ['status_updated', 'committed', 'notes'],
}
const FIX = {
  type: 'object',
  properties: {
    ok: { type: 'boolean', description: 'true if the film was re-rendered with the fixes' },
    changes: { type: 'array', items: { type: 'object', properties: { point: { type: 'string' }, change: { type: 'string' } }, required: ['point', 'change'] } },
    notes: { type: 'string' },
  },
  required: ['ok', 'changes', 'notes'],
}

// ---------- helpers ----------
async function safe(p) {
  try {
    return await p
  } catch (e) {
    log(`agent failed: ${String((e && e.message) || e).slice(0, 200)}`)
    return null
  }
}

async function sub(label, path, a) {
  try {
    const r = await workflow({ scriptPath: path }, a)
    return r || { ok: false, error: `${label}: empty result` }
  } catch (e) {
    const msg = String((e && e.message) || e).slice(0, 300)
    log(`${a.id}: ${label} workflow failed: ${msg}`)
    return { ok: false, error: msg }
  }
}

function sourcePaths(id) {
  return [
    `wth-videos/scripts/storyboards/${id}.json`, `wth-videos/scripts/storyboards/${id}.md`,
    `wth-videos/scripts/story/${id}`, `wth-videos/scripts/story/${id}.py`,
    'wth-videos/motion/src/story', 'wth-videos/pipeline', 'wth-videos/tests',
    `wth-videos/output/qa/${id}.json`, 'wth-videos/output/qa_report.md',
    'wth-videos/scripts/production_status.json',
    '.claude/skills/wth-story-build/references', '.claude/skills/wth-storyboard/references',
  ]
}

function recordPrompt(id, label, update, opts) {
  const commit = COMMIT && opts.paths
    ? `3. Commit and push this step (commit policy of the skill wth-video):
   - run "git -C ${REPO} status --short";
   - stage ONLY changed or new paths among: ${opts.paths.join(', ')}. Never build/, never *.mp4, never cache/tts;
   - if nothing is staged, do not commit;
   - otherwise commit with exactly this message (title, blank line, then the attribution lines verbatim):
${opts.message}

${COMMIT}
   - push the current branch: "git -C ${REPO} push -u origin HEAD"; on a network error retry up to 4 times, waiting 2, 4, 8 then 16 s. If git says .git/index.lock exists, another step is committing: wait 10 s and retry.`
    : '3. Do not commit (the session commits after the batch).'
  return `${CTX}
TASK (record "${label}" for ${id}), from ${REPO}:
1. Update the production status with exactly this command:
${STATUS} merge ${id} - <<'EOF'
${JSON.stringify(update)}
EOF
   Then run "${STATUS} show ${id}" and check the result.
2. ${opts.clean ? `Clean up in ${ROOT}: "make clean-tmp ID=${id}" (keeps the review sheets)${opts.finished ? `, then "rm -rf build/${id}/story/stills && rm -f build/${id}/story/muet_*.mp4"` : ''}; report "df -h ." free space.` : 'No clean-up in this step.'}
${commit}
Report what you did.`
}

async function record(id, label, update, opts) {
  return safe(agent(recordPrompt(id, label, update, opts), { label: `record:${id}:${label}`, phase: 'Record', schema: REC, effort: 'low' }))
}

function muteFixPrompt(id, mv) {
  return `${CTX}
TASK: the final mute check of ${id} is below the threshold: at least 85 % of idees_cles GOT, no main idea MISSED, and "oui" to the user's criterion « en masquant les sous-titres, je dois pouvoir comprendre l’action principale et percevoir ce qui change ».
Follow ${SK}/wth-story-build/SKILL.md (procedure steps 3 to 9; references/review-lenses.md, kit.md and troubleshooting.md as needed).
Make ONE targeted fix round on the scenes of the ideas that are not GOT: a clearer visual verb, a stronger before/after, a visible cause, a longer hold on the key moment, fewer competing elements. Keep the thread, the cast, the storyboard texts, idees_cles and scene boundaries.
Mute check result: ${JSON.stringify(mv).slice(0, 8000)}
Then:
- "make story-props ID=${id}" must be clean (no missing beat, no unstaged scene, no kit warning);
- take stills around each change ("make story-stills ID=${id} FRAMES=...") and look at them;
- re-render with "make story ID=${id}" (it re-runs QA; read its table);
- regenerate 'make review-sheets ID=${id} REVIEW="--nocap --sheets --phone"', then "make clean-tmp".
Do not commit. Report per weak point what you changed.`
}

function planFor(v) {
  const st = v.stages || {}
  let sb = 'skip'
  let sbReason = ''
  if (STAGES.includes('storyboard')) {
    if (v.storyboard === 'absent') sb = 'write'
    else if (per('revise', v.id)) sb = 'revise'
    else if (v.storyboard === 'refused') {
      sb = 'stop'
      sbReason = `storyboard existant refusé par --check${v.storyboard_pending ? ` (reste : ${v.storyboard_pending})` : ''} : relance avec revise: {${v.id}: {notes: [...]}}`
    }
  } else if (v.storyboard !== 'ok' && STAGES.includes('build')) {
    sb = 'stop'
    sbReason = `pas de storyboard valide (${v.storyboard}) et l’étape storyboard n’est pas demandée`
  }
  const forced = per('from', v.id)
  let from = forced
  if (!from) {
    if (sb === 'write' || sb === 'revise') from = 'start'
    else if (st.render !== 'done') from = 'start'
    else if (!PASSED.includes(st.review)) from = 'review'
    else if (st.qa !== 'done') from = 'verify'
    else from = 'done'
  }
  const build = STAGES.includes('build') && from !== 'done' ? from : 'skip'
  const verify = STAGES.includes('verify') && (build !== 'skip' || st.mute_verify !== 'done') ? 'run' : 'skip'
  return { sb, sbReason, build, verify }
}

// ---------- preflight ----------
phase('Preflight')
const pre = await safe(agent(`${CTX}
TASK (preflight of a batch): videos ${IDS.join(', ')}. Work from ${REPO}.
1. Run "${STATUS} init" (idempotent), then "${STATUS} show ${IDS.join(' ')} --json". Report v01_approved = (checkpoints.v01_full_approved.state == "done"), and for each video the state of its stages storyboard, spec, render, review, mute_verify, qa, plus the "pending" text of the storyboard stage if any.
2. Run "${PREFLIGHT} ${IDS.join(' ')} --json".
3. Fix ONLY what is safe and mechanical, then run the preflight again:
   - "voix préparée" missing or stale: "make voice ID=Vxx" in ${ROOT} (no network: the voice is in the cache);
   - illustrations missing or truncated: download each with the Google Drive connector tool download_file_content (fileId = drive_id in ${ROOT}/data/illustrations_manifest.tsv). The result is too big and is saved to a file: decode it with "python3 -I ${SK}/wth-video/scripts/drive_decode.py <saved file> <file name>" (procedure: ${SK}/wth-video/references/environment.md). Never read or print the base64 yourself;
   - Remotion node_modules missing: "make motion-setup" in ${ROOT};
   - disk below 4 GB: "make clean-tmp", then "make clean-tmp ID=Vxx" for videos whose qa stage is done.
   Fix nothing else. A video whose voice is not in the cache is NOT ready: never generate a voice.
4. For each video report: voice (cached and prepared), storyboard ("absent"; "ok" if it exists and --check passes; "refused" if it exists and --check fails), storyboard_version, the stage states, blocking = what still blocks after your fixes (short French phrases), ready = voice && nothing blocking.`, { label: 'preflight', phase: 'Preflight', schema: PRE, effort: 'low' }))

if (!pre) return { ok: false, stage: 'preflight', message: 'preflight agent failed: run preflight.py by hand' }
if (!pre.env_ok) {
  log(`environment not ready: ${(pre.env_blocking || []).join('; ')}`)
  return { ok: false, stage: 'preflight', env_blocking: pre.env_blocking || [], fixed: pre.fixed }
}
if (IDS.some((id) => id !== 'V01') && !pre.v01_approved && A.allowBeforeV01 !== true) {
  return {
    ok: false,
    stage: 'checkpoint',
    message: 'V01 complète pas encore validée par l’utilisateur : envoie-lui V01 (avec et sans sous-titres), attends son accord, puis « status.py checkpoint v01_full_approved done ». allowBeforeV01: true seulement à sa demande explicite.',
  }
}

const byId = {}
for (const v of pre.videos || []) byId[v.id] = v
const results = []
const queue = []
for (const id of IDS) {
  const v = byId[id]
  if (!v) {
    results.push({ id, ok: false, skipped: 'absente du rapport de préflight' })
    continue
  }
  if (!v.ready) {
    results.push({ id, ok: false, skipped: v.voice ? `bloquée : ${v.blocking.join('; ')}` : 'voix absente : recette voix du skill wth-video (hors lot, crédits à vérifier)' })
    continue
  }
  const p = planFor(v)
  log(`${id}: storyboard ${p.sb}, build ${p.build}, verify ${p.verify}`)
  queue.push({ v, p })
}
if (pre.fixed && pre.fixed.length) log(`preflight fixed: ${pre.fixed.join('; ').slice(0, 300)}`)

// ---------- storyboard (memoised: the next video's storyboard starts while the current film is built) ----------
const sbRuns = {}
function storyboardStage(v, p) {
  if (!(v.id in sbRuns)) sbRuns[v.id] = runStoryboard(v, p)
  return sbRuns[v.id]
}
async function runStoryboard(v, p) {
  const id = v.id
  if (p.sb === 'skip') return { ok: v.storyboard === 'ok' || !STAGES.includes('build'), skipped: true, version: v.storyboard_version }
  if (p.sb === 'stop') return { ok: false, reason: p.sbReason }
  const res = p.sb === 'write'
    ? await sub('storyboard', WF.storyboard, { id, root: ROOT, repo: REPO, notes: per('notes', id), muteRounds: A.muteRounds })
    : await sub('revise', WF.revise, { id, root: ROOT, repo: REPO, ...per('revise', id) })
  const ok = Boolean(res && res.ok)
  const scores = (res && (res.test_sans_son ? res.test_sans_son.idees : res.scores)) || []
  const got = scores.filter((s) => s && s.score === 'GOT').length
  const update = {
    storyboard: ok
      ? { state: 'done', version: res.version || '', note: `${p.sb === 'write' ? 'écrit' : 'révisé'} par le lot ; test muet ${got}/${scores.length} idées GOT` }
      : { state: 'fail', note: String((res && (res.reason || res.error || (res.check && res.check.check_output))) || 'échec du workflow').slice(0, 300) },
  }
  const rec = await record(id, 'storyboard', update, {
    paths: ok ? [`wth-videos/scripts/storyboards/${id}.json`, `wth-videos/scripts/storyboards/${id}.md`, 'wth-videos/scripts/production_status.json'] : null,
    message: `${id} : storyboard ${res && res.version ? res.version.split(' ')[0] : ''} (méthode Story, lot)`,
  })
  log(`${id}: storyboard ${ok ? 'OK' : 'FAILED'}${ok ? ` (${res.version || ''}, test muet ${got}/${scores.length})` : ''}`)
  return {
    ok,
    version: res && res.version,
    mute: `${got}/${scores.length}`,
    resume_fr: res && res.check ? res.check.resume_fr : null,
    alerts_left: res && res.check ? res.check.alerts_left || [] : [],
    reason: ok ? null : update.storyboard.note,
    committed: Boolean(rec && rec.committed),
  }
}

// ---------- one video after the other ----------
for (let i = 0; i < queue.length; i++) {
  const { v, p } = queue[i]
  const id = v.id
  phase('Storyboard')
  const sb = await storyboardStage(v, p)
  if (LOOKAHEAD && i + 1 < queue.length) storyboardStage(queue[i + 1].v, queue[i + 1].p)
  if (!sb.ok) {
    results.push({ id, ok: false, stage: 'storyboard', storyboard: sb, open_issues: [sb.reason || 'storyboard en échec'] })
    continue
  }

  // ---- build + reviews + QA (the mute check runs below: a child workflow cannot start another one) ----
  let build = { skipped: true }
  if (p.build !== 'skip') {
    phase('Build')
    build = await sub('build-review', WF.build, {
      id, root: ROOT, repo: REPO, parts: partsFor(id), maxRounds: A.maxRounds, verify: false, from: p.build,
    })
    log(`${id}: build ${build.ok ? 'OK' : 'not OK'} (${JSON.stringify(build.status || {})})`)
  }
  const rendered = build.skipped ? (v.stages || {}).render === 'done' : Boolean(build.status && build.status.render === 'done')

  // ---- final mute check, one targeted fix round if below threshold ----
  let mv = null
  let firstMv = null
  let muteFix = null
  let qa2 = null
  if (p.verify === 'run' && rendered) {
    phase('Verify')
    mv = await sub('mute-verify', WF.verify, { id, root: ROOT, repo: REPO })
    if (mv && mv.ran && !mv.pass) {
      firstMv = mv
      log(`${id}: mute check below threshold (${mv.got}/${mv.total}), one targeted fix round`)
      muteFix = await safe(agent(muteFixPrompt(id, mv), { label: `fix-mute:${id}`, phase: 'Verify', schema: FIX }))
      qa2 = await sub('qa', WF.build, { id, root: ROOT, repo: REPO, from: 'verify', verify: false })
      mv = await sub('mute-verify', WF.verify, { id, root: ROOT, repo: REPO })
    }
  } else if (p.verify === 'run') {
    log(`${id}: no rendered film, mute check skipped`)
  }

  // ---- record ----
  if (build.skipped && !mv && sb.skipped) {
    const st = v.stages || {}
    const finishedBefore = st.render === 'done' && st.qa === 'done' && (st.mute_verify === 'done' || !STAGES.includes('verify'))
    results.push({ id, ok: finishedBefore, skipped: finishedBefore ? 'déjà terminée (rien à refaire)' : 'rien à faire avec les étapes demandées', outputs: { mp4: `${ROOT}/output/WTH-${id}.mp4`, nocap: `${ROOT}/build/${id}/story/film_sans_sous_titres.mp4` }, open_issues: [] })
    continue
  }
  phase('Record')
  const update = {}
  const bs = build.status || {}
  for (const k of ['spec', 'render', 'review', 'qa']) if (bs[k]) update[k] = bs[k]
  if (qa2 && qa2.status && qa2.status.qa) update.qa = qa2.status.qa
  if (mv && mv.ran) {
    update.mute_verify = {
      state: mv.pass ? 'done' : 'fail',
      got: `${mv.got}/${mv.total}`,
      critere: mv.critere_oui ? 'oui' : 'non',
      note: mv.pass ? (firstMv ? 'réussi après un tour de correction ciblé' : '') : `sous le seuil après ${firstMv ? 'un tour de correction' : 'le premier contrôle'} : à remonter à l’utilisateur`,
    }
  } else if (!build.skipped && build.status && build.status.mute_verify) {
    update.mute_verify = build.status.mute_verify   // 'pending' after a new render; absent after a QA-only run
  }
  const openIssues = [
    ...(build.error ? [`build-review en échec : ${build.error}`] : []),
    ...((build.problems || []).map(String)),
    ...((build.open_issues || []).map(String)),
    ...((qa2 && qa2.open_issues) || []).map(String),
    ...(mv && mv.ran && !mv.pass ? (mv.points_faibles || []).map((x) => `sans son : ${x}`) : []),
  ].slice(0, 30)
  // A film built or reviewed again replaces the open issues; a QA-only run ('verify') or a mute check alone adds to
  // them, so the issues the review left open are not lost (status.py merge: open_issues vs open_issues_add).
  if (!build.skipped && p.build !== 'verify') update.open_issues = openIssues
  else if ((!build.skipped || (mv && mv.ran)) && openIssues.length) update.open_issues_add = openIssues
  const qaState = update.qa || (v.stages || {}).qa
  const muteState = update.mute_verify ? (typeof update.mute_verify === 'string' ? update.mute_verify : update.mute_verify.state) : (v.stages || {}).mute_verify
  const finished = rendered && qaState === 'done' && (muteState === 'done' || !STAGES.includes('verify'))
  const rec = await record(id, 'film', update, {
    clean: true,
    finished,
    paths: sourcePaths(id),
    message: `${id} : film Story (mise en scène, revues, QA${muteState === 'done' ? ', contrôle sans son' : ''})`,
  })
  const res = {
    id,
    ok: finished,
    storyboard: { version: sb.version, mute: sb.mute, resume_fr: sb.resume_fr, skipped: Boolean(sb.skipped) },
    build: build.skipped ? { skipped: true } : { ok: build.ok, status: build.status, rounds: build.rounds, error: build.error },
    qa: qa2 && qa2.qa ? qa2.qa : build.qa || null,
    mute_verify: mv && mv.ran ? { pass: mv.pass, got: mv.got, total: mv.total, critere_oui: mv.critere_oui, critere: mv.critere, missed_main: mv.missed_main } : null,
    first_mute_verify: firstMv ? { got: firstMv.got, total: firstMv.total, points_faibles: firstMv.points_faibles } : null,
    mute_fix: muteFix ? muteFix.changes : null,
    open_issues: openIssues,
    outputs: { mp4: `${ROOT}/output/WTH-${id}.mp4`, nocap: `${ROOT}/build/${id}/story/film_sans_sous_titres.mp4` },
    committed: Boolean(rec && rec.committed),
    commit: rec && rec.commit,
  }
  log(`${id}: ${finished ? 'FINISHED' : 'not finished'}${res.mute_verify ? `, mute ${res.mute_verify.got}/${res.mute_verify.total}` : ''}, ${openIssues.length} open issue(s)`)
  results.push(res)
}

results.sort((a, b) => IDS.indexOf(a.id) - IDS.indexOf(b.id))
const done = results.filter((r) => r.ok && !r.skipped)
return {
  ok: results.length > 0 && results.every((r) => r.ok),
  ids: IDS,
  results,
  deliver: done.map((r) => ({ id: r.id, mp4: r.outputs.mp4, nocap: r.outputs.nocap })),
  next: [
    done.length ? `Livrer ${done.map((r) => r.id).join(', ')} (SendUserFile + légende et hashtags de scripts.json), puis status.py set Vxx delivered done.` : null,
    COMMIT ? null : 'Commiter et pousser les sources de chaque vidéo (politique de commit du skill wth-video).',
    results.some((r) => !r.ok) ? `À reprendre : ${results.filter((r) => !r.ok).map((r) => r.id).join(', ')} (status.py next).` : null,
  ].filter(Boolean),
}
