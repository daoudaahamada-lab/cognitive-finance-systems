import {cancelRender, continueRender, delayRender, staticFile} from 'remotion';

// A family name that does NOT exist on the system: if the @font-face fails we get an
// obvious fallback (DejaVu) instead of silently picking up the system-installed Inter.
export const FONT_FAMILY = 'WTH Inter';

const faces: {file: string; weight: number; optional?: boolean}[] = [
  {file: 'fonts/Inter-SemiBold.otf', weight: 600},
  // Bold: Story captions (storyboard: Inter Bold 64 px). Optional: if the file is missing, weight 700 falls back
  // to ExtraBold (CSS weight matching) with a warning instead of cancelling every render (Explainer included).
  {file: 'fonts/Inter-Bold.otf', weight: 700, optional: true},
  {file: 'fonts/Inter-ExtraBold.otf', weight: 800},
];

const STYLE_ID = 'wth-fonts';

if (typeof document !== 'undefined' && !document.getElementById(STYLE_ID)) {
  const style = document.createElement('style');
  style.id = STYLE_ID;
  style.textContent = faces
    .map(
      (f) => `@font-face {
  font-family: '${FONT_FAMILY}';
  src: url('${staticFile(f.file)}') format('opentype');
  font-weight: ${f.weight};
  font-style: normal;
  font-display: block;
}`,
    )
    .join('\n');
  document.head.appendChild(style);

  const handle = delayRender('Loading Inter @font-face');
  Promise.all(
    faces.map((f) =>
      document.fonts.load(`${f.weight} 64px '${FONT_FAMILY}'`).then(
        (l) => ({f, ok: l.length > 0 && l.some((face) => face.status === 'loaded')}),
        () => ({f, ok: false}),
      ),
    ),
  )
    .then((res) => {
      const missing = res.filter((r) => !r.ok);
      const fatal = missing.filter((r) => !r.f.optional);
      if (fatal.length > 0) {
        throw new Error(`@font-face '${FONT_FAMILY}' did not load: ${fatal.map((r) => r.f.file).join(', ')}`);
      }
      for (const r of missing) console.warn(`Optional font face not loaded (fallback used): ${r.f.file}`);
      continueRender(handle);
    })
    .catch((err) => cancelRender(err));
}
