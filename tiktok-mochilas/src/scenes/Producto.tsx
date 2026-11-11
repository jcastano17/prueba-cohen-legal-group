import {Easing, Interactive, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {Mochila} from '../components/Mochila';
import {bodyFont, titleFont} from '../fonts';

// Escena 2 — Producto: la mochila es lo que el espectador debe notar primero.
const ProductoInner = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  return (
    <>
      <Interactive.Div
        name="Titular producto"
        style={{
          fontFamily: titleFont,
          fontWeight: 900,
          fontSize: 116,
          color: '#3B2A20',
          textAlign: 'center',
          translate: interpolate(frame, [0, 0.6 * fps], ['0px -60px', '0px 0px'], {
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
        Tejidas a mano
      </Interactive.Div>

      <Mochila
        name="Mochila protagonista"
        base="#F4EBDD"
        pattern="#C4532D"
        accent="#2F5D50"
        style={{
          width: 640,
          marginTop: 30,
          marginBottom: 30,
          translate: interpolate(frame, [0.2 * fps, 1.1 * fps], ['0px 500px', '0px 0px'], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: Easing.spring({damping: 14}),
          }),
          rotate: interpolate(frame, [0.2 * fps, 1.4 * fps, 3.5 * fps], ['-12deg', '0deg', '4deg'], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: Easing.bezier(0.16, 1, 0.3, 1),
          }),
        }}
      />

      <Interactive.Div
        name="Subtítulo producto"
        style={{
          fontFamily: bodyFont,
          fontWeight: 500,
          fontSize: 54,
          color: '#3B2A20',
          textAlign: 'center',
          width: 820,
          opacity: interpolate(frame, [1 * fps, 1.4 * fps], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          }),
        }}
      >
        por manos artesanas colombianas
      </Interactive.Div>
    </>
  );
};

export const Producto = Interactive.create({
  Component: ProductoInner,
  layout: 'absolute-fill',
  schema: {
    ...Interactive.backgroundSchema,
  },
});
