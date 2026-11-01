#!/usr/bin/env node
// Contrôle d'un modèle de workflow (.wf.js) sans l'exécuter :
//   node .claude/skills/wth-storyboard/scripts/check_wf.mjs <fichier.wf.js> [...]
// 1. le fichier commence par `export const meta = {...}`, un littéral pur (ni variable, ni appel, ni gabarit ${}) ;
// 2. le corps compile comme le fait le moteur de workflows (corps de fonction asynchrone : `await` et `return` au
//    niveau supérieur sont permis, ce que `node --check` refuse) ;
// 3. chaque phase('…') a son entrée dans meta.phases, et inversement ;
// 4. ni Date.now(), ni Math.random(), ni new Date() sans argument (interdits : ils casseraient la reprise) ;
// 5. le modèle lit ses paramètres dans `args`.
// Code 1 si une erreur ; les numéros de ligne sont ceux du fichier.
import { readFileSync } from 'node:fs'
import vm from 'node:vm'

function metaSpan(src) {
  const m = src.match(/^\s*export\s+const\s+meta\s*=\s*\{/)
  if (!m) return null
  let i = m[0].length - 1, depth = 0, quote = null
  for (; i < src.length; i++) {
    const c = src[i]
    if (quote) {
      if (c === '\\') i++
      else if (c === quote) quote = null
      continue
    }
    if (c === "'" || c === '"' || c === '`') quote = c
    else if (c === '{') depth++
    else if (c === '}' && --depth === 0) return { start: src.indexOf('{', m.index), end: i + 1 }
  }
  return null
}

let failed = false
for (const file of process.argv.slice(2)) {
  const src = readFileSync(file, 'utf8')
  const errors = [], notes = []
  const span = metaSpan(src)
  let meta = null
  if (!span) errors.push('le fichier ne commence pas par `export const meta = {...}`')
  else {
    const lit = src.slice(span.start, span.end)
    if (lit.includes('`') || lit.includes('${')) errors.push('meta contient un gabarit (`...` ou ${}) : littéral pur exigé')
    try {
      meta = vm.runInNewContext(`(${lit})`, Object.create(null), { timeout: 100 })
    } catch (e) {
      errors.push(`meta n'est pas un littéral pur : ${e.message}`)
    }
    if (meta && (!meta.name || !meta.description)) errors.push('meta.name et meta.description sont requis')
  }
  const head = span ? src.slice(0, span.end).replace(/[^\n]/g, '') : ''
  const body = span ? src.slice(span.end) : src
  const wrapped = '(async function (args, agent, parallel, pipeline, phase, log, budget, workflow) {' + head + body + '\n})'
  try {
    new vm.Script(wrapped, { filename: file })
  } catch (e) {
    const where = (e.stack || '').split('\n')[0]
    errors.push(`syntaxe : ${e.message} (${where})`)
  }
  const code = body.replace(/\/\/.*$/gm, '')
  const called = [...code.matchAll(/\bphase\(\s*(['"])(.*?)\1\s*\)/g)].map(m => m[2])
  const declared = (meta && meta.phases ? meta.phases : []).map(p => p.title)
  for (const t of called) if (!declared.includes(t)) errors.push(`phase('${t}') absente de meta.phases`)
  for (const t of declared) if (!called.includes(t)) notes.push(`meta.phases « ${t} » sans appel phase('${t}')`)
  if (/\bDate\.now\s*\(|\bMath\.random\s*\(|new\s+Date\s*\(\s*\)/.test(code)) errors.push('Date.now(), Math.random() ou new Date() : interdits dans un workflow')
  if (!/\bargs\b/.test(code)) notes.push("le modèle ne lit pas `args`")
  for (const n of notes) console.log(`  ! ${file} : ${n}`)
  for (const e of errors) console.log(`  ✘ ${file} : ${e}`)
  console.log(`${file} : ${errors.length ? 'REFUSÉ' : 'OK'} (${meta ? meta.name : '?'}, phases : ${declared.join(' → ') || '—'})`)
  if (errors.length) failed = true
}
process.exit(failed ? 1 : 0)
