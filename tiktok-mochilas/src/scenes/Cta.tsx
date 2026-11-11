import {Easing, Interactive, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {Mochila} from '../components/Mochila';
import {PatternBand} from '../components/PatternBand';
import {bodyFont, titleFont} from '../fonts';

// Escena 5 — Llamado a la acción: qué hacer ahora y dónde.
const CtaInner = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  return (
    <>
      <PatternBand colorA="#C4532D" colorB="#E0A526" style={{top: 0}} />

      <Mochila
        name="Mochila CTA"
        base="#E0A526"
        pattern="#2F5D50"
        accent="#C4532D"
        style={{
          width: 380,
          marginBottom: 40,
          rotate: interpolate(frame, [0, 1.5 * fps, 3 * fps], ['-6deg', '6deg', '-6deg'], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: Easing.bezier(0.45, 0, 0.55, 1),
          }),
        }}
      />

      <Interactive.Div
        name="Titular CTA"
        style={{
          fontFamily: titleFont,
          fontWeight: 900,
          fontSize: 120,
          lineHeight: 1.02,
          color: '#F4EBDD',
          textAlign: 'center',
          width: 860,
          translate: interpolate(frame, [0, 0.5 * fps], ['0px 80px', '0px 0px'], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: Easing.bezier(0.16, 1, 0.3, 1),
          }),
          opacity: interpolate(frame, [0, 0.4 * fps], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          }),
        }}
      >
        Pide la tuya hoy
      </Interactive.Div>

      <Interactive.Div
        name="Usuario"
        style={{
          fontFamily: bodyFont,
          fontWeight: 700,
          fontSize: 68,
          color: '#3B2A20',
          backgroundColor: '#E0A526',
          borderRadius: 999,
          padding: '22px 56px',
          marginTop: 50,
          scale: interpolate(frame, [0.5 * fps, 0.9 * fps, 2 * fps, 2.3 * fps, 2.6 * fps], [0, 1, 1, 1.06, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: Easing.spring({damping: 12}),
            output: 'perceptual-scale',
          }),
        }}
      >
        @altamariacol
      </Interactive.Div>

      <Interactive.Div
        name="Link en bio"
        style={{
          fontFamily: bodyFont,
          fontWeight: 500,
          fontSize: 52,
          color: '#F4EBDD',
          marginTop: 36,
          opacity: interpolate(frame, [1 * fps, 1.4 * fps], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          }),
        }}
      >
        Compra en el link de la bio
      </Interactive.Div>
    </>
  );
};

export const Cta = Interactive.create({
  Component: CtaInner,
  layout: 'absolute-fill',
  schema: {
    ...Interactive.backgroundSchema,
  },
});
