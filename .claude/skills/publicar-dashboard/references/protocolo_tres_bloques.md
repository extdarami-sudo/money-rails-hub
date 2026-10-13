# Protocolo de 3 bloques — dashboards del Cash Hub

Todo dashboard que se publica al Cash Hub es un archivo HTML autocontenido cuyo
`<script>` principal tiene **tres bloques en este orden**. La estética es libre;
lo único que se estandariza es esta estructura de datos, porque es lo que permite
que el dashboard se actualice solo (manual o por cron) sin tocar el código de render.

```
BLOQUE 1 — DASHBOARD_META   (qué queries lo alimentan)
BLOQUE 2 — DATA             (los resultados; lo único que cambia al actualizar)
BLOQUE 3 — RENDER           (gráficas y tablas; leen solo de DATA)
```

Usa los delimitadores con caja (`╔══ BLOQUE N ══╗`) tal como vienen en
`assets/plantilla.html`, para que cualquier agente los localice igual.

---

## Bloque 1 — DASHBOARD_META

```js
const DASHBOARD_META = {
  version: "1",
  proyecto: "Nombre del dashboard",
  ventana: { tipo: "rolling", dias: 30 },     // ver tipos abajo
  ultima_actualizacion: "YYYY-MM-DD",
  queries: [
    {
      id: "nombre_query",                      // == llave en DATA
      descripcion: "Qué mide",
      sql: /* sql */ `SELECT ... WHERE fecha BETWEEN '{{fecha_inicio}}' AND '{{fecha_fin}}'`,
      notas: "Aclaraciones opcionales"
    }
  ]
};
```

### Tipos de ventana

| `ventana.tipo` | Parámetros | Cuándo |
|---|---|---|
| `mes_actual` | — | Seguimiento mensual |
| `rolling` | `dias: N` | Últimos N días |
| `fijo` | `fecha_inicio`, `fecha_fin` | Período histórico cerrado |
| `post_campana` | `fecha_fin_campana`, `dias_reporte` | N días después del cierre de una campaña |

Para `post_campana`, si `dias_reporte` es `null`, quien actualice debe **preguntar
cuántos días reportar** antes de correr las queries (cada campaña es distinta).

Usa `{{fecha_inicio}}` y `{{fecha_fin}}` como placeholders en el SQL; el proceso de
actualización los sustituye según la ventana.

---

## Bloque 2 — DATA

Solo resultados de las queries. Las llaves de primer nivel **coinciden** con los
`id` de las queries.

```js
const DATA = {
  nombre_query: [ /* filas */ ],
  kpis: { total: 0, tasa: 0 },
};
```

**Regla de oro:** este es el único bloque que cambia al actualizar. Bloques 1 y 3
quedan intactos.

---

## Bloque 3 — RENDER

Todo el código de gráficas/tablas/DOM. Lee **solo** de `DATA.*`. Prohibido
hardcodear números de negocio aquí: si un valor sale en pantalla, viene de `DATA`.
Así, actualizar el dashboard = reemplazar el Bloque 2 y nada más.

Si reusas código de render que esperaba otros nombres de variable, declara alias
al inicio del Bloque 3:

```js
const CAMP = DATA.camp;   // alias para no reescribir el render
```

---

## Reglas específicas de Grid (importante)

El dashboard se aloja en **Grid**, dentro de un iframe con sandbox. Para que no
falle silenciosamente:

- **No uses `localStorage` ni `sessionStorage`** — fallan en silencio en el iframe.
  Si necesitas estado persistente, usa `window.GRID.state.get/set()`.
- **No uses `alert()`, `confirm()` ni `prompt()`** — están bloqueados.
- Las gráficas con ApexCharts por CDN funcionan (los dashboards actuales lo usan).
  Grid también ofrece librerías en `/d/_libs/` (Chart.js, Plotly, D3, Leaflet…) si
  prefieres no depender de un CDN externo.
- Embebe los datos en el `<script>` (Bloque 2). No dependas de archivos externos
  salvo recursos de CDN.

---

## Estructuras típicas de DATA

| Tipo de análisis | Forma sugerida |
|---|---|
| Serie de tiempo | `{ labels: [...], serie_a: [...] }` |
| Métricas por brazo/segmento | `[ { arm, n, conversiones, ... } ]` |
| Pre/post por grupo | `[ { id, test:{pre,post}, ctrl:{pre,post} } ]` |
| KPIs planos | `{ total: 0, tasa: 0 }` |
