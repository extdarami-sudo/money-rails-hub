# Cash Hub — Campañas Money Rails

Hub de dashboards de iniciativas Cash-in / Cash-out de Mercado Pago México.

- **En vivo:** https://extdarami-sudo.github.io/money-rails-hub/
- **Canal:** Slack `#cash-mlm`

---

## Cómo está armado

Hay dos lugares, y cada cosa vive en uno solo:

```
   ┌─────────────────────────────┐         ┌──────────────────────────────────┐
   │  GRID  (privado, MELI)       │         │  Este repo  (PÚBLICO, GitHub Pages)│
   │                              │         │                                    │
   │  • El HTML del dashboard      │  ◀───┐  │  • index.html  (la cara del hub)   │
   │  • Sus queries (DASHBOARD_META)│      └──│  • dashboards.json (las tarjetas)  │
   │  • Los números / tablas       │  enlace │  • refresh/config.json (cron)      │
   └─────────────────────────────┘         └──────────────────────────────────┘
```

La página (`index.html`) **lee las tarjetas desde `dashboards.json`** y cada tarjeta enlaza al dashboard
en Grid. El repo es público, así que **nunca** guardamos aquí el HTML del dashboard ni el SQL: eso vive en
Grid, que respeta la identidad MELI.

---

## Quiero publicar mi dashboard

1. Pídele a Daniel acceso de **colaborador** a este repo y clónalo.
2. Abre Claude Code dentro de la carpeta del repo. Se carga sola la skill **`publicar-dashboard`**.
3. Dile algo como *"publica mi dashboard de la campaña X en el cash hub"* y sigue el flujo: arma el HTML con
   la estructura de 3 bloques, lo sube a Grid, agrega tu tarjeta validada a `dashboards.json` y hace push.

La skill está en `.claude/skills/publicar-dashboard/` (con plantilla, validador y la guía del protocolo).

### Regla de oro

- **No edites `index.html`** — es la cara del hub y ya lee todo desde `dashboards.json`.
- **El dashboard va a Grid; al repo solo va su tarjeta** en `dashboards.json`.
- **Valida antes de hacer push:**
  ```bash
  python3 .claude/skills/publicar-dashboard/scripts/validar_manifest.py dashboards.json
  ```

---

## Estructura del repo

| Ruta | Qué es |
|---|---|
| `index.html` | Landing del hub. Pinta roadmap + tarjetas (las tarjetas vienen de `dashboards.json`). |
| `dashboards.json` | Manifiesto de tarjetas. Lo único que edita la skill al publicar. |
| `refresh/config.json` | Punteros a docs de Grid para el cron de auto-actualización (sin SQL). |
| `.claude/skills/publicar-dashboard/` | La skill para construir y publicar dashboards. |
| `.gitignore` | Bloquea `*_dashboard.html` y `*.sql` para no exponer datos en el repo público. |
