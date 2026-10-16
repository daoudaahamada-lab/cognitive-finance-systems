"use client";

import { X } from "lucide-react";
import { useState, type KeyboardEvent } from "react";
import { cn } from "@/lib/cn";

/** Free-text chips. Submits its value as a JSON array in a hidden input. */
export function TagInput({
  name,
  defaultValue = [],
  placeholder,
  suggestions = [],
  id,
  ...aria
}: {
  name: string;
  defaultValue?: string[];
  placeholder?: string;
  suggestions?: string[];
  id?: string;
  /** Set by Field: forwarded to the text input. */
  "aria-describedby"?: string;
  "aria-invalid"?: boolean | "true" | "false";
  "aria-label"?: string;
}) {
  const [tags, setTags] = useState<string[]>(defaultValue);
  const [draft, setDraft] = useState("");
  const listId = suggestions.length > 0 ? `${id ?? name}-suggestions` : undefined;

  const add = (raw: string) => {
    const value = raw.trim().replace(/,$/, "");
    if (value && !tags.some((t) => t.toLowerCase() === value.toLowerCase())) setTags([...tags, value]);
    setDraft("");
  };

  const onKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" || e.key === ",") {
      e.preventDefault();
      add(draft);
    } else if (e.key === "Backspace" && draft === "" && tags.length > 0) {
      setTags(tags.slice(0, -1));
    }
  };

  return (
    <div
      className={cn(
        "flex min-h-11 flex-wrap items-center gap-1.5 rounded-control border border-line bg-surface px-2 py-1.5 sm:min-h-9",
        "focus-within:border-brand-600 focus-within:ring-2 focus-within:ring-brand-600/50",
        (aria["aria-invalid"] === true || aria["aria-invalid"] === "true") && "border-danger",
      )}
    >
      <input type="hidden" name={name} value={JSON.stringify(tags)} />
      {tags.map((tag) => (
        <span key={tag} className="inline-flex items-center gap-1 rounded-md bg-brand-50 px-2 py-0.5 text-xs font-medium text-brand-700">
          {tag}
          <button type="button" onClick={() => setTags(tags.filter((t) => t !== tag))} aria-label={`Retirer ${tag}`} className="rounded text-brand-700/60 hover:text-brand-900 pointer-coarse:p-1">
            <X className="size-3" />
          </button>
        </span>
      ))}
      <input
        id={id}
        list={listId}
        value={draft}
        onChange={(e) => setDraft(e.target.value)}
        onKeyDown={onKeyDown}
        onBlur={() => draft && add(draft)}
        placeholder={tags.length === 0 ? placeholder : undefined}
        {...aria}
        className="min-w-32 flex-1 bg-transparent px-1 text-base outline-none placeholder:text-muted sm:text-sm"
      />
      {listId ? (
        <datalist id={listId}>
          {suggestions.map((s) => (
            <option key={s} value={s} />
          ))}
        </datalist>
      ) : null}
    </div>
  );
}
