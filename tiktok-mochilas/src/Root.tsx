import {Composition, Folder} from 'remotion';
import {Mochila} from './components/Mochila';
import {Beneficios} from './scenes/Beneficios';
import {Cta} from './scenes/Cta';
import {Hook} from './scenes/Hook';
import {Oferta} from './scenes/Oferta';
import {Producto} from './scenes/Producto';
import {TikTokMochilas} from './TikTokMochilas';

// Cada registro es su propio nodo JSX con id literal y defaultProps en línea,
// para que Studio pueda guardar cambios de vuelta al código (compositions.md).
export const RemotionRoot = () => (
  <>
    <Folder name="TikTok">
      <Composition
        id="TikTokMochilas"
        component={TikTokMochilas}
        width={1080}
        height={1920}
        fps={30}
        durationInFrames={447}
      />
    </Folder>

    {/* Escenas conectadas: se pueden abrir y editar cada una en su propia línea de tiempo */}
    <Folder name="Escenas">
      <Composition
        id="Gancho"
        component={Hook}
        width={1080}
        height={1920}
        fps={30}
        durationInFrames={75}
        defaultProps={{
          style: {backgroundColor: '#C4532D', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', paddingBottom: 260},
        }}
      />
      <Composition
        id="Producto"
        component={Producto}
        width={1080}
        height={1920}
        fps={30}
        durationInFrames={105}
        defaultProps={{
          style: {backgroundColor: '#F4EBDD', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', paddingBottom: 260},
        }}
      />
      <Composition
        id="Beneficios"
        component={Beneficios}
        width={1080}
        height={1920}
        fps={30}
        durationInFrames={120}
        defaultProps={{
          style: {backgroundColor: '#2F5D50', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', paddingBottom: 260},
        }}
      />
      <Composition
        id="Oferta"
        component={Oferta}
        width={1080}
        height={1920}
        fps={30}
        durationInFrames={90}
        defaultProps={{
          style: {backgroundColor: '#E0A526', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', paddingBottom: 260},
        }}
      />
      <Composition
        id="LlamadoALaAccion"
        component={Cta}
        width={1080}
        height={1920}
        fps={30}
        durationInFrames={105}
        defaultProps={{
          style: {backgroundColor: '#3B2A20', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', paddingBottom: 260},
        }}
      />
    </Folder>

    <Folder name="Elementos">
      <Composition
        id="Mochila"
        component={Mochila}
        width={1080}
        height={1080}
        fps={30}
        durationInFrames={60}
        defaultProps={{
          base: '#F4EBDD',
          pattern: '#C4532D',
          accent: '#2F5D50',
          style: {width: 640, margin: 'auto'},
        }}
      />
    </Folder>
  </>
);
