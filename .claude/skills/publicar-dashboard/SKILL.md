---
name: publicar-dashboard
description: >
  Construye y publica dashboards de comunicación al Cash Hub de Money Rails (Mercado Pago MLM).
  Úsala SIEMPRE que alguien quiera armar un dashboard nuevo para el hub, subir/publicar su dashboard,
  agregar su tarjeta al Cash Hub, compartir un dashboard de campaña con el equipo, o actualizar uno ya
  publicado. Dispara con frases como "publica mi dashboard", "sube esto al cash hub", "agregar dashboard
  al hub", "arma un dashboard de la campaña X", "ya tengo los datos, móntalo en el hub", "ship my dashboard",
  "add my dashboard to the cash hub". La skill arma el HTML con la estructura estándar de 3 bloques, lo sube
  a Grid (privado, MELI), agrega la tarjeta validada al hub público y deja todo enlazado y en vivo.
allowed-tools: [Bash, Read, Write, Edit, Glob, Grep, AskUserQuestion, Skill]
---

# Publicar un dashboard al Cash Hub

Esta skill te lleva de "tengo datos de una campaña" a "mi dashboard está en vivo en el Cash Hub,
enlazado y actualizable". Síguela de principio a fin; al terminar habrás:

1. Armado el dashboard con la **estructura de 3 bloques** (estructura obligatoria, estética libre).
2. Subido el HTML a **Grid** (privado, solo MELI).
3. Agregado tu **tarjeta** al hub público con un enlace a tu doc de Grid.
4. Dejado todo **enlazado y en vivo** en `https://extdarami-sudo.github.io/money-rails-hub/`.

## El modelo mental (léelo, evita el 90% de los errores)

Hay **dos lugares** y cada cosa va en uno solo:

| Va a **Grid** (privado, MELI) | Va al **repo público** (`money-rails-hub`) |
|---|---|
| El HTML completo del dashboard | **Solo** una tarjeta en `dashboards.json` |
| El `DASHBOARD_META` con tus queries | (título, descripción, pilar, estado, enlace a Grid) |
| Los números, tablas internas, SQL | Nada más |

**Por qué importa:** el repo es público en GitHub Pages. Si subes ahí el HTML o el SQL, expones
nombres de tablas internas y datos de MELL al internet abierto. Grid respeta la identidad MELI, así
que el dashboard solo lo ven tus compañeros. Por eso el dashboard vive en Grid y el repo solo guarda
la tarjeta que enlaza a Grid.

La **página principal del hub (`index.html`) es lo más visible y NO se toca**: lee las tarjetas desde
`dashboards.json`. Tú solo agregas una entrada validada a ese JSON.

---

## Requisitos (una sola vez)

1. **Acceso al repo.** Daniel te agrega como colaborador de `github.com/extdarami-sudo/money-rails-hub`.
   Clónalo y trabaja dentro de esa carpeta (es la raíz del repo).
2. **VPN de MELI activa** para poder subir a Grid (GlobalProtect). La skill `grid-sharing` la verifica.
3. **Python** disponible (para validar el manifiesto). En Mac/Linux es `python3`; en Windows suele ser `python`.

---

## Flujo

### 0. ¿Nuevo o actualización?

Pregunta (o deduce del contexto) si es un **dashboard nuevo** o una **actualización** de uno ya publicado.
Si hay un enlace de Grid (`grid.adminml.com/d/.../view`) o un `doc_id` en la conversación, es actualización
→ ve a la sección **"Actualizar un dashboard existente"** al final. Si es nuevo, sigue aquí.

### 1. Arma el dashboard (estructura obligatoria, estética libre)

Parte de la plantilla: `.claude/skills/publicar-dashboard/assets/plantilla.html`. Cópiala a un archivo
de trabajo **fuera del repo** (o con nombre `*_dashboard.html`, que el `.gitignore` ya bloquea) y llénala.

- **Obligatorio:** mantener los tres bloques delimitados (`DASHBOARD_META`, `DATA`, `RENDER`) y que el
  RENDER lea **solo** de `DATA`. Lee `.claude/skills/publicar-dashboard/references/protocolo_tres_bloques.md`
  para el detalle de cada bloque, los tipos de `ventana`, y las **reglas de Grid** (no `localStorage`, no
  `alert/confirm/prompt`).
- **Libre:** colores, tipografía, layout, qué gráficas, cuántas. El hub no impone estética — cada dashboard
  comunica cosas distintas. Usa el diseño que mejor cuente tu historia.
- Pon en `DASHBOARD_META.queries` el SQL real con `{{fecha_inicio}}`/`{{fecha_fin}}` donde aplique. Eso es
  lo que permitirá actualizarlo después (manual o por cron).

Verifica que abre bien en el navegador y que **NO sale en blanco** — que los KPIs, gráficas y tabla
realmente aparezcan con datos. Un dashboard vacío casi siempre significa que el `<script>` corre antes de
que existan sus contenedores: el BLOQUE 3 (RENDER) debe ir **después** de los `<div>` que usa (haz
`getElementById` sobre elementos que ya existen). Si corres en un agente sin navegador, haz un volcado
headless del DOM y confirma que los valores aparecen; y verifica la estructura: los tres bloques presentes
y que el RENDER solo lea de `DATA` (sin números de negocio hardcodeados).

### 2. Sube el HTML a Grid

Usa la skill **`grid-sharing`** (no reimplementes el curl; ella maneja VPN, versión y errores). Pídele subir
tu archivo con:

- `visibility: "public"` → en Grid significa **visible para MELI** (tus compañeros pueden abrir la tarjeta;
  gente fuera de MELI no alcanza Grid). Es lo que hace que el enlace del hub funcione para el equipo.
- Un `title` claro (p. ej. "Camp. OXXO Cash-out — Money Rails").
- `tags` útiles (p. ej. `["money-rails","cash-hub","oxxo"]`).

Guarda de la respuesta el **`view_url`** (`https://grid.adminml.com/d/<doc_id>/view`) y el **`doc_id`**.
Ese `view_url` es el `url` de tu tarjeta.

### 3. Clasifica la tarjeta — PREGUNTA al usuario, no adivines

Las tarjetas del hub muestran **si la iniciativa está en línea** y **de qué tipo es**. Estos campos no se
infieren: **pregúntalos siempre al usuario**, con sus opciones fijas. Si los adivinas, las tarjetas quedan
inconsistentes y los filtros del hub (CI/CO/Campañas, En vivo/Desarrollo/Pilot) dejan de agrupar bien.
Usa `AskUserQuestion` cuando esté disponible para que la respuesta sea siempre un valor válido del enum.
Si `AskUserQuestion` no está disponible, pregúntalo en texto plano listando las opciones fijas — pero
pregunta, no asumas.

**Muestra al usuario las opciones de cada campo** (las listas de abajo) para que elija — no preguntes en
abierto ni sustituyas por tu propia suposición. Si por alguna razón no puedes preguntarle (p. ej. corres
sin supervisión), **detente y pídelas**: nunca publiques una tarjeta con la clasificación asumida.

Pregunta estos cuatro:

1. **¿Está en línea? (`status`)** — ¿la iniciativa ya está en vivo, en desarrollo o en pilot?
   - `live` · `dev` · `pilot`
2. **Tipo / pilar estratégico (`pillar`)** — ¿cuál aplica?
   - `capi` (Capilaridad) · `exp` (Experiencia) · `aware` (Awareness) · `econ` (Economics)
3. **Tipo de movimiento (`tags`)** — uno o varios (multi-selección):
   - `ci` (cash-in) · `co` (cash-out) · `campanas` (campaña)
4. **Trimestre (`quarter`)** — ej. `Q2 26`, `Continuo`.

El **`statusLabel` NO se pregunta**: se deriva de `status` para que nunca quede desalineado
(`live`→"En vivo", `dev`→"En desarrollo", `pilot`→"En pilot").

El **`motif`** (ícono) proponlo tú y confírmalo. Guía rápida para que el equipo elija parecido ante la
misma temática: `atm` (cajeros/retiros bancarios) · `oxxo` (OXXO/tiendas de conveniencia) ·
`megaphone` (campañas/push/awareness) · `smile` (experiencia/NPS) · `shop` (comercios/marketplace/cadenas) ·
`coins` (economics/costos/dinero genérico). Si ninguno encaja perfecto, elige el más cercano por tema.

### 4. Agrega tu tarjeta a `dashboards.json`

Con las respuestas de arriba, **agrega un objeto** al array. El orden físico en el archivo no importa: el
hub ordena las tarjetas por `added` (más nuevo primero) al renderizar. Solo **no modifiques ni reordenes las
demás tarjetas**:

```json
{
  "id": "oxxo-co",
  "pillar": "capi",
  "tags": ["co", "campanas"],
  "added": "2026-06-02",
  "title": "OXXO Cash-out — Money Rails",
  "desc": "Una o dos líneas: qué mide el dashboard, en español.",
  "status": "live",
  "statusLabel": "En vivo",
  "quarter": "Q2 26",
  "url": "https://grid.adminml.com/d/01XXXX.../view",
  "motif": "oxxo"
}
```

- `id`: kebab-case, único en el archivo (deriva del título).
- `added`: la fecha de hoy (YYYY-MM-DD).
- `url`: el `view_url` de Grid del paso 2.
- `title`/`desc`: del dashboard, en español.
- `status`, `pillar`, `tags`, `quarter`, `motif`: de lo que respondió el usuario en el paso 3.
- `statusLabel`: derivado de `status` (ver arriba).

### 5. Valida el manifiesto (obligatorio antes de commit)

```bash
python3 .claude/skills/publicar-dashboard/scripts/validar_manifest.py dashboards.json \
  || python .claude/skills/publicar-dashboard/scripts/validar_manifest.py dashboards.json
```

- Sale con `[OK]` → continúa.
- Sale con `[FALLO]` → corrige lo que liste y vuelve a correr. **No hagas commit hasta que pase.**
  Este paso es el que protege la página pública: un manifiesto inválido se detiene aquí, no en producción.

### 6. (Opcional) Regístralo para el cron de auto-actualización

Si quieres que tu dashboard se actualice solo, agrega un puntero en `refresh/config.json` dentro de
`campaigns`:

```json
{ "id": "oxxo-co", "grid_doc_id": "01XXXX...", "grid_view_url": "https://grid.adminml.com/d/01XXXX.../view", "schedule": "daily" }
```

**Nunca** pongas SQL ni nombres de tabla aquí (repo público). El cron lee tus queries desde el `DASHBOARD_META`
embebido en el doc de Grid.

Si tu `ventana.tipo` es `post_campana` con `dias_reporte: null`, o el experimento ya cerró, usa
`"schedule": "manual"`: el cron no puede resolver la ventana solo (necesita que alguien diga cuántos días reportar).

### 7. Guardarrail + commit + push

Antes de commitear, confirma que **solo** estás subiendo el manifiesto (y opcionalmente el config del cron):

```bash
git add dashboards.json refresh/config.json
# Revisa que NO se haya colado un dashboard ni un .sql:
git diff --cached --name-only
```

Lo único que debe aparecer es `dashboards.json` (y `refresh/config.json` si lo usaste). Si ves un
`*_dashboard.html`, un `.sql`, o `index.html`, **deténte y quítalo del stage** (`git restore --staged <archivo>`):
eso no va al repo público. Luego:

```bash
git commit -m "Agregar dashboard: <título>"
git push corporate master
```

> Si `corporate` no existe como remote en tu clon, usa `origin` (o el remote que apunte a
> `extdarami-sudo/money-rails-hub`). Verifícalo con `git remote -v`.

### 8. Confirma que quedó en vivo

GitHub Pages reconstruye en ~1 min. Abre `https://extdarami-sudo.github.io/money-rails-hub/`, busca tu
tarjeta y haz clic: debe abrir tu dashboard en Grid. Avísale a quien corresponda (Slack `#cash-mlm`).

---

## Reglas que protegen el hub (no negociables, y el porqué)

- **No edites `index.html`.** Es la cara del hub y ya lee las tarjetas desde `dashboards.json`. Tocar su
  HTML/CSS/JS es la forma más fácil de romper la página de todos. Tú solo agregas al JSON.
- **No subas el HTML del dashboard ni `.sql` al repo.** Van a Grid. El `.gitignore` y el paso 7 te cubren,
  pero la responsabilidad es tuya: el repo es público.
- **No toques las tarjetas de otros** en `dashboards.json` ni el `RAILS`/roadmap de `index.html`
  (el roadmap se maneja aparte).
- **Siempre valida antes de push** (paso 5). Es barato; una página rota o un dato interno expuesto no lo es.

---

## Actualizar un dashboard existente

Cuando ya hay un doc de Grid y solo cambian los datos (o el estado):

1. Toma el HTML actual (si no lo tienes local, descárgalo de Grid con `grid-sharing` usando el `doc_id`).
2. **Reemplaza solo el BLOQUE 2 (`DATA`)** con los nuevos resultados (corre las queries de `DASHBOARD_META`,
   sustituyendo `{{fecha_inicio}}`/`{{fecha_fin}}` según `ventana`). Sube `ultima_actualizacion` a hoy.
   - Si `ventana.tipo` es `post_campana` y `dias_reporte` es `null`, **pregunta cuántos días reportar** antes
     de correr nada.
3. Sube **nueva versión** a Grid con `grid-sharing` (`doc_id` + `file_new_version: true`). El `view_url` no
   cambia, así que la tarjeta sigue igual.
4. En `dashboards.json` normalmente **no cambias nada**. Solo edita la tarjeta si cambió el `title`, `desc`,
   `status`/`statusLabel` (p. ej. de `live` a un cierre) o `quarter`. Si la tocas, valida (paso 5) y commitea.

---

## Referencia de campos de la tarjeta

| Campo | Valores |
|---|---|
| `pillar` | `capi` (Capilaridad) · `exp` (Experiencia) · `aware` (Awareness) · `econ` (Economics) |
| `status` / `statusLabel` | `live`/"En vivo" · `dev`/"En desarrollo" · `pilot`/"En pilot" |
| `tags` | cualquier combo de `ci` · `co` · `campanas` |
| `motif` (ícono) | `atm` · `oxxo` · `megaphone` · `smile` · `shop` · `coins` |
| `url` | `view_url` de Grid (`https://grid.adminml.com/d/<id>/view`) |
| `added` | fecha de alta, `YYYY-MM-DD` (define el orden: lo más nuevo primero) |

---

## Archivos de esta skill

| Archivo | Para qué |
|---|---|
| `assets/plantilla.html` | Plantilla base con los 3 bloques. Cópiala para empezar. |
| `references/protocolo_tres_bloques.md` | Detalle de los bloques, tipos de ventana y reglas de Grid. |
| `scripts/validar_manifest.py` | Valida `dashboards.json`. Córrelo antes de cada commit (paso 5). |
