"""Chemins, configuration et accès aux scripts partagés par toutes les étapes."""
import csv
import json
import os
import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config.yaml"
VIDEOS_CSV = ROOT / "config" / "videos.csv"
SCRIPTS_JSON = Path(os.environ.get("WTH_SCRIPTS", ROOT / "scripts" / "scripts.json"))
CAROUSELS = ROOT / "data" / "carousels"
ASSETS = Path(os.environ.get("WTH_ASSETS", ROOT / "assets"))
BRAND_DIR = ASSETS / "brand"
CACHE_TTS = ROOT / "cache" / "tts"
LOCKS = ROOT / "locks"
# Surchargeables pour les tests (WTH_BUILD, WTH_OUTPUT).
BUILD = Path(os.environ.get("WTH_BUILD", ROOT / "build"))
OUTPUT = Path(os.environ.get("WTH_OUTPUT", ROOT / "output"))


def load_config():
    cfg = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    brand_file = BRAND_DIR / "brand.yaml"
    if brand_file.exists():
        cfg["brand"].update(yaml.safe_load(brand_file.read_text(encoding="utf-8")) or {})
    return cfg


def videos():
    with VIDEOS_CSV.open(encoding="utf-8") as f:
        return {row["id"]: row for row in csv.DictReader(f)}


def load_scripts():
    data = json.loads(SCRIPTS_JSON.read_text(encoding="utf-8"))
    return {s["id"]: s for s in data}


def script(video_id):
    scripts = load_scripts()
    if video_id not in scripts:
        raise SystemExit(f"{video_id} absent de {SCRIPTS_JSON}")
    return scripts[video_id]


def build_dir(video_id):
    path = BUILD / video_id
    path.mkdir(parents=True, exist_ok=True)
    return path


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def hex_to_ass(color, alpha="00"):
    """#RRGGBB -> &HAABBGGRR (format couleur ASS)."""
    c = color.lstrip("#")
    return f"&H{alpha}{c[4:6]}{c[2:4]}{c[0:2]}".upper()


def run(cmd, **kwargs):
    return subprocess.run(cmd, check=True, text=True, capture_output=True, **kwargs)


def ffprobe(path):
    out = run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(path)])
    return json.loads(out.stdout)


def env(name):
    value = os.environ.get(name)
    if not value:
        raise SystemExit(f"Variable d'environnement {name} manquante.")
    return value
