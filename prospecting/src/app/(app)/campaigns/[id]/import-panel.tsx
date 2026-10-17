"use client";

import { Upload, X } from "lucide-react";
import { useEffect, useRef, useSyncExternalStore, type ReactNode } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { cn } from "@/lib/cn";

/** The panel's id, and the URL hash that opens it (/campaigns/<id>#import). */
export const IMPORT_ID = "import";
const TOGGLE_ID = "import-toggle";
const CHANGE = "vela:import-panel";

// The URL hash is the panel's state, so links to #import open it and the header button stays in sync.
function subscribe(onChange: () => void) {
  window.addEventListener("hashchange", onChange);
  window.addEventListener("popstate", onChange);
  window.addEventListener(CHANGE, onChange);
  return () => {
    window.removeEventListener("hashchange", onChange);
    window.removeEventListener("popstate", onChange);
    window.removeEventListener(CHANGE, onChange);
  };
}

const isOpen = () => window.location.hash === `#${IMPORT_ID}`;

function useImportOpen(): boolean {
  return useSyncExternalStore(subscribe, isOpen, () => false);
}

function setOpen(open: boolean) {
  const url = new URL(window.location.href);
  url.hash = open ? IMPORT_ID : "";
  // replaceState keeps the history clean and does not jump; Next.js keeps its router state in sync.
  window.history.replaceState(null, "", url);
  window.dispatchEvent(new Event(CHANGE));
}

/** 'Importer une liste' header button: opens and closes the panel below the page header. */
export function ImportToggle() {
  const open = useImportOpen();
  return (
    <Button id={TOGGLE_ID} variant="secondary" aria-expanded={open} aria-controls={IMPORT_ID} onClick={() => setOpen(!open)}>
      <Upload className="size-4" aria-hidden /> Importer une liste
    </Button>
  );
}

export function ImportPanel({ children, className }: { children: ReactNode; className?: string }) {
  const open = useImportOpen();
  const panel = useRef<HTMLElement>(null);
  const wasOpen = useRef(false);

  // Each time it opens (button, link or #import on arrival), bring the panel into view and move focus to it.
  useEffect(() => {
    if (open && !wasOpen.current) {
      const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      panel.current?.scrollIntoView({ block: "start", behavior: reduce ? "auto" : "smooth" });
      panel.current?.focus({ preventScroll: true });
    }
    wasOpen.current = open;
  }, [open]);

  const close = () => {
    setOpen(false);
    document.getElementById(TOGGLE_ID)?.focus();
  };

  return (
    <Card
      ref={panel}
      id={IMPORT_ID}
      hidden={!open}
      tabIndex={-1}
      aria-labelledby="import-title"
      className={cn("focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand-600", className)}
    >
      <CardHeader
        title={<span id="import-title">Importer une liste</span>}
        description="Les profils importés sont contactés quelle que soit leur note. Les exclusions restent appliquées."
        actions={
          <Button variant="ghost" size="icon" onClick={close} aria-label="Fermer l'import" title="Fermer">
            <X className="size-4" aria-hidden />
          </Button>
        }
      />
      <CardBody>{children}</CardBody>
    </Card>
  );
}
