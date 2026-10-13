#!/usr/bin/env python3
"""
Valida dashboards.json antes de hacer commit al Cash Hub.

Este es el guardarrail que protege la página pública del hub: si el manifiesto
no pasa esta validación, NO se hace commit. Un error aquí es barato; una página
rota en producción no lo es.

Uso:
    python3 validar_manifest.py [ruta_a_dashboards.json]

Sin argumento, busca ./dashboards.json. Sale con código 0 si todo está bien,
1 si hay errores. Las advertencias no bloquean el commit pero conviene leerlas.
"""

import json
import re
import sys
from pathlib import Path

# En Windows la consola suele ser cp1252 y truena al imprimir acentos.
# Forzamos UTF-8 en la salida para que el script corra igual en Win/Mac/Linux.
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# ── Valores permitidos (deben coincidir con index.html) ──────────────────────
PILARES   = {"capi", "exp", "aware", "econ"}
ESTADOS   = {"live", "dev", "pilot"}
TAGS_OK   = {"ci", "co", "campanas"}
MOTIFS    = {"atm", "oxxo", "megaphone", "smile", "shop", "coins"}
REQUERIDOS = ["id", "pillar", "tags", "added", "title", "desc",
              "status", "statusLabel", "quarter", "url", "motif"]

RE_ID    = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")          # kebab-case
RE_FECHA = re.compile(r"^\d{4}-\d{2}-\d{2}$")                 # YYYY-MM-DD
RE_GRID  = re.compile(r"^https://grid\.adminml\.com/d/[A-Za-z0-9]+/view$")
RE_HTML  = re.compile(r"^[\w./-]+\.html$")                    # ruta relativa local


def validar(ruta: Path):
    errores, avisos = [], []

    if not ruta.exists():
        return [f"No se encontró el archivo: {ruta}"], []

    try:
        datos = json.loads(ruta.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"JSON inválido: {e}"], []

    if not isinstance(datos, list):
        return ["El manifiesto debe ser un array (lista) de tarjetas."], []

    ids_vistos = {}
    for i, d in enumerate(datos):
        et = f"tarjeta #{i}"
        if not isinstance(d, dict):
            errores.append(f"{et}: debe ser un objeto.")
            continue
        et = f"tarjeta #{i} (id={d.get('id', '??')})"

        # Campos requeridos presentes
        for k in REQUERIDOS:
            if k not in d:
                errores.append(f"{et}: falta el campo requerido '{k}'.")

        # id: kebab-case y único
        _id = d.get("id")
        if isinstance(_id, str):
            if not RE_ID.match(_id):
                errores.append(f"{et}: 'id' debe ser kebab-case (ej. 'oxxo-co').")
            if _id in ids_vistos:
                errores.append(f"{et}: 'id' duplicado (ya usado en tarjeta #{ids_vistos[_id]}).")
            else:
                ids_vistos[_id] = i

        # Enums
        if d.get("pillar") not in PILARES:
            errores.append(f"{et}: 'pillar' debe ser uno de {sorted(PILARES)}.")
        if d.get("status") not in ESTADOS:
            errores.append(f"{et}: 'status' debe ser uno de {sorted(ESTADOS)}.")
        if d.get("motif") not in MOTIFS:
            errores.append(f"{et}: 'motif' debe ser uno de {sorted(MOTIFS)}.")

        # tags: lista, subconjunto de TAGS_OK
        tags = d.get("tags")
        if not isinstance(tags, list):
            errores.append(f"{et}: 'tags' debe ser una lista.")
        else:
            fuera = set(tags) - TAGS_OK
            if fuera:
                errores.append(f"{et}: tags no válidos {sorted(fuera)}; permitidos {sorted(TAGS_OK)}.")
            if not tags:
                avisos.append(f"{et}: 'tags' está vacío; la tarjeta no saldrá en los filtros CI/CO/Campañas.")

        # added: fecha
        if isinstance(d.get("added"), str) and not RE_FECHA.match(d["added"]):
            errores.append(f"{et}: 'added' debe tener formato YYYY-MM-DD.")

        # Textos no vacíos
        for k in ("title", "desc", "statusLabel", "quarter"):
            v = d.get(k)
            if not isinstance(v, str) or not v.strip():
                errores.append(f"{et}: '{k}' no puede estar vacío.")

        # url: Grid view URL (preferido), null, o ruta .html local (con aviso)
        url = d.get("url")
        if url is None:
            avisos.append(f"{et}: 'url' es null; la tarjeta mostrará 'Próximamente'.")
        elif isinstance(url, str):
            if RE_GRID.match(url):
                pass  # caso ideal: dashboard alojado en Grid
            elif RE_HTML.match(url):
                avisos.append(
                    f"{et}: 'url' apunta a un archivo local ('{url}'). "
                    "Los dashboards deben alojarse en Grid (URL grid.adminml.com/d/.../view) "
                    "para no exponer datos internos en este repo público."
                )
            else:
                errores.append(
                    f"{et}: 'url' debe ser una URL de Grid "
                    "(https://grid.adminml.com/d/<id>/view) o null."
                )
        else:
            errores.append(f"{et}: 'url' debe ser texto o null.")

    return errores, avisos


def main():
    ruta = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("dashboards.json")
    errores, avisos = validar(ruta)

    for a in avisos:
        print(f"  AVISO: {a}")
    for e in errores:
        print(f"  ERROR: {e}")

    if errores:
        print(f"\n[FALLO] {ruta.name}: {len(errores)} error(es). NO hacer commit hasta corregir.")
        sys.exit(1)

    n = len(json.loads(ruta.read_text(encoding='utf-8')))
    extra = f" ({len(avisos)} aviso(s))" if avisos else ""
    print(f"\n[OK] {ruta.name}: {n} tarjeta(s), valido{extra}.")
    sys.exit(0)


if __name__ == "__main__":
    main()
