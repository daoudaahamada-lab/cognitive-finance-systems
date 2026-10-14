import {ThreeCanvas} from '@remotion/three';
import {useThree} from '@react-three/fiber';
import React, {useLayoutEffect, useMemo} from 'react';
import * as THREE from 'three';

// Avatar du jeu (« Daouda ») reconstruit en 3D, dans le style low-poly de l'application :
// tête ronde, cheveux et barbe noirs, pull bleu à col roulé, pantalon et chaussures anthracite.
export const COULEURS_AVATAR = {
  peau: '#8f532e',
  cheveux: '#17120e',
  barbe: '#130f0b',
  pull: '#1b59cc',
  pantalon: '#1f222a',
  chaussures: '#0c0d11',
} as const;

export type PlanCamera = {
  azimut: number; // degrés, autour de l'axe vertical (0 = face à l'avatar)
  elevation: number; // degrés
  champ: number; // champ vertical en degrés
  cible: [number, number, number]; // point visé
  echelle: number; // hauteur visible (unités 3D) au niveau de la cible = 2·d·tan(champ/2)
  ecranY: number; // position verticale (px) de la cible à l'écran
};

export const LARGEUR = 1080;
export const HAUTEUR = 1920;

// Construit une caméra three.js à partir d'un plan (utilisée par la scène et pour projeter des étiquettes).
export const cameraDepuisPlan = (p: PlanCamera, cam = new THREE.PerspectiveCamera()) => {
  const d = p.echelle / (2 * Math.tan(THREE.MathUtils.degToRad(p.champ / 2)));
  const az = THREE.MathUtils.degToRad(p.azimut);
  const el = THREE.MathUtils.degToRad(p.elevation);
  const [cx, cy, cz] = p.cible;
  cam.fov = p.champ;
  cam.aspect = LARGEUR / HAUTEUR;
  cam.near = Math.max(0.05, d * 0.05);
  cam.far = d * 10 + 50;
  cam.position.set(cx + d * Math.cos(el) * Math.sin(az), cy + d * Math.sin(el), cz + d * Math.cos(el) * Math.cos(az));
  cam.up.set(0, 1, 0);
  cam.lookAt(cx, cy, cz);
  // décale le cadre pour placer la cible à la hauteur voulue à l'écran
  cam.setViewOffset(LARGEUR, HAUTEUR, 0, -(p.ecranY - HAUTEUR / 2), LARGEUR, HAUTEUR);
  cam.updateProjectionMatrix();
  cam.updateMatrixWorld(true);
  return cam;
};

export const projeter = (p: PlanCamera, point: [number, number, number]) => {
  const cam = cameraDepuisPlan(p);
  const v = new THREE.Vector3(...point).project(cam);
  return {x: ((v.x + 1) / 2) * LARGEUR, y: ((1 - v.y) / 2) * HAUTEUR};
};

const CameraPilotee: React.FC<{plan: PlanCamera}> = ({plan}) => {
  const camera = useThree((s) => s.camera) as THREE.PerspectiveCamera;
  useLayoutEffect(() => {
    cameraDepuisPlan(plan, camera);
  });
  cameraDepuisPlan(plan, camera);
  return null;
};

const Matiere: React.FC<{couleur: string; rugosite?: number}> = ({couleur, rugosite = 0.62}) => (
  <meshStandardMaterial color={couleur} roughness={rugosite} metalness={0} />
);

// Ombre portée douce (texture radiale), comme sous les personnages du jeu.
const OmbreSol: React.FC<{opacite: number}> = ({opacite}) => {
  const texture = useMemo(() => {
    const c = document.createElement('canvas');
    c.width = 256;
    c.height = 256;
    const g = c.getContext('2d')!;
    const grad = g.createRadialGradient(128, 128, 0, 128, 128, 128);
    grad.addColorStop(0, 'rgba(40,36,30,0.55)');
    grad.addColorStop(0.55, 'rgba(40,36,30,0.22)');
    grad.addColorStop(1, 'rgba(40,36,30,0)');
    g.fillStyle = grad;
    g.fillRect(0, 0, 256, 256);
    return new THREE.CanvasTexture(c);
  }, []);
  return (
    <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0.25, 0.002, -0.2]} scale={[1.9, 1.3, 1]}>
      <planeGeometry args={[1, 1]} />
      <meshBasicMaterial map={texture} transparent opacity={opacite} depthWrite={false} />
    </mesh>
  );
};

export const Personnage: React.FC<{respiration: number; tete: number}> = ({respiration, tete}) => {
  const C = COULEURS_AVATAR;
  return (
    <group>
      {/* chaussures et jambes */}
      {[-1, 1].map((s) => (
        <group key={s} position={[s * 0.125, 0, 0]}>
          <mesh position={[0, 0.055, 0.05]} castShadow>
            <boxGeometry args={[0.22, 0.11, 0.36]} />
            <Matiere couleur={C.chaussures} rugosite={0.5} />
          </mesh>
          <mesh position={[0, 0.4, -0.01]} castShadow>
            <boxGeometry args={[0.2, 0.62, 0.24]} />
            <Matiere couleur={C.pantalon} />
          </mesh>
        </group>
      ))}
      {/* buste (pull) avec une légère respiration */}
      <group position={[0, 1.08, 0]} scale={[1, 1 + 0.012 * respiration, 1 + 0.01 * respiration]}>
        <mesh scale={[1, 1, 0.86]} castShadow>
          <capsuleGeometry args={[0.27, 0.32, 10, 28]} />
          <Matiere couleur={C.pull} />
        </mesh>
      </group>
      {/* col roulé */}
      <mesh position={[0, 1.52, 0]} castShadow>
        <cylinderGeometry args={[0.15, 0.17, 0.16, 28]} />
        <Matiere couleur={C.pull} />
      </mesh>
      {/* bras */}
      {[-1, 1].map((s) => (
        <mesh key={s} position={[s * 0.335, 1.13, 0.01]} rotation={[0, 0, s * 0.06]} castShadow>
          <capsuleGeometry args={[0.088, 0.44, 8, 20]} />
          <Matiere couleur={C.pull} />
        </mesh>
      ))}
      {/* tête */}
      <group position={[0, 1.79, 0]} rotation={[0.04 * tete, 0.18 * tete, 0]}>
        <mesh castShadow>
          <sphereGeometry args={[0.29, 40, 32]} />
          <Matiere couleur={C.peau} rugosite={0.55} />
        </mesh>
        {/* cheveux : calotte qui descend plus bas à l'arrière */}
        <mesh rotation={[-0.38, 0, 0]}>
          <sphereGeometry args={[0.302, 40, 24, 0, Math.PI * 2, 0, Math.PI * 0.43]} />
          <Matiere couleur={C.cheveux} rugosite={0.85} />
        </mesh>
        {/* barbe : collier sur la mâchoire et le menton, relié aux cheveux par les pattes */}
        <mesh>
          <sphereGeometry args={[0.297, 40, 20, 0, Math.PI, Math.PI * 0.63, Math.PI * 0.25]} />
          <Matiere couleur={C.barbe} rugosite={0.9} />
        </mesh>
        {[0.01, 0.84].map((debut) => (
          <mesh key={debut}>
            <sphereGeometry args={[0.299, 12, 16, Math.PI * debut, Math.PI * 0.15, Math.PI * 0.36, Math.PI * 0.32]} />
            <Matiere couleur={C.barbe} rugosite={0.9} />
          </mesh>
        ))}
        {/* yeux */}
        {[-1, 1].map((s) => (
          <mesh key={s} position={[s * 0.095, 0.035, 0.27]}>
            <sphereGeometry args={[0.032, 16, 12]} />
            <meshStandardMaterial color="#0d0c0d" roughness={0.3} />
          </mesh>
        ))}
      </group>
    </group>
  );
};

export const SceneAvatar: React.FC<{plan: PlanCamera; respiration: number; tete: number; ombre: number; opacite: number}> = ({
  plan,
  respiration,
  tete,
  ombre,
  opacite,
}) => (
  <ThreeCanvas
    width={LARGEUR}
    height={HAUTEUR}
    style={{position: 'absolute', left: 0, top: 0, opacity: opacite}}
    gl={{alpha: true, antialias: true, preserveDrawingBuffer: true}}
    shadows
  >
    <CameraPilotee plan={plan} />
    <hemisphereLight args={['#ffffff', '#d8d0c2', 1.35]} />
    <directionalLight
      position={[-2.5, 5, 4]}
      intensity={2.1}
      color="#fff4e6"
      castShadow
      shadow-mapSize-width={2048}
      shadow-mapSize-height={2048}
      shadow-camera-left={-3}
      shadow-camera-right={3}
      shadow-camera-top={3}
      shadow-camera-bottom={-3}
      shadow-bias={-0.0004}
    />
    {/* douce lumière de face pour le visage */}
    <directionalLight position={[1.5, 2.2, 5]} intensity={0.75} color="#fff8f0" />
    {/* contre-jour froid pour détacher la silhouette du fond */}
    <directionalLight position={[3, 3.5, -4]} intensity={1.6} color="#d9e5ff" />
    <Personnage respiration={respiration} tete={tete} />
    <OmbreSol opacite={ombre} />
  </ThreeCanvas>
);
