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

export function unknownVariables(template: string): string[] {
  const found = new Set<string>();
  for (const m of template.matchAll(/\{\{\s*(\w+)\s*\}\}/g)) {
    const name = m[1]!;
    if (!TEMPLATE_VARIABLES.includes(name as keyof TemplateVars)) found.add(name);
  }
  return [...found];
}
