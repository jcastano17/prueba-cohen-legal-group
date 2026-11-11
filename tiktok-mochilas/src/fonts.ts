import {loadFont} from '@remotion/fonts';
import {staticFile} from 'remotion';

// Fuentes locales en public/fonts (lineamiento local-fonts.md).
// Son fuentes variables de Google Fonts (licencia OFL): un archivo cubre
// todos los pesos. Locales = el render no depende de la red.
export const titleFont = 'Fraunces';
export const bodyFont = 'DM Sans';

loadFont({
  family: titleFont,
  url: staticFile('fonts/Fraunces-Variable.woff2'),
  weight: '100 900',
});

loadFont({
  family: bodyFont,
  url: staticFile('fonts/DMSans-Variable.woff2'),
  weight: '100 1000',
});
