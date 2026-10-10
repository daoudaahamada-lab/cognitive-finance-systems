import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

/** Joins class names; later Tailwind utilities override earlier conflicting ones (w-auto beats w-full). */
export function cn(...values: ClassValue[]) {
  return twMerge(clsx(values));
}
