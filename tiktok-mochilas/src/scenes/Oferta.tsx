import {Easing, Interactive, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {bodyFont, titleFont} from '../fonts';

// Escena 4 — La oferta que insta a comprar. Urgencia + número grande.
const OfertaInner = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  return (
    <>
      <Interactive.Div
        name="Urgencia"
        style={{
          fontFamily: bodyFont,
          fontWeight: 700,
          fontSize: 56,
          letterSpacing: 4,
          color: '#F4EBDD',
          backgroundColor: '#3B2A20',
          borderRadius: 999,
          padding: '18px 44px',
          opacity: interpolate(frame, [0, 0.3 * fps], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          }),
        }}
      >
        SOLO ESTA SEMANA
      </Interactive.Div>

      <Interactive.Div
        name="Descuento"
        style={{
          fontFamily: titleFont,
          fontWeight: 900,
          fontSize: 300,
          lineHeight: 1,
          color: '#3B2A20',
          marginTop: 40,
          scale: interpolate(frame, [0.2 * fps, 0.7 * fps, 1.6 * fps, 2 * fps], [0, 1, 1, 1.08], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: Easing.spring({damping: 10}),
            output: 'perceptual-scale',
          }),
        }}
      >
        -20%
      </Interactive.Div>

      <Interactive.Div
        name="Detalle oferta"
        style={{
          fontFamily: bodyFont,
          fontWeight: 700,
          fontSize: 60,
          color: '#3B2A20',
          textAlign: 'center',
          width: 820,
          opacity: interpolate(frame, [0.7 * fps, 1 * fps], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          }),
        }}
      >
        en todas las mochilas
      </Interactive.Div>

      <Interactive.Div
        name="Sello unidades"
        style={{
          fontFamily: bodyFont,
          fontWeight: 700,
          fontSize: 44,
          lineHeight: 1.1,
          color: '#F4EBDD',
          backgroundColor: '#C4532D',
          width: 260,
          height: 260,
          borderRadius: 999,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          textAlign: 'center',
          marginTop: 60,
          rotate: interpolate(frame, [1 * fps, 1.5 * fps], ['-40deg', '-10deg'], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: Easing.spring({damping: 12}),
          }),
          scale: interpolate(frame, [1 * fps, 1.5 * fps], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: Easing.spring({damping: 12}),
            output: 'perceptual-scale',
          }),
        }}
      >
        Unidades limitadas
      </Interactive.Div>
    </>
  );
};

export const Oferta = Interactive.create({
  Component: OfertaInner,
  layout: 'absolute-fill',
  schema: {
    ...Interactive.backgroundSchema,
  },
});
