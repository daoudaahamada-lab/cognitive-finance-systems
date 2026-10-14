// Palette et typographie de la video.
// Une seule couleur d'accent : le bleu. Le jaune ne sert qu'au statut "en travaux"
// (c'est la couleur de l'application elle-meme).

export const C = {
  fond: '#e4dfd6', // identique au fond des captures du QG : les etages flottent sans bord
  encre: '#111214',
  gris: '#6e6a63',
  grisClair: '#9a958c',
  accent: '#2f6bff',
  accentDoux: 'rgba(47, 107, 255, 0.10)',
  travaux: '#f2b400',
  carte: '#faf9f6',
  trait: 'rgba(17, 18, 20, 0.08)',
  ombre: '0 30px 80px rgba(40, 32, 20, 0.16), 0 6px 18px rgba(40, 32, 20, 0.08)',

  // Cockpit (theme sombre de l'application)
  nuit: '#07090e',
  nuitCarte: '#111318',
  nuitCarte2: '#14181e',
  nuitBord: '#23262d',
  nuitBordContacts: '#1f3b4c',
  nuitTexte: '#f4f5f7',
  nuitGris: '#8b9098',
  nuitGrisFonce: '#5d626b',
  nuitBouton: '#1a1c21',
  nuitBoutonBord: '#2c2f36',
  nuitPiste: '#23262d',
} as const;

export const SANS = "'Inter', system-ui, -apple-system, 'Helvetica Neue', Arial, sans-serif";
export const MONO = "'JetBrains Mono', ui-monospace, 'SF Mono', Menlo, monospace";

export const W = 1080;
export const H = 1920;
export const MARGE = 72;
