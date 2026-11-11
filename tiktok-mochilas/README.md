# TikTok — Venta de mochilas artesanales (@altamariacol)

Ejemplo de video vertical (1080x1920, 30 fps, 14,9 s) hecho con
[Remotion](https://www.remotion.dev) siguiendo los lineamientos de
[`remotion-dev/skills`](https://github.com/remotion-dev/skills).

> El texto, la oferta (-20%) y la ilustración de la mochila son de ejemplo.
> Cámbialos por los datos reales y por fotos del producto antes de publicar.

## Comandos

```bash
npm i
npm run dev                                   # Remotion Studio (vista previa editable)
npx remotion render TikTokMochilas out/tiktok.mp4   # Exportar el MP4
```

## Estructura

| Archivo | Qué es |
|---|---|
| `src/index.ts` | Punto de entrada: registra la raíz. |
| `src/Root.tsx` | Registra las composiciones: el video completo, cada escena y la mochila. |
| `src/TikTokMochilas.tsx` | El video: 5 escenas unidas con `TransitionSeries` y transiciones. |
| `src/scenes/*.tsx` | Una escena por archivo: Gancho, Producto, Beneficios, Oferta, Llamado a la acción. |
| `src/components/Mochila.tsx` | Ilustración SVG de la mochila con colores editables. |
| `src/components/PatternBand.tsx` | Franja decorativa con rombos en movimiento. |
| `src/fonts.ts` | Carga las fuentes Fraunces y DM Sans desde `public/fonts`. |
| `public/fonts/` | Fuentes variables (Google Fonts, licencia OFL). |
