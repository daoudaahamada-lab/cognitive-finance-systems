import { clsx, type ClassValue } from "clsx";
import { extendTailwindMerge } from "tailwind-merge";

/** Knows the custom @theme scales (globals.css), so text-h1 is a size and not a colour. */
const twMerge = extendTailwindMerge({
  extend: {
    theme: {
      text: ["2xs", "title", "h1", "kpi"],
      radius: ["control", "card"],
      shadow: ["card", "pop"],
    },
  },
});

/** Joins class names; later Tailwind utilities override earlier conflicting ones (w-auto beats w-full). */
export function cn(...values: ClassValue[]) {
  return twMerge(clsx(values));
}
