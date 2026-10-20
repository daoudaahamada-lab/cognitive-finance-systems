import {AbsoluteFill, Img, staticFile, useCurrentFrame} from 'remotion';
import {exitSpan, heroPose} from './pose';
import type {Asset, Shot, Style} from './types';

/**
 * Glass illustrations. Each asset is one RGBA image with its halo baked in (pipeline/motion.py), so the glow
 * follows every transform and can never show a rectangle. The image is laid out at its displayed size
 * (no CSS scale) so Chrome resamples it once, with mipmaps, and never above source resolution.
 * The layer fades out above the caption band so the hero never fights the caption.
 */
export const HeroLayer: React.FC<{shots: Shot[]; assets: Record<string, Asset>; style: Style}> = ({
  shots,
  assets,
  style,
}) => {
  const frame = useCurrentFrame();
  const m = style.hero_mask;
  const mask = `linear-gradient(to bottom, transparent ${m.top0}px, black ${m.top1}px, black ${m.bottom0}px, transparent ${m.bottom1}px)`;
  return (
    <AbsoluteFill style={{maskImage: mask, WebkitMaskImage: mask}}>
      {shots.map((shot, i) => {
        const asset = assets[shot.asset];
        // Keep the image mounted a little before / after it shows, so it is decoded when needed.
        const mounted = frame >= shot.from - 2 && frame < shot.to + exitSpan(shot, style) + 2;
        if (!mounted) return null;
        const pose = heroPose(shot, asset, style, frame, i === shots.length - 1);
        const filter =
          pose.brightness !== 1 || pose.saturate !== 1
            ? `brightness(${pose.brightness.toFixed(4)}) saturate(${pose.saturate.toFixed(4)})`
            : undefined;
        return (
          <Img
            key={shot.id}
            src={staticFile(asset.src)}
            style={{
              position: 'absolute',
              left: 0,
              top: 0,
              width: asset.w * pose.k,
              height: asset.h * pose.k,
              opacity: pose.visible ? pose.opacity : 0,
              transformOrigin: `${pose.fx * pose.k}px ${pose.fy * pose.k}px`,
              transform: `translate(${pose.x}px, ${pose.y}px) rotate(${pose.rot}deg)`,
              filter,
            }}
          />
        );
      })}
    </AbsoluteFill>
  );
};
