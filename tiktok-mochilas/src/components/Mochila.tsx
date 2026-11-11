import type React from 'react';
import {Interactive} from 'remotion';

type MochilaProps = {
  readonly base: string;
  readonly pattern: string;
  readonly accent: string;
  readonly style: React.CSSProperties;
};

// Ilustración de una mochila tejida. Es un marcador de posición:
// reemplázala por fotos reales del producto con <CanvasImage src={staticFile('mochila.jpg')} />.
const MochilaInner = ({base, pattern, accent, style}: MochilaProps) => {
  return (
    <svg viewBox="0 0 400 540" style={{overflow: 'visible', ...style}}>
      <defs>
        <clipPath id="mochila-body">
          <path d="M 70 190 L 330 190 C 348 320 348 420 332 470 Q 200 525 68 470 C 52 420 52 320 70 190 Z" />
        </clipPath>
      </defs>

      {/* Gaza (correa) tejida */}
      <path
        d="M 92 200 C 50 -30, 350 -30, 308 200"
        fill="none"
        stroke={accent}
        strokeWidth={26}
        strokeLinecap="round"
      />
      <path
        d="M 92 200 C 50 -30, 350 -30, 308 200"
        fill="none"
        stroke={base}
        strokeWidth={8}
        strokeDasharray="14 12"
      />

      {/* Cuerpo */}
      <path
        d="M 70 190 L 330 190 C 348 320 348 420 332 470 Q 200 525 68 470 C 52 420 52 320 70 190 Z"
        fill={base}
      />

      {/* Franjas geométricas recortadas al cuerpo (plantilla: se generan en bucle) */}
      <g clipPath="url(#mochila-body)">
        {[250, 345, 440].map((y, row) => (
          <g key={y}>
            <rect x={40} y={y - 34} width={320} height={68} fill={row === 1 ? accent : pattern} />
            {Array.from({length: 9}).map((_, i) => (
              <path
                key={i}
                d={`M ${40 + i * 40} ${y} l 20 -22 l 20 22 l -20 22 Z`}
                fill={row === 1 ? pattern : accent}
              />
            ))}
            {Array.from({length: 9}).map((_, i) => (
              <circle key={`d${i}`} cx={60 + i * 40} cy={y} r={5} fill={base} />
            ))}
          </g>
        ))}
        {/* Textura de tejido */}
        {Array.from({length: 40}).map((_, i) => (
          <line
            key={`t${i}`}
            x1={40}
            x2={360}
            y1={190 + i * 9}
            y2={190 + i * 9}
            stroke="#000"
            strokeOpacity={0.06}
            strokeWidth={2}
          />
        ))}
      </g>

      {/* Boca de la mochila y cordón */}
      <ellipse cx={200} cy={190} rx={130} ry={24} fill={pattern} />
      <ellipse cx={200} cy={186} rx={116} ry={15} fill="#2a1d15" opacity={0.55} />
      <path d="M 120 196 Q 200 222 280 196" fill="none" stroke={accent} strokeWidth={6} />
      <path d="M 200 214 L 188 268 M 200 214 L 214 270" stroke={accent} strokeWidth={5} />
      <circle cx={187} cy={274} r={9} fill={pattern} />
      <circle cx={215} cy={276} r={9} fill={pattern} />

      {/* Borlas */}
      <path d="M 88 196 l -14 70 l 28 0 Z" fill={accent} />
      <path d="M 312 196 l -14 70 l 28 0 Z" fill={accent} />
    </svg>
  );
};

export const Mochila = Interactive.create({
  Component: MochilaInner,
  layout: 'none',
  schema: {
    base: {type: 'color', default: '#F4EBDD', description: 'Color base'},
    pattern: {type: 'color', default: '#C4532D', description: 'Color del patrón'},
    accent: {type: 'color', default: '#2F5D50', description: 'Color de acento'},
  },
});
