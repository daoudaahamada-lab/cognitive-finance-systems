import React from 'react';
import {interpolateColors} from 'remotion';
import {easeIn, easeInOut, easeOut, prog} from '../anim';
import {C, MONO, SANS} from '../theme';
import {COCKPIT} from '../timeline';

// --- Compteurs -------------------------------------------------------------

const valeur = (f: number, taps: readonly number[]) => taps.filter((t) => f >= t).length;
const dernier = (f: number, taps: readonly number[]) => {
  const passes = taps.filter((t) => f >= t);
  return passes.length ? passes[passes.length - 1] : -1;
};

// Chiffre qui roule : l'ancien sort par le haut, le nouveau entre par le bas.
const Roulant: React.FC<{f: number; v: number; depuis: number; taille: number; couleur?: string}> = ({
  f,
  v,
  depuis,
  taille,
  couleur,
}) => {
  const p = depuis < 0 ? 1 : prog(f, depuis, 9, easeOut);
  return (
    <span
      style={{
        position: 'relative',
        display: 'inline-block',
        height: taille * 1.18,
        lineHeight: `${taille * 1.18}px`,
        overflow: 'hidden',
        verticalAlign: 'bottom',
        color: couleur,
      }}
    >
      <span style={{display: 'block', transform: `translateY(${(1 - p) * 100}%)`, opacity: 0.3 + 0.7 * p}}>{v}</span>
      {p < 1 ? (
        <span style={{position: 'absolute', left: 0, top: 0, transform: `translateY(${-p * 100}%)`, opacity: 1 - p}}>{v - 1}</span>
      ) : null}
    </span>
  );
};

const Barre: React.FC<{f: number; v: number; cible: number; depuis: number}> = ({f, v, cible, depuis}) => {
  const p = depuis < 0 ? 1 : prog(f, depuis, 10, easeOut);
  const largeur = (Math.max(0, v - 1 + p) / cible) * 100;
  return (
    <div style={{height: 10, borderRadius: 99, background: C.nuitPiste, overflow: 'hidden'}}>
      <div style={{height: '100%', width: `${v === 0 ? 0 : largeur}%`, borderRadius: 99, background: C.accent}} />
    </div>
  );
};

const Bouton: React.FC<{plus?: boolean; f?: number; taps?: readonly number[]}> = ({plus, f = 0, taps = []}) => {
  const t = dernier(f, taps);
  const d = t < 0 ? 99 : f - t;
  const appui = d < 8 ? 1 - 0.1 * Math.sin((Math.PI * d) / 8) : 1;
  const onde = 33 + d * 1.6;
  return (
    <div style={{position: 'relative', width: 66, height: 66}}>
      {plus && d < 14 ? (
        <div
          style={{
            position: 'absolute',
            left: 33 - onde,
            top: 33 - onde,
            width: onde * 2,
            height: onde * 2,
            borderRadius: 999,
            border: `3px solid ${C.accent}`,
            opacity: 0.7 * (1 - d / 14),
          }}
        />
      ) : null}
      <div
        style={{
          width: 66,
          height: 66,
          borderRadius: 18,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: 38,
          fontWeight: 600,
          transform: `scale(${appui})`,
          background: plus ? interpolateColors(d < 10 ? 1 - d / 10 : 0, [0, 1], ['#f4f5f8', '#dfe8ff']) : C.nuitBouton,
          border: plus ? 'none' : `2px solid ${C.nuitBoutonBord}`,
          color: plus ? '#0b0d12' : C.nuitTexte,
        }}
      >
        {plus ? '+' : '−'}
      </div>
      {/* +1 qui s'envole : seul le dernier appui est affiché, pour rester lisible */}
      {plus && d < 20 ? (
        <div
          style={{
            position: 'absolute',
            left: 0,
            right: 0,
            top: -44 - d * 3,
            textAlign: 'center',
            fontFamily: MONO,
            fontSize: 34,
            fontWeight: 700,
            color: C.accent,
            opacity: d < 2 ? 0.6 + 0.2 * d : 1 - (d - 2) / 18,
            transform: `scale(${d < 4 ? 1.15 - (0.15 * d) / 4 : 1})`,
          }}
        >
          +1
        </div>
      ) : null}
    </div>
  );
};

const CarteCompteur: React.FC<{
  f: number;
  titre: string;
  sous: string;
  taps: readonly number[];
  cible?: number;
}> = ({f, titre, sous, taps, cible}) => {
  const v = valeur(f, taps);
  const t = dernier(f, taps);
  const tAtteinte = cible !== undefined && taps.length >= cible ? taps[cible - 1] : 1e9;
  const bord = interpolateColors(prog(f, tAtteinte + 4, 8), [0, 1], [C.nuitBord, C.accent]);
  return (
    <div
      style={{
        background: C.nuitCarte2,
        border: `2px solid ${bord}`,
        borderRadius: 26,
        padding: '24px 24px 22px',
      }}
    >
      <div style={{fontSize: 26, fontWeight: 500, color: '#c9ccd2'}}>{titre}</div>
      <div style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between', margin: '26px 0 20px'}}>
        <Bouton />
        <div style={{fontFamily: MONO, fontSize: 64, fontWeight: 700, color: C.nuitTexte, display: 'flex', alignItems: 'flex-end'}}>
          <Roulant f={f} v={v} depuis={t} taille={64} />
          {cible !== undefined ? <span style={{fontSize: 30, color: C.nuitGrisFonce, marginBottom: 8, marginLeft: 2}}>/{cible}</span> : null}
        </div>
        <Bouton plus f={f} taps={taps} />
      </div>
      {cible !== undefined ? <Barre f={f} v={v} cible={cible} depuis={t} /> : <div style={{height: 10}} />}
      <div style={{fontSize: 22, color: C.nuitGris, marginTop: 14}}>{sous}</div>
    </div>
  );
};

// --- En-tête du cockpit (commun au montage et aux compteurs) ---------------

// Onglets à largeur fixe pour que la pastille active glisse de l'un à l'autre.
const ONGLETS = [
  {nom: 'Aujourd’hui', x: 0, w: 176},
  {nom: 'Atelier', x: 182, w: 120},
  {nom: 'Projets', x: 308, w: 126},
];
const HAUT_ENTETE = 138;

const EnTete: React.FC<{actif: number}> = ({actif}) => {
  const k = Math.max(0, Math.min(ONGLETS.length - 1.0001, actif));
  const a = ONGLETS[Math.floor(k)];
  const b = ONGLETS[Math.ceil(k)];
  const t = k - Math.floor(k);
  return (
    <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: HAUT_ENTETE, fontFamily: SANS, color: C.nuitTexte}}>
      <div style={{display: 'flex', alignItems: 'center', gap: 22, padding: '38px 44px 0'}}>
        <span style={{width: 18, height: 18, borderRadius: 9, background: C.accent}} />
        <span style={{fontSize: 36, fontWeight: 800, letterSpacing: '-0.02em'}}>Cockpit</span>
        <div
          style={{
            marginLeft: 'auto',
            position: 'relative',
            width: 434,
            height: 56,
            padding: 6,
            border: `2px solid ${C.nuitBord}`,
            borderRadius: 20,
            boxSizing: 'content-box',
          }}
        >
          <div
            style={{
              position: 'absolute',
              top: 6,
              left: 6 + a.x + (b.x - a.x) * t,
              width: a.w + (b.w - a.w) * t,
              height: 56,
              borderRadius: 15,
              background: '#1b1e24',
              border: '2px solid #34373e',
              boxSizing: 'border-box',
            }}
          />
          {ONGLETS.map((o, i) => (
            <div
              key={o.nom}
              style={{
                position: 'absolute',
                top: 6,
                left: 6 + o.x,
                width: o.w,
                height: 56,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: 24,
                color: interpolateColors(Math.max(0, 1 - Math.abs(actif - i)), [0, 1], [C.nuitGris, C.nuitTexte]),
              }}
            >
              {o.nom}
            </div>
          ))}
        </div>
      </div>
      <div style={{position: 'absolute', left: 0, right: 0, bottom: 0, height: 2, background: '#16191f'}} />
    </div>
  );
};

// --- Compteurs recréés en vectoriel (d'après la capture mobile 13) ----------

const CorpsCompteurs: React.FC<{f: number}> = ({f}) => {
  const contactsTaps = [...COCKPIT.invitations, ...COCKPIT.relances].sort((a, b) => a - b);
  const contacts = valeur(f, contactsTaps);
  const tContacts = dernier(f, contactsTaps);
  // chaque objectif est validé un court instant après le dernier appui qui l'atteint
  const objectifsTaps = [contactsTaps[3] + 8, COCKPIT.commentaires[4] + 6, COCKPIT.post[0] + 6];
  const objectifs = valeur(f, objectifsTaps);
  const tObjectifs = dernier(f, objectifsTaps);
  const serie = valeur(f, COCKPIT.serie);
  const complet = prog(f, objectifsTaps[2], 12, easeOut);
  const bordContacts = interpolateColors(prog(f, contactsTaps[3] + 4, 8), [0, 1], [C.nuitBordContacts, C.accent]);
  return (
    <div style={{padding: '34px 44px 40px', fontFamily: SANS, color: C.nuitTexte}}>
      <div style={{fontSize: 22, fontWeight: 700, letterSpacing: '0.2em', color: C.nuitGrisFonce}}>MARDI 13 OCTOBRE</div>
      <div style={{fontSize: 54, fontWeight: 800, letterSpacing: '-0.035em', lineHeight: 1.08, marginTop: 14}}>
        Moteur du jour{'\u00a0'}:{' '}
        <span style={{color: interpolateColors(complet, [0, 1], [C.nuitTexte, C.accent])}}>
          <Roulant f={f} v={objectifs} depuis={tObjectifs} taille={54} />
          /3
        </span>{' '}
        objectifs atteints
      </div>

      <div
        style={{
          marginTop: 34,
          background: C.nuitCarte,
          border: `2px solid ${C.nuitBord}`,
          borderRadius: 34,
          padding: '30px 30px 32px',
        }}
      >
        <div style={{fontSize: 22, fontWeight: 700, letterSpacing: '0.18em', color: C.nuitGrisFonce}}>AGENTIC WEALTH · AUJOURD’HUI</div>
        <div style={{display: 'flex', alignItems: 'center', gap: 22, marginTop: 18}}>
          <span style={{fontFamily: MONO, fontSize: 72, fontWeight: 700}}>
            <Roulant f={f} v={serie} depuis={dernier(f, COCKPIT.serie)} taille={72} />
          </span>
          <span style={{fontSize: 25, color: C.nuitGris, lineHeight: 1.3}}>
            jour ouvré d’affilée
            <br />à 4 contacts
          </span>
        </div>

        {/* Contacts du jour = invitations + relances */}
        <div
          style={{
            marginTop: 22,
            background: '#121920',
            border: `2px solid ${bordContacts}`,
            borderRadius: 28,
            padding: '24px 30px 24px',
          }}
        >
          <div style={{fontSize: 26, color: '#c9ccd2'}}>Contacts du jour</div>
          <div
            style={{
              fontFamily: MONO,
              fontSize: 92,
              fontWeight: 700,
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'flex-end',
              margin: '4px 0 14px',
            }}
          >
            <Roulant f={f} v={contacts} depuis={tContacts} taille={92} />
            <span style={{fontSize: 38, color: C.nuitGrisFonce, marginBottom: 14, marginLeft: 4}}>/4</span>
          </div>
          <Barre f={f} v={contacts} cible={4} depuis={tContacts} />
          <div style={{fontSize: 22, color: C.nuitGris, marginTop: 14}}>Invitations + relances</div>
        </div>

        <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20, marginTop: 20}}>
          <CarteCompteur f={f} titre="Invitations et emails" sous="Nouveaux CGP" taps={COCKPIT.invitations} />
          <CarteCompteur f={f} titre="Relances" sous="CGP déjà contactés" taps={COCKPIT.relances} />
          <CarteCompteur f={f} titre="Commentaires CGP" sous="15 min" taps={COCKPIT.commentaires} cible={5} />
          <CarteCompteur f={f} titre="Post publié" sous="Validé dans Metricool" taps={COCKPIT.post} cible={1} />
        </div>
      </div>
    </div>
  );
};

// --- Étape 5 : la carte du cockpit monte, les compteurs du jour avancent ---

export const CarteCockpit: React.FC<{f: number}> = ({f}) => {
  const entree = prog(f, COCKPIT.entree, 26, easeOut);
  const sortie = prog(f, COCKPIT.sortie - 12, 9, easeIn);
  if (entree <= 0 || sortie >= 1) return null;
  const top = 1920 - (1920 - 372) * entree + sortie * 80;
  return (
    <div
      style={{
        position: 'absolute',
        left: 60,
        top,
        width: 960,
        height: 1420,
        borderRadius: 40,
        overflow: 'hidden',
        background: C.nuit,
        boxShadow: '0 40px 90px rgba(20, 16, 10, 0.26), 0 8px 20px rgba(20, 16, 10, 0.12)',
        opacity: 1 - sortie,
      }}
    >
      <EnTete actif={0} />
      <div style={{position: 'absolute', left: 0, top: HAUT_ENTETE, width: 960}}>
        <CorpsCompteurs f={f} />
      </div>
    </div>
  );
};
