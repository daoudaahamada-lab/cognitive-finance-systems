// Reusable explainer composition: every video is described entirely by its props (build/Vxx/motion.json).
import {AbsoluteFill} from 'remotion';
import {Background} from './Background';
import {Captions} from './Captions';
import {EndCard} from './EndCard';
import {HeroLayer} from './Hero';
import {OverlayLayer} from './Overlays';
import {StepIndicator} from './StepIndicator';
import type {ExplainerProps} from './types';

export const Explainer: React.FC<ExplainerProps> = (props) => {
  const {style, width, height, shots, assets, overlays} = props;
  const layer = {overlays, shots, assets, style, width, height};
  return (
    <AbsoluteFill style={{backgroundColor: style.bg}}>
      <Background src={props.background} color={style.bg} />
      <OverlayLayer {...layer} layer="behind" />
      {props.steps ? <StepIndicator steps={props.steps} style={style} width={width} layer="behind" /> : null}
      <HeroLayer shots={shots} assets={assets} style={style} />
      <OverlayLayer {...layer} layer="front" />
      {props.steps ? <StepIndicator steps={props.steps} style={style} width={width} layer="front" /> : null}
      {props.endCard ? <EndCard card={props.endCard} style={style} /> : null}
      <Captions groups={props.captions} style={style} width={width} height={height} />
    </AbsoluteFill>
  );
};
