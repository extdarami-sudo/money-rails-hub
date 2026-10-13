# Logos de cadenas

Logos que consume la pestaña **`Performance por cadena V2`** del
*Master Dashboard Cash 2026* (`1s14SUaSZ-ffjpdARL1Y1rs8g81_QXIKkGPocTSNbMUs`).

La hoja no guarda las imágenes: guarda la URL en la columna `AD` de la tabla de mapeo
(`T3:AD21`) y las pinta con `=IMAGE(...)` junto a cada selector de cadena. Al cambiar el
selector, cambia el logo.

## Por qué viven aquí y no en Drive

`IMAGE()` de Google Sheets baja la imagen desde los servidores de Google, no desde tu sesión
del navegador. O sea que la URL tiene que ser **pública y sin login**. Eso descarta Drive
(las ligas `drive.google.com/uc?...` ya no funcionan con `IMAGE()`) y descarta cualquier
recurso interno de MELI. Este repo ya es público y ya publica por GitHub Pages, así que es
el lugar natural.

## Convención de nombres

Un archivo por cadena, nombre en minúsculas con guiones, **extensión `.png`**:

| Cadena (selector) | Archivo |
|---|---|
| 7-Eleven | `7-eleven.png` |
| 7-24 | `7-24.png` |
| Abarrey | `abarrey.png` |
| Circle_K | `circle-k.png` |
| Farmacias Roma | `farmacias-roma.png` |
| Farmacias YZA | `farmacias-yza.png` |
| FdA | `fda.png` |
| Finabien | `finabien.png` |
| Kiosko | `kiosko.png` |
| Santander | `santander.png` |
| Soriana | `soriana.png` |
| Systienda | `systienda.png` |
| Tiendas Neto | `tiendas-neto.png` |
| Farmacias Guadalajara | `farmacias-guadalajara.png` |
| OXXO | `oxxo.png` |
| Grupo Walmart | `grupo-walmart.png` |
| CHEDRAUI | `chedraui.png` |
| Grupo La Comer | `grupo-la-comer.png` |

Las URLs ya están escritas en la columna `AD` de la hoja apuntando a estos nombres, así que
**no hay que tocar la hoja**: basta con dejar aquí el archivo con el nombre correcto, hacer
push, y el logo aparece solo.

## Requisitos de cada archivo

- **PNG.** `IMAGE()` no renderiza SVG, y casi todos los logos de marca circulan en SVG —
  hay que exportarlos a PNG antes de subirlos.
- **Fondo transparente**, para que se vea bien sobre el fondo de la celda.
- **Ancho de 240 a 400 px.** La celda mide 111 × 44 px y la fórmula usa el modo 1 de
  `IMAGE()` (ajustar al tamaño de la celda respetando la proporción), así que más resolución
  solo pesa de más.
- Peso razonable, por debajo de ~50 KB. Son íconos, no fotos.

## Cómo se ve la URL final

```
https://extdarami-sudo.github.io/money-rails-hub/assets/logos/oxxo.png
```

Se usa la URL de **GitHub Pages**, no la de `raw.githubusercontent.com`: Pages no trae el
nombre de la rama en la ruta, así que si algún día se renombra `master` las URLs siguen vivas.

## Nota sobre el uso de marcas

Son logos de terceros usados para identificar a cada cadena dentro de un tablero interno de
análisis. No se rediseñan ni se usan como marca propia. Si Legal o Marca pide quitarlos,
se borra el archivo y la celda queda vacía sola — la fórmula está escrita para no marcar
error cuando la imagen no existe.
