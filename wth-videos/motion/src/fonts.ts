import {cancelRender, continueRender, delayRender, staticFile} from 'remotion';

// A family name that does NOT exist on the system: if the @font-face fails we get an
// obvious fallback (DejaVu) instead of silently picking up the system-installed Inter.
export const FONT_FAMILY = 'WTH Inter';

const faces: {file: string; weight: number}[] = [
  {file: 'fonts/Inter-SemiBold.otf', weight: 600},
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
  Promise.all(faces.map((f) => document.fonts.load(`${f.weight} 64px '${FONT_FAMILY}'`)))
    .then((loaded) => {
      if (loaded.some((l) => l.length === 0)) {
        throw new Error(`@font-face '${FONT_FAMILY}' did not load`);
      }
      continueRender(handle);
    })
    .catch((err) => cancelRender(err));
}
