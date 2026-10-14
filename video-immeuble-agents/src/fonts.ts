import {loadFont} from '@remotion/fonts';
import {staticFile} from 'remotion';

// Polices embarquées dans public/fonts (licence SIL OFL) : aucun accès réseau au rendu.
// loadFont() bloque le rendu tant que la police n'est pas chargée.
for (const w of [400, 500, 600, 700, 800, 900]) {
  loadFont({family: 'Inter', url: staticFile(`fonts/inter-latin-${w}-normal.woff2`), weight: String(w)});
}
for (const w of [500, 700]) {
  loadFont({family: 'JetBrains Mono', url: staticFile(`fonts/jetbrains-mono-latin-${w}-normal.woff2`), weight: String(w)});
}
