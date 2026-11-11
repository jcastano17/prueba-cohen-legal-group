import {Easing, Interactive, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {PatternBand} from '../components/PatternBand';
import {bodyFont, titleFont} from '../fonts';

// Escena 1 — Gancho: lo primero que se ve en el feed. Una sola idea por cuadro.
const HookInner = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  return (
    <>
      <PatternBand colorA="#2F5D50" colorB="#E0A526" style={{top: 0}} />

      <Interactive.Div
        name="Kicker"
        style={{
          fontFamily: bodyFont,
          fontWeight: 700,
          fontSize: 48,
          letterSpacing: 6,
          color: '#F4EBDD',
          marginBottom: 40,
          opacity: interpolate(frame, [0, 0.4 * fps], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          }),
        }}
      >
        HECHO EN COLOMBIA
      </Interactive.Div>

      <Interactive.Div
        name="Pregunta gancho"
        style={{
          fontFamily: titleFont,
          fontWeight: 900,
          fontSize: 124,
          lineHeight: 1.02,
          color: '#F4EBDD',
          textAlign: 'center',
          width: 860,
          scale: interpolate(frame, [0.1 * fps, 0.8 * fps], [0.6, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: Easing.spring({damping: 12}),
            output: 'perceptual-scale',
          }),
          opacity: interpolate(frame, [0.1 * fps, 0.4 * fps], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          }),
        }}
      >
        ¿Buscas una mochila que nadie más tenga?
      </Interactive.Div>
    </>
  );
};

export const Hook = Interactive.create({
  Component: HookInner,
  layout: 'absolute-fill',
  schema: {
    ...Interactive.backgroundSchema,
  },
});
