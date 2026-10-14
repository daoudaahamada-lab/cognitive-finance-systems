import {loadFont} from '@remotion/fonts';
import {staticFile} from 'remotion';

// Polices embarquées dans public/fonts (licence SIL OFL) : aucun accès réseau au rendu.
const inter = [400, 500, 600, 700, 800, 900].map((w) =>
  loadFont({family: 'Inter', url: staticFile(`fonts/inter-latin-${w}-normal.woff2`), weight: String(w)}),
);
const mono = [500, 700].map((w) =>
  loadFont({family: 'JetBrains Mono', url: staticFile(`fonts/jetbrains-mono-latin-${w}-normal.woff2`), weight: String(w)}),
);

export const policesPretes = Promise.all([...inter, ...mono]);
