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
}: {
  name: string;
  defaultValue?: string[];
  placeholder?: string;
  suggestions?: string[];
  id?: string;
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
        "flex min-h-9 flex-wrap items-center gap-1.5 rounded-lg border border-line bg-surface px-2 py-1.5 shadow-sm",
        "focus-within:border-brand-500 focus-within:ring-2 focus-within:ring-brand-500/20",
      )}
    >
      <input type="hidden" name={name} value={JSON.stringify(tags)} />
      {tags.map((tag) => (
        <span key={tag} className="inline-flex items-center gap-1 rounded-md bg-brand-50 px-2 py-0.5 text-xs font-medium text-brand-700">
          {tag}
          <button type="button" onClick={() => setTags(tags.filter((t) => t !== tag))} aria-label={`Retirer ${tag}`} className="text-brand-700/60 hover:text-brand-900">
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
        className="min-w-32 flex-1 bg-transparent px-1 text-sm outline-none placeholder:text-muted/70"
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
