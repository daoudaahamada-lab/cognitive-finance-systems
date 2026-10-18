"""Voix ElevenLabs (text-to-speech with-timestamps) avec cache et verrouillage des voix validées.

Une voix déjà générée n'est jamais régénérée : le cache est indexé par un hash
(texte, voix, modèle, réglages, format, seed). Une vidéo validée est verrouillée
(locks/Vxx.json) : son audio ne change plus, même si le texte ou la config changent,
sauf FORCE=1.
"""
import argparse
import base64
import hashlib
import json
import os
import re
from datetime import datetime, timezone

import requests

from .common import (CACHE_TTS, LOCKS, OUTPUT, build_dir, env, load_config, load_scripts, read_json, script,
                     write_json)

API = "https://api.elevenlabs.io"


def _headers():
    return {"xi-api-key": env("ELEVENLABS_API_KEY"), "Content-Type": "application/json"}


def request_spec(text, voice_id, cfg):
    t = cfg["tts"]
    return {
        "text": text,
        "voice_id": voice_id,
        "model_id": t["model_id"],
        "voice_settings": t["voice_settings"],
        "output_format": t["output_format"],
        "seed": t["seed"],
    }


def cache_key(spec):
    blob = json.dumps(spec, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()[:24]


def cache_paths(key):
    return CACHE_TTS / f"{key}.mp3", CACHE_TTS / f"{key}.json"


def ensure_voice(voice_id, name=""):
    """Ajoute à « Mes voix » une voix de la bibliothèque si le compte ne l'a pas encore."""
    r = requests.get(f"{API}/v1/voices/{voice_id}", headers=_headers(), timeout=30)
    if r.ok:
        return
    params = {"page_size": 100, "language": "fr"}
    if name:
        params["search"] = name.split(" - ")[0]
    shared = requests.get(f"{API}/v1/shared-voices", headers=_headers(), params=params, timeout=30)
    shared.raise_for_status()
    match = next((v for v in shared.json().get("voices", []) if v["voice_id"] == voice_id), None)
    if not match:
        raise SystemExit(f"Voix {voice_id} introuvable dans le compte ni dans la bibliothèque.")
    add = requests.post(f"{API}/v1/voices/add/{match['public_owner_id']}/{voice_id}", headers=_headers(),
                        json={"new_name": match.get("name", name) or voice_id}, timeout=30)
    if not add.ok:
        raise SystemExit(f"Ajout de la voix {voice_id} refusé : {add.status_code} {add.text[:300]}")


def synthesize(spec, name=""):
    """Retourne (mp3, json) depuis le cache, ou appelle l'API une seule fois."""
    key = cache_key(spec)
    mp3, meta = cache_paths(key)
    if mp3.exists() and meta.exists():
        return key, mp3, meta
    url = f"{API}/v1/text-to-speech/{spec['voice_id']}/with-timestamps"
    body = {k: spec[k] for k in ("text", "model_id", "voice_settings", "seed")}
    r = requests.post(url, headers=_headers(), params={"output_format": spec["output_format"]}, json=body, timeout=300)
    if r.status_code in (400, 404) and "voice" in r.text.lower() and "not" in r.text.lower():
        ensure_voice(spec["voice_id"], name)
        r = requests.post(url, headers=_headers(), params={"output_format": spec["output_format"]}, json=body,
                          timeout=300)
    if not r.ok:
        raise SystemExit(f"ElevenLabs {r.status_code} : {r.text[:500]}")
    data = r.json()
    CACHE_TTS.mkdir(parents=True, exist_ok=True)
    mp3.write_bytes(base64.b64decode(data["audio_base64"]))
    write_json(meta, {
        "request": spec,
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "alignment": data["alignment"],
        "normalized_alignment": data.get("normalized_alignment"),
    })
    return key, mp3, meta


def lock_path(video_id):
    return LOCKS / f"{video_id}.json"


def tts_video(video_id, force=False):
    cfg = load_config()
    voice_id = cfg["tts"]["voice_id"]
    s = script(video_id)
    lock = lock_path(video_id)
    if lock.exists() and not force:
        locked = read_json(lock)
        mp3, meta = cache_paths(locked["cache_key"])
        if not (mp3.exists() and meta.exists()):
            raise SystemExit(f"{video_id} est verrouillée mais son audio {locked['cache_key']} est absent du cache.")
        if read_json(meta)["request"]["text"] != s["texte"]:
            print(f"{video_id} : verrouillée, le texte de scripts.json a changé mais l'audio validé est conservé "
                  f"(FORCE=1 pour régénérer).")
        key = locked["cache_key"]
    else:
        if not voice_id:
            raise SystemExit("Aucune voix choisie : renseigne tts.voice_id dans config.yaml (voir make voices).")
        key, mp3, meta = synthesize(request_spec(s["texte"], voice_id, cfg))
    out = build_dir(video_id)
    write_json(out / "tts.json", {"cache_key": key, "audio": str(mp3), "meta": str(meta)})
    print(f"{video_id} : audio {mp3.name}")
    return key


def lock_video(video_id):
    current = build_dir(video_id) / "tts.json"
    if not current.exists():
        raise SystemExit(f"{video_id} : pas d'audio à verrouiller (lance make video ID={video_id}).")
    info = read_json(current)
    req = read_json(info["meta"])["request"]
    write_json(lock_path(video_id), {
        "cache_key": info["cache_key"],
        "voice_id": req["voice_id"],
        "text_sha": hashlib.sha256(req["text"].encode("utf-8")).hexdigest()[:16],
        "validated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    })
    print(f"{video_id} verrouillée sur {info['cache_key']}")


def sample_text():
    """Environ 10 s : accroche + contexte de V01."""
    s = load_scripts()["V01"]
    parts = {seg["partie"]: seg["texte"] for seg in s["segments"]}
    return f"{parts['accroche']} {parts['contexte']}"


def list_french_voices():
    mine = requests.get(f"{API}/v2/voices", headers=_headers(), params={"page_size": 100}, timeout=30)
    mine.raise_for_status()
    rows = []
    for v in mine.json().get("voices", []):
        langs = {(v.get("labels") or {}).get("language", "")}
        langs |= {lang.get("language", "") for lang in v.get("verified_languages") or []}
        if "fr" in langs:
            rows.append(("compte", v["voice_id"], v["name"], (v.get("labels") or {}).get("accent", ""),
                         (v.get("labels") or {}).get("gender", "")))
    shared = requests.get(f"{API}/v1/shared-voices", headers=_headers(),
                          params={"language": "fr", "page_size": 100, "use_cases": "informative_educational"},
                          timeout=30)
    shared.raise_for_status()
    for v in shared.json().get("voices", []):
        rows.append(("bibliothèque", v["voice_id"], v["name"], v.get("accent", ""), v.get("gender", "")))
    return rows


def voices():
    cfg = load_config()
    out = OUTPUT / "voices"
    out.mkdir(parents=True, exist_ok=True)
    rows = list_french_voices()
    lines = ["| Source | voice_id | Nom | Accent | Genre |", "|---|---|---|---|---|"]
    lines += [f"| {a} | `{b}` | {c} | {d} | {e} |" for a, b, c, d, e in rows]
    (out / "voix_fr.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(rows)} voix françaises -> {out / 'voix_fr.md'}")
    text = sample_text()
    for v in cfg["tts"]["shortlist"]:
        _, mp3, _ = synthesize(request_spec(text, v["voice_id"], cfg), v["name"])
        slug = re.sub(r"[^a-z0-9]+", "-", v["name"].lower()).strip("-")
        target = out / f"extrait-{slug}.mp3"
        target.write_bytes(mp3.read_bytes())
        print(f"{v['name']} -> {target}")


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("video")
    v.add_argument("id")
    sub.add_parser("voices")
    lk = sub.add_parser("lock")
    lk.add_argument("id")
    args = p.parse_args()
    if args.cmd == "video":
        tts_video(args.id, force=os.environ.get("FORCE") == "1")
    elif args.cmd == "voices":
        voices()
    else:
        lock_video(args.id)


if __name__ == "__main__":
    main()
