#!/usr/bin/env python3
"""Decode screen images captured with the browser-export strategy.

Reads page-script result files (JSON with {"text": ...} blocks, or plain text)
containing '@@<key>@@<base64>' and saves <key>.png in the output folder. When
the design tool returned a ZIP (several export settings on one frame), the
largest PNG inside is kept.

Usage:
    python decode_captures.py --output <folder> result1 [result2 ...]
    python decode_captures.py --output <folder> --contact-sheet results*
(Spanish aliases: --salida, --hoja-contactos.)
"""
import argparse
import base64
import io
import json
import os
import re
import sys
import zipfile

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    sys.exit("Pillow is missing: pip install pillow")

PATRON = re.compile(r"@@([\w.-]+)@@([A-Za-z0-9+/=]+)")


def leer_texto(ruta):
    crudo = open(ruta, encoding="utf-8", errors="replace").read()
    try:
        datos = json.loads(crudo)
    except ValueError:
        return crudo
    if isinstance(datos, list):
        return "".join(d.get("text", "") if isinstance(d, dict) else str(d) for d in datos)
    if isinstance(datos, dict):
        return datos.get("text", crudo)
    return crudo


def a_png(raw):
    if raw[:2] == b"PK":
        z = zipfile.ZipFile(io.BytesIO(raw))
        pngs = [n for n in z.namelist() if n.lower().endswith(".png")]
        if not pngs:
            raise ValueError("ZIP without PNG: " + ", ".join(z.namelist()))
        raw = z.read(max(pngs, key=lambda n: z.getinfo(n).file_size))
    img = Image.open(io.BytesIO(raw))
    img.load()
    return raw, img


def hoja_contactos(imagenes, destino, ancho=220):
    if not imagenes:
        return
    miniaturas = []
    for clave, img in imagenes:
        m = img.copy()
        m.thumbnail((ancho, ancho * 3))
        miniaturas.append((clave, m))
    cols = min(6, len(miniaturas))
    filas = (len(miniaturas) + cols - 1) // cols
    alto = max(m.height for _, m in miniaturas) + 24
    hoja = Image.new("RGB", (cols * (ancho + 16), filas * alto), "white")
    try:
        from PIL import ImageDraw
        dibujo = ImageDraw.Draw(hoja)
    except Exception:
        dibujo = None
    for i, (clave, m) in enumerate(miniaturas):
        x, y = (i % cols) * (ancho + 16), (i // cols) * alto
        hoja.paste(m, (x, y + 20))
        if dibujo:
            dibujo.text((x, y + 4), clave[:34], fill="black")
    hoja.save(destino)
    print("contact sheet:", destino)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", "--salida", dest="salida", required=True, help="output folder")
    p.add_argument("--contact-sheet", "--hoja-contactos", dest="hoja_contactos", action="store_true",
                   help="also write _contact-sheet.png with every image")
    p.add_argument("archivos", nargs="+", metavar="files")
    a = p.parse_args()
    os.makedirs(a.salida, exist_ok=True)
    ok, fallos, imagenes = 0, 0, []
    for ruta in a.archivos:
        for m in PATRON.finditer(leer_texto(ruta)):
            clave, b64 = m.group(1), m.group(2)
            try:
                raw, img = a_png(base64.b64decode(b64))
            except Exception as e:  # imagen truncada o corrupta
                fallos += 1
                print(f"FAILED {clave}: {e} ({len(b64)} characters) — fetch it again, alone")
                continue
            open(os.path.join(a.salida, clave + ".png"), "wb").write(raw)
            imagenes.append((clave, img))
            ok += 1
            print(f"OK {clave} {img.size[0]}x{img.size[1]}")
    if a.hoja_contactos:
        hoja_contactos(imagenes, os.path.join(a.salida, "_contact-sheet.png"))
    print(f"{ok} images, {fallos} failures")
    sys.exit(1 if fallos else 0)


if __name__ == "__main__":
    main()
