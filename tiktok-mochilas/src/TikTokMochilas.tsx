import {linearTiming, TransitionSeries} from '@remotion/transitions';
import {fade} from '@remotion/transitions/fade';
import {slide} from '@remotion/transitions/slide';
import {wipe} from '@remotion/transitions/wipe';
import {useVideoConfig} from 'remotion';
import {Beneficios} from './scenes/Beneficios';
import {Cta} from './scenes/Cta';
import {Hook} from './scenes/Hook';
import {Oferta} from './scenes/Oferta';
import {Producto} from './scenes/Producto';

// Video vertical para TikTok (1080x1920).
// Escenas consecutivas que deben quedar pegadas si cambia la duración de una
// => TransitionSeries (lineamiento multi-scene-video.md).
//
// Zona segura de TikTok: la interfaz tapa ~420px abajo (descripción, música)
// y ~140px a la derecha (botones). Por eso cada escena lleva paddingBottom
// para subir el contenido, además del margen general de 80px a los lados.
//
// Duración total: 2.5 + 3.5 + 4 + 3 + 3.5 = 16.5 s menos 4 transiciones de
// 0.4 s (12 cuadros) = 14.9 s = 447 cuadros a 30 fps.
export const TikTokMochilas = () => {
  const {fps} = useVideoConfig();

  return (
    <TransitionSeries name="Escenas">
      <TransitionSeries.Sequence name="Gancho" durationInFrames={2.5 * fps}>
        <Hook
          name="Gancho"
          style={{
            backgroundColor: '#C4532D',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            paddingBottom: 260,
          }}
        />
      </TransitionSeries.Sequence>
      <TransitionSeries.Transition
        presentation={slide({direction: 'from-bottom'})}
        timing={linearTiming({durationInFrames: 12})}
      />
      <TransitionSeries.Sequence name="Producto" durationInFrames={3.5 * fps}>
        <Producto
          name="Producto"
          style={{
            backgroundColor: '#F4EBDD',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            paddingBottom: 260,
          }}
        />
      </TransitionSeries.Sequence>
      <TransitionSeries.Transition
        presentation={wipe({direction: 'from-left'})}
        timing={linearTiming({durationInFrames: 12})}
      />
      <TransitionSeries.Sequence name="Beneficios" durationInFrames={4 * fps}>
        <Beneficios
          name="Beneficios"
          style={{
            backgroundColor: '#2F5D50',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            paddingBottom: 260,
          }}
        />
      </TransitionSeries.Sequence>
      <TransitionSeries.Transition
        presentation={slide({direction: 'from-right'})}
        timing={linearTiming({durationInFrames: 12})}
      />
      <TransitionSeries.Sequence name="Oferta" durationInFrames={3 * fps}>
        <Oferta
          name="Oferta"
          style={{
            backgroundColor: '#E0A526',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            paddingBottom: 260,
          }}
        />
      </TransitionSeries.Sequence>
      <TransitionSeries.Transition
        presentation={fade()}
        timing={linearTiming({durationInFrames: 12})}
      />
      <TransitionSeries.Sequence name="Llamado a la acción" durationInFrames={3.5 * fps}>
        <Cta
          name="Llamado a la acción"
          style={{
            backgroundColor: '#3B2A20',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            paddingBottom: 260,
          }}
        />
      </TransitionSeries.Sequence>
    </TransitionSeries>
  );
};
