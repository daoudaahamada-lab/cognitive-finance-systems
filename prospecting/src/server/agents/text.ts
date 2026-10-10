/** Lowercases and strips accents so "Directeur Général" matches "directeur general". */
export function normalize(value: string): string {
  return value
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .toLowerCase()
    .replace(/[’']/g, "'")
    .replace(/\s+/g, " ")
    .trim();
}

export function containsTerm(haystack: string, term: string): boolean {
  const needle = normalize(term);
  if (!needle) return false;
  const text = normalize(haystack);
  // Short acronyms (CFO, DG, RH) must match a whole word, or "cto" would match "directory".
  if (needle.length <= 4 && /^[a-z0-9]+$/.test(needle)) {
    return new RegExp(`(^|[^a-z0-9])${needle}([^a-z0-9]|$)`).test(text);
  }
  return text.includes(needle);
}
