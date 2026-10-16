"use client";

import { FileText, UploadCloud, X } from "lucide-react";
import { useEffect, useId, useRef, useState, type DragEvent } from "react";
import { cn } from "@/lib/cn";

/** Dropzone around a visually hidden file input: the file is submitted with the form as usual. */
export function FileDrop({
  name,
  id,
  accept,
  label = "Glissez un CSV ou cliquez pour choisir",
  hint,
  className,
  ...aria
}: {
  name: string;
  id?: string;
  accept?: string;
  label?: string;
  hint?: string;
  className?: string;
  /** Set by Field: forwarded to the input. */
  "aria-describedby"?: string;
  "aria-invalid"?: boolean | "true" | "false";
}) {
  const fallbackId = useId();
  const inputId = id ?? fallbackId;
  const input = useRef<HTMLInputElement>(null);
  const [fileName, setFileName] = useState<string | null>(null);
  const [dragging, setDragging] = useState(false);

  // React resets forms after a successful action: forget the name with the file.
  useEffect(() => {
    const form = input.current?.form;
    if (!form) return;
    const onReset = () => setFileName(null);
    form.addEventListener("reset", onReset);
    return () => form.removeEventListener("reset", onReset);
  }, []);

  const onDrop = (e: DragEvent<HTMLLabelElement>) => {
    e.preventDefault();
    setDragging(false);
    if (!input.current || e.dataTransfer.files.length === 0) return;
    input.current.files = e.dataTransfer.files;
    setFileName(e.dataTransfer.files[0]!.name);
  };

  const clear = () => {
    if (input.current) input.current.value = "";
    setFileName(null);
  };

  return (
    <div className={cn("min-w-0", className)}>
      <label
        htmlFor={inputId}
        onDragOver={(e) => {
          e.preventDefault();
          setDragging(true);
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={onDrop}
        className={cn(
          "flex cursor-pointer flex-col items-center justify-center gap-1.5 rounded-card border-2 border-dashed px-4 py-6 text-center transition-colors",
          "has-[:focus-visible]:outline-2 has-[:focus-visible]:outline-offset-2 has-[:focus-visible]:outline-brand-600",
          dragging ? "border-brand-600 bg-brand-50" : "border-line-strong bg-surface-2 hover:border-brand-400",
          (aria["aria-invalid"] === true || aria["aria-invalid"] === "true") && "border-danger",
        )}
      >
        <UploadCloud className={cn("size-6", dragging ? "text-brand-600" : "text-muted")} aria-hidden />
        <span className="text-sm font-medium text-ink">{label}</span>
        {hint ? <span className={cn("text-xs", dragging ? "text-brand-700" : "text-muted")}>{hint}</span> : null}
        <input
          ref={input}
          id={inputId}
          name={name}
          type="file"
          accept={accept}
          className="sr-only"
          onChange={(e) => setFileName(e.target.files?.[0]?.name ?? null)}
          {...aria}
        />
      </label>
      {fileName ? (
        <div className="mt-2 flex items-center gap-2 rounded-control border border-line bg-surface px-3 py-2 text-sm">
          <FileText className="size-4 shrink-0 text-muted" aria-hidden />
          <span className="min-w-0 flex-1 truncate" aria-live="polite">
            {fileName}
          </span>
          <button
            type="button"
            onClick={clear}
            aria-label="Retirer le fichier"
            className="-m-1 rounded p-1 text-muted hover:text-ink focus-visible:outline-2 focus-visible:outline-brand-600 pointer-coarse:p-2"
          >
            <X className="size-4" aria-hidden />
          </button>
        </div>
      ) : null}
    </div>
  );
}
