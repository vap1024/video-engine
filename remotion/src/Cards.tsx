import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame, interpolate, spring, useVideoConfig} from 'remotion';

const FONT = "'Noto Sans','DejaVu Sans',sans-serif";

const Paw: React.FC<{x: number; y: number; s: number; rot: number; op: number}> = ({x, y, s, rot, op}) => (
  <svg width={60 * s} height={56 * s} style={{position: 'absolute', left: x, top: y, transform: `rotate(${rot}deg)`, opacity: op}}>
    <ellipse cx="30" cy="38" rx="15" ry="12" fill="#fff" />
    <ellipse cx="8" cy="22" rx="6.5" ry="8.5" fill="#fff" />
    <ellipse cx="21" cy="12" rx="6.5" ry="9" fill="#fff" />
    <ellipse cx="36" cy="11" rx="6.5" ry="9" fill="#fff" />
    <ellipse cx="50" cy="20" rx="6.5" ry="8.5" fill="#fff" />
  </svg>
);

export const TitleCard: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const sp = spring({frame, fps, config: {damping: 14}});
  const titleY = interpolate(sp, [0, 1], [60, 0]);
  const subOp = interpolate(frame, [25, 45], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const fade = interpolate(frame, [135, 150], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{backgroundColor: '#17100b', opacity: fade}}>
      <Img src={staticFile('cat-group.webp')} style={{width: '100%', height: '100%', objectFit: 'cover', opacity: 0.45}} />
      <AbsoluteFill style={{background: 'linear-gradient(90deg, rgba(15,9,5,0.88) 30%, rgba(15,9,5,0.15))'}} />
      <div style={{position: 'absolute', left: 80, top: 215, transform: `translateY(${titleY}px)`, opacity: sp}}>
        <div style={{fontFamily: FONT, fontWeight: 900, fontSize: 118, color: '#fff', letterSpacing: 2, lineHeight: 1}}>КОТИКИ</div>
        <div style={{fontFamily: FONT, fontWeight: 700, fontSize: 34, color: '#ffb066', marginTop: 22, opacity: subOp}}>
          тест движка · 60 секунд про главных
        </div>
        <div style={{fontFamily: FONT, fontSize: 22, color: 'rgba(255,255,255,0.75)', marginTop: 12, opacity: subOp}}>
          смонтировано кодом: FFmpeg + Whisper + Remotion
        </div>
      </div>
      <Paw x={1080} y={90} s={1.1} rot={24} op={0.5} />
      <Paw x={1150} y={180} s={0.8} rot={10} op={0.35} />
    </AbsoluteFill>
  );
};

export const EndCard: React.FC = () => {
  const frame = useCurrentFrame();
  const op = interpolate(frame, [0, 20], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{backgroundColor: '#17100b', opacity: op}}>
      <Img src={staticFile('cat-group.webp')} style={{width: '100%', height: '100%', objectFit: 'cover', opacity: 0.3}} />
      <AbsoluteFill style={{background: 'radial-gradient(circle at 50% 45%, rgba(15,9,5,0.25), rgba(15,9,5,0.92))'}} />
      <div style={{position: 'absolute', width: '100%', top: 265, textAlign: 'center'}}>
        <div style={{fontFamily: FONT, fontWeight: 900, fontSize: 56, color: '#fff'}}>Движок собран</div>
        <div style={{fontFamily: FONT, fontWeight: 700, fontSize: 28, color: '#ffb066', marginTop: 16}}>Дальше — твоё видео</div>
      </div>
      <Paw x={600} y={470} s={0.9} rot={-14} op={0.5} />
    </AbsoluteFill>
  );
};

export const LowerThird: React.FC<{name: string; role: string; color: string}> = ({name, role, color}) => (
  <AbsoluteFill>
    <div style={{position: 'absolute', left: 56, bottom: 118, display: 'flex', alignItems: 'stretch'}}>
      <div style={{width: 10, backgroundColor: color, borderRadius: 4}} />
      <div style={{backgroundColor: 'rgba(12,8,5,0.78)', padding: '14px 26px 16px 20px', borderRadius: '0 14px 14px 0'}}>
        <div style={{fontFamily: FONT, fontWeight: 900, fontSize: 40, color: '#fff', letterSpacing: 1.5, lineHeight: 1}}>{name}</div>
        <div style={{fontFamily: FONT, fontWeight: 700, fontSize: 19, color: color, marginTop: 7, letterSpacing: 1}}>{role}</div>
      </div>
    </div>
  </AbsoluteFill>
);
