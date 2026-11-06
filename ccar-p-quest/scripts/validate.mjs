// Vérifie la structure des fichiers content/level-XX.json.
// Usage : node scripts/validate.mjs            (tous les niveaux présents)
//         node scripts/validate.mjs 3 4        (seulement les niveaux 3 et 4)
import { readFileSync, readdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const contentDir = join(root, "content");

export const DOMAINS = {
  D1: "Solution Design & Architecture",
  D2: "Claude Models, Prompting & Context Engineering",
  D3: "Integration",
  D4: "Evaluation, Testing & Optimization",
  D5: "Governance, Safety & Risk Management",
  D6: "Stakeholder Communication & Lifecycle Management",
  D7: "Developer Productivity & Operational Enablement",
};

export const BLUEPRINT = {
  1: { D2: 9, D1: 1 },
  2: { D1: 10 },
  3: { D3: 10 },
  4: { D3: 7, D2: 3 },
  5: { D4: 10 },
  6: { D4: 5, D1: 4, D6: 1 },
  7: { D5: 10 },
  8: { D6: 10 },
  9: { D7: 6, D6: 2, D5: 2 },
  10: { D1: 2, D2: 1, D3: 2, D4: 1, D5: 2, D6: 1, D7: 1 },
};

const OFFICIAL = /^https:\/\/(platform\.claude\.com\/docs\/|code\.claude\.com\/docs\/|www\.anthropic\.com\/|docs\.claude\.com\/|claude\.com\/|support\.claude\.com\/)/;

function str(v, min = 1) {
  return typeof v === "string" && v.trim().length >= min;
}

export function validateLevel(level, n) {
  const errors = [];
  const err = (m) => errors.push(`niveau ${n} : ${m}`);
  if (level.id !== n) err(`id vaut ${level.id}, attendu ${n}`);
  for (const k of ["title", "theme", "intro"]) if (!str(level[k])) err(`champ ${k} manquant`);
  const b = level.boss || {};
  for (const k of ["name", "epithet", "taunt", "defeat", "victory"]) if (!str(b[k])) err(`boss.${k} manquant`);

  const checkSource = (s, where) => {
    if (!s || !str(s.title) || !str(s.url)) return err(`${where} : source incomplète`);
    if (!OFFICIAL.test(s.url)) err(`${where} : source non officielle ${s.url}`);
  };

  if (!Array.isArray(level.cards) || level.cards.length !== 6) err(`il faut 6 fiches (trouvé ${level.cards?.length})`);
  (level.cards || []).forEach((c, i) => {
    for (const k of ["term", "fr", "trap"]) if (!str(c[k])) err(`fiche ${i + 1} : ${k} manquant`);
    checkSource(c.source, `fiche ${i + 1}`);
  });

  if (!Array.isArray(level.warmup) || level.warmup.length !== 5) err(`il faut 5 affirmations d'échauffement (trouvé ${level.warmup?.length})`);
  const w = level.warmup || [];
  w.forEach((x, i) => {
    if (!str(x.statement)) err(`échauffement ${i + 1} : statement manquant`);
    if (typeof x.answer !== "boolean") err(`échauffement ${i + 1} : answer doit être true/false`);
    if (!str(x.fr)) err(`échauffement ${i + 1} : fr manquant`);
  });
  const trues = w.filter((x) => x.answer === true).length;
  if (w.length === 5 && (trues < 2 || trues > 3)) err(`échauffement : il faut 2 ou 3 affirmations vraies (trouvé ${trues})`);

  const qs = level.questions || [];
  if (qs.length !== 10) err(`il faut 10 questions (trouvé ${qs.length})`);
  const counts = {};
  const ids = new Set();
  let multi = 0;
  qs.forEach((q, i) => {
    const where = q.id || `question ${i + 1}`;
    const expectedId = `L${String(n).padStart(2, "0")}-Q${String(i + 1).padStart(2, "0")}`;
    if (q.id !== expectedId) err(`${where} : id attendu ${expectedId}`);
    if (ids.has(q.id)) err(`${where} : id en double`);
    ids.add(q.id);
    if (!DOMAINS[q.domain]) err(`${where} : domaine inconnu ${q.domain}`);
    counts[q.domain] = (counts[q.domain] || 0) + 1;
    if (!str(q.stem, 120)) err(`${where} : énoncé trop court`);
    const opts = q.options || [];
    if (q.type === "single") {
      if (opts.length !== 4) err(`${where} : une question single a 4 options`);
      if (!Array.isArray(q.answer) || q.answer.length !== 1) err(`${where} : une question single a 1 bonne réponse`);
    } else if (q.type === "multi") {
      multi++;
      if (opts.length !== 5) err(`${where} : une question multi a 5 options`);
      if (!Array.isArray(q.answer) || q.answer.length !== 2) err(`${where} : une question multi a 2 bonnes réponses`);
      if (!/\(Select TWO\.\)\s*$/.test(q.stem || "")) err(`${where} : l'énoncé multi doit finir par « (Select TWO.) »`);
    } else err(`${where} : type inconnu ${q.type}`);
    (q.answer || []).forEach((a) => {
      if (!Number.isInteger(a) || a < 0 || a >= opts.length) err(`${where} : index de réponse invalide ${a}`);
    });
    if (new Set(q.answer || []).size !== (q.answer || []).length) err(`${where} : réponse en double`);
    opts.forEach((o, j) => {
      if (!str(o.text)) err(`${where} : option ${j + 1} sans texte`);
      if (!str(o.why)) err(`${where} : option ${j + 1} sans explication`);
    });
    if (!str(q.explanation)) err(`${where} : explanation manquante`);
    if (!str(q.tip)) err(`${where} : tip manquant`);
    checkSource(q.source, where);
  });
  if (multi < 1) err(`prévoir au moins 1 question multi (trouvé ${multi})`);

  // Longueur des options : la bonne réponse ne doit pas se repérer à sa taille.
  let longest = 0;
  qs.forEach((q, i) => {
    const where = q.id || `question ${i + 1}`;
    const opts = q.options || [];
    const ans = q.answer || [];
    if (opts.length < 4 || !ans.length) return;
    const len = opts.map((o) => (o.text || "").length);
    const right = ans.map((a) => len[a] || 0);
    const wrong = len.filter((_, j) => !ans.includes(j));
    const meanWrong = wrong.reduce((s, x) => s + x, 0) / wrong.length;
    const ratio = Math.max(...right) / meanWrong;
    if (ratio > 1.3) err(`${where} : la bonne réponse est ${ratio.toFixed(2)}× plus longue que la moyenne des mauvaises (max 1.30)`);
    if (ratio < 0.75) err(`${where} : la bonne réponse est nettement plus courte que les mauvaises (${ratio.toFixed(2)}×, min 0.75)`);
    if (Math.max(...right) > Math.max(...wrong)) longest++;
  });
  if (qs.length === 10 && longest > 4) err(`la bonne réponse est l'option la plus longue dans ${longest} questions sur 10 (max 4)`);
  const bp = BLUEPRINT[n];
  if (bp) {
    for (const d of Object.keys(DOMAINS)) {
      if ((counts[d] || 0) !== (bp[d] || 0)) err(`domaine ${d} : ${counts[d] || 0} question(s), attendu ${bp[d] || 0}`);
    }
  }
  return errors;
}

export function loadLevels(only) {
  const files = readdirSync(contentDir).filter((f) => /^level-\d{2}\.json$/.test(f)).sort();
  const levels = [];
  const errors = [];
  for (const f of files) {
    const n = Number(f.slice(6, 8));
    if (only && only.length && !only.includes(n)) continue;
    let level;
    try {
      level = JSON.parse(readFileSync(join(contentDir, f), "utf8"));
    } catch (e) {
      errors.push(`${f} : JSON invalide (${e.message})`);
      continue;
    }
    errors.push(...validateLevel(level, n));
    levels.push(level);
  }
  return { levels, errors };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const only = process.argv.slice(2).map(Number).filter(Boolean);
  const { levels, errors } = loadLevels(only);
  if (errors.length) {
    console.error(errors.join("\n"));
    console.error(`\n${errors.length} erreur(s).`);
    process.exit(1);
  }
  const total = levels.reduce((s, l) => s + l.questions.length, 0);
  console.log(`OK : ${levels.length} niveau(x), ${total} questions.`);
}
