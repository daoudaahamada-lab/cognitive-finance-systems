import { semanticTone, type SemanticTone, type Tone } from "./labels";

export type ToneClasses = {
  /** Badge: soft background, readable text and the ring colour (pair with ring-1 ring-inset). */
  badge: string;
  /** Soft background and text, without ring: icon circles, chips, banners. */
  soft: string;
  /** Text and icon colour alone. */
  text: string;
  /** Solid fill: dots, bars, progress. */
  fill: string;
  /** Border colour for accents (border-t-2, outlines). */
  border: string;
};

/** Every semantic tone as token classes, so pages never pick raw palette colours. */
export const TONE_CLASSES: Record<SemanticTone, ToneClasses> = {
  neutral: { badge: "bg-canvas text-ink-2 ring-line", soft: "bg-canvas text-ink-2", text: "text-muted", fill: "bg-muted", border: "border-line-strong" },
  strong: { badge: "bg-line text-ink ring-line-strong", soft: "bg-line text-ink", text: "text-ink", fill: "bg-ink-2", border: "border-ink-2" },
  brand: { badge: "bg-brand-50 text-brand-700 ring-brand-200", soft: "bg-brand-50 text-brand-700", text: "text-brand-700", fill: "bg-brand-600", border: "border-brand-600" },
  ai: { badge: "bg-ai-soft text-ai ring-ai-line", soft: "bg-ai-soft text-ai", text: "text-ai", fill: "bg-ai", border: "border-ai" },
  success: { badge: "bg-success-soft text-success ring-success-line", soft: "bg-success-soft text-success", text: "text-success", fill: "bg-success", border: "border-success" },
  warning: { badge: "bg-warning-soft text-warning ring-warning-line", soft: "bg-warning-soft text-warning", text: "text-warning", fill: "bg-warning", border: "border-warning" },
  danger: { badge: "bg-danger-soft text-danger ring-danger-line", soft: "bg-danger-soft text-danger", text: "text-danger", fill: "bg-danger", border: "border-danger" },
  info: { badge: "bg-info-soft text-info ring-info-line", soft: "bg-info-soft text-info", text: "text-info", fill: "bg-info", border: "border-info" },
};

/** Classes for a tone; legacy names (gray, green…) resolve to their semantic tone. */
export function toneClasses(tone: Tone): ToneClasses {
  return TONE_CLASSES[semanticTone(tone)];
}
