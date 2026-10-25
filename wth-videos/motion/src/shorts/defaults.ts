// Studio preview / default props of the "Short" composition: S01 of wth-videos/shorts/shorts.json (the render
// script pipeline/shorts.py passes each short object of that file as props).
import type {ShortProps} from './types';

export const defaultShortProps: ShortProps = {
  "id": "S01",
  "titre": "Mes 5 applis pour commencer à investir",
  "accroche": "Mon dossier « Finances », ouvert.",
  "elements": [
    {
      "nom": "Trade Republic",
      "couleur": "#1E1416",
      "role": "Actions et ETF, même avec de petits montants",
      "geste": "une pièce tombe dans un panier de 3 mini-courbes"
    },
    {
      "nom": "Bitstack",
      "couleur": "#2F4BFF",
      "role": "J'arrondis mes achats en bitcoin",
      "geste": "4,60 € → 5,00 € : les 0,40 € filent dans une pièce ₿"
    },
    {
      "nom": "Exodus",
      "couleur": "#2A1B6E",
      "role": "Mon coffre crypto : mes clés, chez moi",
      "geste": "une clé entre dans un coffre qui se ferme"
    },
    {
      "nom": "Trust Wallet",
      "couleur": "#0500FF",
      "role": "Un portefeuille, plusieurs blockchains",
      "geste": "un portefeuille relie 3 petits réseaux"
    },
    {
      "nom": "LiveCoinWatch",
      "couleur": "#3CC7C0",
      "role": "Je suis les cours, sans rien acheter",
      "geste": "une courbe se dessine sous une loupe"
    }
  ],
  "fin": "Ce n'est pas un conseil en investissement. Crypto : risque de perte totale."
};
