const AVATAR_COLORS = ["#4f46e5", "#0e7490", "#7c3aed", "#be185d", "#b45309", "#15803d", "#1d4ed8", "#9333ea"];

export function hashColor(seed: string): string {
  let h = 0;
  for (let i = 0; i < seed.length; i++) h = (h * 31 + seed.charCodeAt(i)) >>> 0;
  return AVATAR_COLORS[h % AVATAR_COLORS.length]!;
}
