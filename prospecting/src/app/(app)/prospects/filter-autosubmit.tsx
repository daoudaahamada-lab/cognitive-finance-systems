"use client";

import Form from "next/form";
import { useEffect, useRef, type ReactNode } from "react";

/**
 * The prospects filter form. Changing a select applies the filters at once (form.requestSubmit()),
 * the search applies on Enter. Without JavaScript it is a plain GET form with its 'Filtrer' button.
 * `values` holds the filters the page was rendered with, by field name.
 */
export function FilterAutosubmit({
  action,
  label,
  values,
  className,
  children,
}: {
  action: string;
  label: string;
  values: Record<string, string>;
  className?: string;
  children: ReactNode;
}) {
  const formRef = useRef<HTMLFormElement>(null);
  const applied = JSON.stringify(values);

  // The fields are uncontrolled and the form stays mounted across client navigations, so a link that changes
  // the filters ('Effacer les filtres', '+ N autres') must bring the fields back in line with the page.
  useEffect(() => {
    const form = formRef.current;
    if (!form) return;
    const wanted = JSON.parse(applied) as Record<string, string>;
    for (const name of Object.keys(wanted)) {
      const field = form.elements.namedItem(name);
      if (!(field instanceof HTMLInputElement || field instanceof HTMLSelectElement)) continue;
      if (field.value !== wanted[name]) field.value = wanted[name] ?? "";
      if (field instanceof HTMLSelectElement && field.selectedIndex === -1) field.selectedIndex = 0;
    }
  }, [applied]);

  return (
    <Form
      ref={formRef}
      action={action}
      scroll={false}
      role="search"
      aria-label={label}
      className={className}
      onChange={(event) => {
        if (event.target instanceof HTMLSelectElement) event.currentTarget.requestSubmit();
      }}
    >
      {children}
    </Form>
  );
}
