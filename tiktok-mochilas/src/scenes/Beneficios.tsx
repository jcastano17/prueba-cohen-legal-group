import {Easing, Interactive, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {bodyFont, titleFont} from '../fonts';

// Escena 3 — Beneficios. Cada tarjeta es su propio nodo JSX (no un .map()),
// para que en Studio se pueda mover, editar o borrar cada una por separado
// (lineamiento timeline-structure.md).
const BeneficiosInner = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  return (
    <>
      <Interactive.Div
        name="Titular beneficios"
        style={{
          fontFamily: titleFont,
          fontWeight: 900,
          fontSize: 104,
          lineHeight: 1.05,
          color: '#F4EBDD',
          textAlign: 'center',
          width: 860,
          marginBottom: 70,
          opacity: interpolate(frame, [0, 0.4 * fps], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          }),
        }}
      >
        Cada mochila es única
      </Interactive.Div>

      <Interactive.Div
        name="Beneficio 1"
        style={{
          fontFamily: bodyFont,
          fontWeight: 700,
          fontSize: 56,
          color: '#3B2A20',
          backgroundColor: '#F4EBDD',
          borderRadius: 28,
          padding: '36px 48px',
          width: 820,
          marginBottom: 32,
          translate: interpolate(frame, [0.4 * fps, 0.9 * fps], ['-1000px 0px', '0px 0px'], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: Easing.spring({damping: 16}),
          }),
        }}
      >
        ✓ Hecha 100% a mano
      </Interactive.Div>

      <Interactive.Div
        name="Beneficio 2"
        style={{
          fontFamily: bodyFont,
          fontWeight: 700,
          fontSize: 56,
          color: '#3B2A20',
          backgroundColor: '#E0A526',
          borderRadius: 28,
          padding: '36px 48px',
          width: 820,
          marginBottom: 32,
          translate: interpolate(frame, [0.9 * fps, 1.4 * fps], ['-1000px 0px', '0px 0px'], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: Easing.spring({damping: 16}),
          }),
        }}
      >
        ✓ Diseños irrepetibles
      </Interactive.Div>

      <Interactive.Div
        name="Beneficio 3"
        style={{
          fontFamily: bodyFont,
          fontWeight: 700,
          fontSize: 56,
          color: '#F4EBDD',
          backgroundColor: '#C4532D',
          borderRadius: 28,
          padding: '36px 48px',
          width: 820,
          translate: interpolate(frame, [1.4 * fps, 1.9 * fps], ['-1000px 0px', '0px 0px'], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: Easing.spring({damping: 16}),
          }),
        }}
      >
        ✓ Envíos a toda Colombia
      </Interactive.Div>
    </>
  );
};

export const Beneficios = Interactive.create({
  Component: BeneficiosInner,
  layout: 'absolute-fill',
  schema: {
    ...Interactive.backgroundSchema,
  },
});
