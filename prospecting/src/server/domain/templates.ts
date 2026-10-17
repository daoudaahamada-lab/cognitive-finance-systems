import { createRng, pick } from "./random";

export type TemplateVars = {
  firstName: string;
  lastName: string;
  company: string;
  title: string;
  industry: string;
  location: string;
  senderFirstName: string;
  bookingUrl: string;
};

export const TEMPLATE_VARIABLES: (keyof TemplateVars)[] = [
  "firstName",
  "lastName",
  "company",
  "title",
  "industry",
  "location",
  "senderFirstName",
  "bookingUrl",
];

/** LinkedIn rejects invitation notes longer than this. */
export const INVITE_NOTE_MAX = 300;

/**
 * Resolves spintax ("{Bonjour|Hello} {{firstName}}") and variables.
 * The seed keeps the chosen variant stable for a given prospect.
 */
export function renderTemplate(template: string, vars: TemplateVars, seed: string): string {
  const rng = createRng(seed);
  // Swap variables for placeholders first so their values can never be read as spintax.
  const values: string[] = [];
  let text = template.replace(/\{\{\s*(\w+)\s*\}\}/g, (match, name: string) => {
    if (!(name in vars)) return match;
    values.push(vars[name as keyof TemplateVars] ?? "");
    return `\u0000${values.length - 1}\u0000`;
  });
  // Innermost groups first, so nesting works.
  const spin = /\{([^{}]*\|[^{}]*)\}/;
  for (let guard = 0; guard < 100 && spin.test(text); guard++) {
    text = text.replace(spin, (_, options: string) => pick(rng, options.split("|")));
  }
  text = text.replace(/\u0000(\d+)\u0000/g, (_, index: string) => values[Number(index)] ?? "");
  return text.replace(/[ \t]+\n/g, "\n").replace(/ {2,}/g, " ").trim();
}

/**
 * Names between {{ }} that are not template variables. Any content counts, accented or spaced
 * ({{prénom}}, {{mon prénom}}), since renderTemplate would otherwise send it as written.
 */
export function unknownVariables(template: string): string[] {
  const found = new Set<string>();
  for (const m of template.matchAll(/\{\{\s*([^{}]*?)\s*\}\}/g)) {
    const name = m[1]!;
    if (!TEMPLATE_VARIABLES.includes(name as keyof TemplateVars)) found.add(name);
  }
  return [...found];
}

/** French names of the template variables, for the editor's insert chips. */
export const VARIABLE_LABELS_FR: Record<keyof TemplateVars, string> = {
  firstName: "Prénom",
  lastName: "Nom",
  company: "Entreprise",
  title: "Poste",
  industry: "Secteur",
  location: "Ville",
  senderFirstName: "Votre prénom",
  bookingUrl: "Votre lien de réservation",
};

/** What a French speaker is likely to type instead of the real variable name (accents and separators removed). */
const VARIABLE_ALIASES: Record<string, keyof TemplateVars> = {
  prenom: "firstName",
  first: "firstName",
  nom: "lastName",
  nomdefamille: "lastName",
  last: "lastName",
  entreprise: "company",
  societe: "company",
  boite: "company",
  organisation: "company",
  poste: "title",
  titre: "title",
  fonction: "title",
  job: "title",
  jobtitle: "title",
  secteur: "industry",
  industrie: "industry",
  ville: "location",
  lieu: "location",
  localisation: "location",
  region: "location",
  monprenom: "senderFirstName",
  votreprenom: "senderFirstName",
  expediteur: "senderFirstName",
  sender: "senderFirstName",
  signature: "senderFirstName",
  lien: "bookingUrl",
  lienrdv: "bookingUrl",
  rdv: "bookingUrl",
  agenda: "bookingUrl",
  calendly: "bookingUrl",
  reservation: "bookingUrl",
  liendereservation: "bookingUrl",
  booking: "bookingUrl",
};

function normalizeName(name: string): string {
  return name
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9]/g, "");
}

/** The variable an unknown name most likely meant ({{prenom}} → firstName), or null. */
export function suggestVariable(name: string): keyof TemplateVars | null {
  const key = normalizeName(name);
  if (!key) return null;
  return TEMPLATE_VARIABLES.find((v) => v.toLowerCase() === key) ?? VARIABLE_ALIASES[key] ?? null;
}

/** Number of distinct texts the spintax can produce: "{Bonjour|Salut} … {a|b|c}" gives 6. */
export function countVariants(template: string): number {
  // Variables are never spintax (see renderTemplate): drop them first.
  let text = template.replace(/\{\{[^{}]*\}\}/g, "");
  const counts: number[] = [];
  const product = (part: string) => [...part.matchAll(/\u0001(\d+)\u0001/g)].reduce((total, m) => total * (counts[Number(m[1])] ?? 1), 1);
  // Innermost groups first, as renderTemplate resolves them.
  const spin = /\{([^{}]*\|[^{}]*)\}/;
  for (let guard = 0; guard < 100 && spin.test(text); guard++) {
    text = text.replace(spin, (_, options: string) => {
      counts.push(options.split("|").reduce((sum, option) => sum + product(option), 0));
      return `\u0001${counts.length - 1}\u0001`;
    });
  }
  return product(text);
}
