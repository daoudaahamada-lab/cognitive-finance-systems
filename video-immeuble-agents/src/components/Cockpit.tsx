import React from 'react';
import {Img, interpolateColors, staticFile} from 'remotion';
import {easeIn, easeInOut, easeOut, piste, prog} from '../anim';
import {CAPTURES} from '../data';
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
      <span style={{display: 'block', transform: `translateY(${(1 - p) * 100}%)`}}>{v}</span>
      {p < 1 ? (
        <span style={{position: 'absolute', left: 0, top: 0, transform: `translateY(${-p * 100}%)`}}>{v - 1}</span>
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
  return (
    <div style={{position: 'relative', width: 66, height: 66}}>
      {plus && d < 18 ? (
        <div
          style={{
            position: 'absolute',
            left: 33 - (33 + d * 3.2),
            top: 33 - (33 + d * 3.2),
            width: (33 + d * 3.2) * 2,
            height: (33 + d * 3.2) * 2,
            borderRadius: 999,
            border: `3px solid ${C.accent}`,
            opacity: 0.7 * (1 - d / 18),
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
      {/* +1 qui s'envole */}
      {plus
        ? taps
            .filter((tp) => f >= tp && f - tp < 24)
            .map((tp) => {
              const e = f - tp;
              return (
                <div
                  key={tp}
                  style={{
                    position: 'absolute',
                    left: 0,
                    right: 0,
                    top: -44 - e * 2.6,
                    textAlign: 'center',
                    fontFamily: MONO,
                    fontSize: 34,
                    fontWeight: 700,
                    color: C.accent,
                    opacity: e < 4 ? e / 4 : 1 - (e - 4) / 20,
                  }}
                >
                  +1
                </div>
              );
            })
        : null}
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
  const atteint = cible !== undefined && v >= cible;
  return (
    <div
      style={{
        background: C.nuitCarte2,
        border: `2px solid ${atteint ? C.accent : C.nuitBord}`,
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

// --- Cockpit recréé en vectoriel (repris de la capture mobile 13) ----------

const CockpitVectoriel: React.FC<{f: number}> = ({f}) => {
  const contactsTaps = [...COCKPIT.invitations, ...COCKPIT.relances].sort((a, b) => a - b);
  const contacts = valeur(f, contactsTaps);
  const tContacts = dernier(f, contactsTaps);
  const objectifsTaps = [contactsTaps[3], COCKPIT.commentaires[4], COCKPIT.post[0]];
  const objectifs = valeur(f, objectifsTaps);
  const tObjectifs = dernier(f, objectifsTaps);
  const serie = valeur(f, COCKPIT.serie);
  const complet = prog(f, COCKPIT.post[0], 12, easeOut);
  const contactsOk = contacts >= 4;
  return (
    <div style={{padding: '40px 44px', fontFamily: SANS, color: C.nuitTexte}}>
      {/* barre du haut */}
      <div style={{display: 'flex', alignItems: 'center', gap: 22}}>
        <span style={{width: 18, height: 18, borderRadius: 9, background: C.accent}} />
        <span style={{fontSize: 36, fontWeight: 800, letterSpacing: '-0.02em'}}>Cockpit</span>
        <div
          style={{
            marginLeft: 'auto',
            display: 'flex',
            gap: 6,
            padding: 6,
            border: `2px solid ${C.nuitBord}`,
            borderRadius: 20,
            fontSize: 24,
          }}
        >
          <span style={{padding: '9px 20px', borderRadius: 15, background: '#1b1e24', border: '2px solid #34373e'}}>Aujourd’hui</span>
          <span style={{padding: '11px 18px', color: C.nuitGris}}>Atelier</span>
          <span style={{padding: '11px 18px', color: C.nuitGris}}>Projets</span>
        </div>
      </div>
      <div style={{height: 2, background: '#16191f', margin: '30px -44px 34px'}} />
      <div style={{fontSize: 22, fontWeight: 700, letterSpacing: '0.2em', color: C.nuitGrisFonce}}>MARDI 13 OCTOBRE</div>
      <div style={{fontSize: 54, fontWeight: 800, letterSpacing: '-0.035em', lineHeight: 1.08, marginTop: 14}}>
        Moteur du jour :{' '}
        <span style={{fontFamily: SANS, color: interpolateColors(complet, [0, 1], [C.nuitTexte, C.accent])}}>
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

        {/* Contacts du jour */}
        <div
          style={{
            marginTop: 22,
            background: '#121920',
            border: `2px solid ${contactsOk ? C.accent : C.nuitBordContacts}`,
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
              textAlign: 'center',
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

// --- Scène 5 : montage des captures desktop puis compteurs ------------------

const LARGEUR = 960;
const MONTAGE = [CAPTURES.cockpitProjets, CAPTURES.cockpitAtelier, CAPTURES.cockpitAujourdhui];

export const Cockpit: React.FC<{f: number}> = ({f}) => {
  const top = piste(f, [
    [COCKPIT.entree, 1920],
    [COCKPIT.entree + 32, 690],
    [COCKPIT.morphose, 690],
    [COCKPIT.morphose + 30, 370],
  ]);
  const hauteur = piste(f, [
    [COCKPIT.morphose, 540],
    [COCKPIT.morphose + 30, 1470],
  ]);
  const sortie = prog(f, COCKPIT.sortie, 22, easeIn);
  const index = piste(f, [
    [COCKPIT.bascules[0], 0],
    [COCKPIT.bascules[0] + 12, 1],
    [COCKPIT.bascules[1], 1],
    [COCKPIT.bascules[1] + 12, 2],
  ]);
  const zoom = piste(f, [
    [COCKPIT.zoom, 1],
    [COCKPIT.zoom + 22, 1.45],
  ]);
  const montage = 1 - prog(f, COCKPIT.morphose, 16, easeInOut);
  const vecteur = prog(f, COCKPIT.vecteur, 20, easeOut);
  if (sortie >= 1) return null;
  return (
    <div
      style={{
        position: 'absolute',
        left: 60,
        width: LARGEUR,
        top: top + sortie * 100,
        height: hauteur,
        borderRadius: 40,
        overflow: 'hidden',
        background: C.nuit,
        border: '1px solid #1c1f26',
        boxShadow: '0 40px 90px rgba(20, 16, 10, 0.28), 0 8px 20px rgba(20, 16, 10, 0.12)',
        opacity: 1 - sortie,
        transform: `scale(${1 - 0.04 * sortie})`,
      }}
    >
      {montage > 0 ? (
        <div style={{position: 'absolute', left: 0, top: 0, width: LARGEUR, height: 540, opacity: montage, overflow: 'hidden'}}>
          <div style={{position: 'absolute', left: -index * LARGEUR, top: 0, width: LARGEUR * 3, height: 540, display: 'flex'}}>
            {MONTAGE.map((src, i) => (
              <div key={src} style={{width: LARGEUR, height: 540, overflow: 'hidden', position: 'relative'}}>
                <Img
                  src={staticFile(src)}
                  style={{
                    width: LARGEUR,
                    height: 540,
                    transformOrigin: '480px 186px',
                    transform: i === 2 ? `scale(${zoom})` : undefined,
                  }}
                />
              </div>
            ))}
          </div>
        </div>
      ) : null}
      {vecteur > 0 ? (
        <div style={{position: 'absolute', left: 0, top: 0, width: LARGEUR, opacity: vecteur, transform: `translateY(${(1 - vecteur) * 40}px)`}}>
          <CockpitVectoriel f={f} />
        </div>
      ) : null}
    </div>
  );
};
