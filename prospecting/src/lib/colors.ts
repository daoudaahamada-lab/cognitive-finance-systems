/** Soft avatar tints ({bg, fg}) plus a saturated fill kept for large avatars. None is the brand colour. */
const AVATAR_TINTS = [
  { bg: "#e6eefb", fg: "#1f4f99", solid: "#2b5fb4" },
  { bg: "#e0f2f2", fg: "#0f5e62", solid: "#0e7490" },
  { bg: "#efe9fc", fg: "#5b2bb0", solid: "#6d3fd0" },
  { bg: "#fbe8f0", fg: "#99204f", solid: "#be185d" },
  { bg: "#fbf0e1", fg: "#86480b", solid: "#b45309" },
  { bg: "#e5f3ea", fg: "#1d6a3a", solid: "#15803d" },
  { bg: "#eceef3", fg: "#3a4152", solid: "#4b5567" },
  { bg: "#fdece5", fg: "#9f3a17", solid: "#c2410c" },
] as const;

export type AvatarTint = (typeof AVATAR_TINTS)[number];

function hash(seed: string): number {
  let h = 0;
  for (let i = 0; i < seed.length; i++) h = (h * 31 + seed.charCodeAt(i)) >>> 0;
  return h;
}

export function avatarTint(seed: string): AvatarTint {
  return AVATAR_TINTS[hash(seed) % AVATAR_TINTS.length]!;
}

/** Saturated colour for a seed (large avatars). */
export function hashColor(seed: string): string {
  return avatarTint(seed).solid;
}
