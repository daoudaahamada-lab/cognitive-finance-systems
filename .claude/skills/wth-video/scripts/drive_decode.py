#!/usr/bin/env python3
"""Décode une illustration téléchargée par le connecteur Google Drive (download_file_content) vers assets/illustrations.

La machine ne joint pas drive.google.com : la seule voie est l'outil MCP download_file_content, qui renvoie le fichier
en base64. Le résultat (~1,8 Mo de texte pour une PNG) dépasse la taille d'un résultat d'outil : le harnais
l'enregistre dans un fichier et donne son chemin (« Output has been saved to … »). Ce script lit ce fichier, en extrait
la base64 (objet JSON {content, id, mimeType, title}, éventuellement enveloppé), écrit la PNG et vérifie sa taille
contre data/illustrations_manifest.tsv.

    python3 -I .claude/skills/wth-video/scripts/drive_decode.py <fichier_résultat> WTH-004-03.png [--root /abs/wth-videos]

Ne lis jamais la base64 toi-même et ne l'affiche pas : elle remplit le contexte pour rien.
Code 0 si la PNG est complète (taille du manifeste, signature PNG), 1 sinon (rien n'est écrit).
"""
import argparse
import base64
import csv
import json
import os
import sys
import tempfile
from pathlib import Path

PNG_SIG = b"\x89PNG\r\n\x1a\n"


def default_root():
    return Path(__file__).resolve().parents[4] / "wth-videos"


def find_payload(obj):
    """Cherche {content: <base64>} dans un résultat éventuellement enveloppé ([{type: text, text: "{...}"}], etc.)."""
    if isinstance(obj, dict):
        if isinstance(obj.get("content"), str) and len(obj["content"]) > 100:
            return obj
        for key in ("text", "result", "content", "data"):
            val = obj.get(key)
            if isinstance(val, (dict, list)):
                hit = find_payload(val)
                if hit:
                    return hit
            elif isinstance(val, str) and val.lstrip().startswith(("{", "[")):
                try:
                    hit = find_payload(json.loads(val))
                except json.JSONDecodeError:
                    hit = None
                if hit:
                    return hit
    if isinstance(obj, list):
        for item in obj:
            hit = find_payload(item)
            if hit:
                return hit
    return None


def main():
    p = argparse.ArgumentParser(description="Décode une illustration Drive (base64) vers assets/illustrations/")
    p.add_argument("saved", help="fichier où le harnais a enregistré le résultat de download_file_content")
    p.add_argument("name", help="nom du fichier tel que dans data/illustrations_manifest.tsv (ex. WTH-004-03.png)")
    p.add_argument("--root", default=str(default_root()))
    a = p.parse_args()
    root = Path(a.root)
    manifest = {}
    with (root / "data" / "illustrations_manifest.tsv").open(encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            manifest[row["fichier"]] = row
    if a.name not in manifest:
        sys.exit(f"{a.name} absent de data/illustrations_manifest.tsv : nom inattendu, rien n'est écrit.")
    expected = int(manifest[a.name]["octets"])

    raw = Path(a.saved).read_text(encoding="utf-8", errors="replace")
    payload = None
    try:
        payload = find_payload(json.loads(raw))
    except json.JSONDecodeError:
        pass
    if payload is not None:
        b64, title, mime = payload["content"], payload.get("title"), payload.get("mimeType")
    else:
        b64, title, mime = raw.strip(), None, None   # base64 nue
    try:
        data = base64.b64decode(b64, validate=True)
    except (ValueError, base64.binascii.Error) as e:
        sys.exit(f"base64 illisible ({e}) : le résultat est peut-être tronqué ; retélécharge ce fichier seul.")
    if title and title != a.name:
        print(f"attention : le fichier Drive s'appelle « {title} », pas « {a.name} » (vérifie l'identifiant)")
    if not data.startswith(PNG_SIG):
        sys.exit(f"pas une PNG (type annoncé : {mime}) : rien n'est écrit.")
    if len(data) != expected:
        sys.exit(f"{len(data)} octets au lieu de {expected} (manifeste) : fichier incomplet, rien n'est écrit.")
    dst = root / "assets" / "illustrations" / a.name
    dst.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=dst.parent, prefix=".dl-", suffix=".png")
    with os.fdopen(fd, "wb") as f:
        f.write(data)
    os.replace(tmp, dst)
    size = ""
    try:
        from PIL import Image
        with Image.open(dst) as im:
            size = f", {im.size[0]}x{im.size[1]} {im.mode}"
    except Exception:  # noqa: BLE001 - PIL facultatif ici
        pass
    print(f"{dst} : {len(data)} octets (= manifeste){size}")


if __name__ == "__main__":
    main()
