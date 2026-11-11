import type React from 'react';
import {interpolate, useCurrentFrame, useVideoConfig} from 'remotion';

// Franja decorativa con motivo de rombos que se desplaza lentamente.
// useCurrentFrame() vive aquí, en el componente más pequeño que lo necesita
// (lineamiento remotion-markup: "Keep useCurrentFrame() in the smallest component").
export const PatternBand: React.FC<{
  readonly colorA: string;
  readonly colorB: string;
  readonly style?: React.CSSProperties;
}> = ({colorA, colorB, style}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  return (
    <div style={{position: 'absolute', left: 0, width: 1080, height: 56, overflow: 'hidden', ...style}}>
      <svg
        width={1240}
        height={56}
        // Decoración en bucle (no editable en Studio): el módulo hace el desplazamiento infinito.
        style={{translate: `${-(interpolate(frame, [0, fps], [0, 20]) % 40)}px 0px`}}
      >
        <rect width={1240} height={56} fill={colorA} />
        {Array.from({length: 32}).map((_, i) => (
          <path key={i} d={`M ${i * 40} 28 l 20 -20 l 20 20 l -20 20 Z`} fill={colorB} />
        ))}
      </svg>
    </div>
  );
};
