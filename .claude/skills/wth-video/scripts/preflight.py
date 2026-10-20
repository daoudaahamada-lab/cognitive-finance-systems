#!/usr/bin/env python3
"""Contrôle avant production d'une ou plusieurs vidéos WTH : imprime ce qui manque et comment le réparer.

    python3 .claude/skills/wth-video/scripts/preflight.py V07 [V08 ...] [--root /abs/wth-videos] [--json]
                                                          [--no-voice] [--no-clean]

Environnement : motion/node_modules (Remotion), navigateur de rendu (motion/browser.json ou
REMOTION_BROWSER_EXECUTABLE), ffmpeg/ffprobe/node/npx, modules Python du pipeline, disque libre ≥ 4 Go (sinon lance
« make clean-tmp » puis remesure, sauf --no-clean), rendu en cours (verrou build/.render.lock).
Par vidéo : script dans scripts/scripts.json et config/videos.csv (même carrousel) ; illustrations du manifeste
(data/illustrations_manifest.tsv) pour SON carrousel + les génériques, présentes et de la bonne taille ; voix en cache
(cache/tts/<clé>.mp3/.json, clé = texte + voix + réglages de config.yaml), versionnée, sous la limite de durée de la
QA, préparée (build/Vxx/tts.json, words.json, audio.wav) ; storyboard (--check), mise en scène, QA existante (info).

Bloquant (✘) : ce qui empêche le storyboard ou le rendu. --no-voice : une voix absente n'est qu'une alerte (pour
lancer la recette voix). Code 1 s'il reste un point bloquant. Aucun appel réseau ; seule écriture possible :
« make clean-tmp » quand le disque est sous le seuil.
"""
import argparse
import csv
import fcntl
import importlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

MIN_FREE_GB = 4.0
CAROUSEL = re.compile(r"^(WTH-\d{3})-\d+\.png$")
OK, WARN, FAIL, INFO = "ok", "warn", "fail", "info"
MARK = {OK: "✔", WARN: "!", FAIL: "✘", INFO: "·"}


def default_root():
    return Path(__file__).resolve().parents[4] / "wth-videos"


class Report:
    def __init__(self):
        self.items = []

    def add(self, level, name, detail="", fix=""):
        self.items.append({"level": level, "name": name, "detail": detail, "fix": fix})

    @property
    def blocking(self):
        return [i for i in self.items if i["level"] == FAIL]


def free_gb(path):
    return shutil.disk_usage(path).free / 1e9


def probe_duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True)
    try:
        return float(out.stdout.strip())
    except ValueError:
        return None


def git_tracked(repo, path):
    r = subprocess.run(["git", "-C", str(repo), "ls-files", "--error-unmatch", str(path)], capture_output=True)
    return r.returncode == 0


def lock_holder(lock):
    """None si le verrou de rendu est libre, sinon le contenu du fichier (pid du rendu)."""
    if not lock.exists():
        return None
    try:
        with open(lock, "r") as fh:
            try:
                fcntl.flock(fh, fcntl.LOCK_SH | fcntl.LOCK_NB)
            except BlockingIOError:
                return (fh.read().strip() or "pid inconnu")
            fcntl.flock(fh, fcntl.LOCK_UN)
    except OSError:
        return None
    return None


def check_env(root, a):
    r = Report()
    motion = root / "motion"
    if (motion / "node_modules" / ".bin" / "remotion").exists():
        r.add(OK, "Remotion (motion/node_modules)")
    else:
        r.add(FAIL, "Remotion (motion/node_modules)", "absent", "make motion-setup (npm ci dans motion/)")
    exe = os.environ.get("REMOTION_BROWSER_EXECUTABLE")
    src = "REMOTION_BROWSER_EXECUTABLE"
    if not exe:
        src = "motion/browser.json"
        try:
            exe = json.loads((motion / "browser.json").read_text(encoding="utf-8")).get("executable")
        except (OSError, json.JSONDecodeError):
            exe = None
    if exe and os.access(exe, os.X_OK):
        r.add(OK, "navigateur de rendu", f"{exe} ({src})")
    else:
        r.add(FAIL, "navigateur de rendu", f"{exe or 'non renseigné'} ({src}) introuvable",
              "references/environment.md, « Navigateur de rendu »")
    for tool in ("ffmpeg", "ffprobe", "node", "npx", "git"):
        if shutil.which(tool):
            r.add(OK, tool)
        else:
            r.add(FAIL, tool, "absent du PATH", "installe-le (references/environment.md)")
    missing = []
    for mod in ("yaml", "numpy", "PIL", "requests"):
        try:
            importlib.import_module(mod)
        except ImportError:
            missing.append(mod)
    if missing:
        r.add(FAIL, "modules Python", ", ".join(missing), "make setup (pip install -r requirements.txt)")
    else:
        r.add(OK, "modules Python (yaml, numpy, PIL, requests)")
    gb = free_gb(root)
    if gb < MIN_FREE_GB and not a.no_clean:
        subprocess.run(["make", "--no-print-directory", "clean-tmp"], cwd=root, capture_output=True, text=True)
        after = free_gb(root)
        r.add(INFO, "make clean-tmp lancé", f"{gb:.1f} Go -> {after:.1f} Go libres")
        gb = after
    if gb >= MIN_FREE_GB:
        r.add(OK, "disque", f"{gb:.1f} Go libres (seuil {MIN_FREE_GB:g} Go)")
    else:
        r.add(FAIL, "disque", f"{gb:.1f} Go libres < {MIN_FREE_GB:g} Go",
              "make clean-tmp ID=<vidéo terminée> ; supprime build/Vxx/review/*/frames, build/Vxx/story/stills/*.png "
              "et muet_*.mp4 des vidéos finies (references/environment.md)")
    holder = lock_holder(root / "build" / ".render.lock")
    if holder:
        r.add(INFO, "rendu en cours", f"verrou build/.render.lock pris ({holder}) : un nouveau rendu attendra")
    return r


def manifest_rows(root):
    path = root / "data" / "illustrations_manifest.tsv"
    if not path.exists():
        return None
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def check_video(root, vid, scripts, videos_csv, rows, cfg, a, common):
    r = Report()
    info = {"id": vid}
    s = scripts.get(vid)
    if not s:
        r.add(FAIL, "script", f"{vid} absent de scripts/scripts.json",
              "écris le script (SKILL.md, « Nouvelle vidéo »), puis make lint ID=" + vid)
        return r, info
    info.update(title=s.get("titre"), source=s.get("source"))
    row = videos_csv.get(vid)
    if not row:
        r.add(FAIL, "config/videos.csv", f"{vid} absent", f"ajoute « {vid},{s.get('source')},<date> »")
    elif row.get("source") != s.get("source"):
        r.add(FAIL, "config/videos.csv", f"carrousel {row.get('source')} ≠ {s.get('source')} (scripts.json)",
              "aligne les deux fichiers")
    else:
        r.add(OK, "script", f"« {s.get('titre')} » ({s.get('source')}, {s.get('mots', '?')} mots)")

    # Illustrations : son carrousel + génériques.
    source = s.get("source", "")
    if rows is None:
        r.add(FAIL, "illustrations", "data/illustrations_manifest.tsv absent", "git checkout du dépôt")
    else:
        illus = root / "assets" / "illustrations"
        wanted = [x for x in rows if not CAROUSEL.match(x["fichier"]) or CAROUSEL.match(x["fichier"]).group(1) == source]
        own = [x for x in wanted if CAROUSEL.match(x["fichier"])]
        missing, bad = [], []
        for x in wanted:
            f = illus / x["fichier"]
            if not f.exists():
                missing.append(x)
            elif f.stat().st_size != int(x["octets"]):
                bad.append(x)
        info["illustrations"] = {"own": len(own), "generic": len(wanted) - len(own),
                                 "missing": [x["fichier"] for x in missing], "bad_size": [x["fichier"] for x in bad]}
        if missing or bad:
            detail = []
            if missing:
                detail.append("absentes : " + ", ".join(f"{x['fichier']} (Drive {x['drive_id']})" for x in missing))
            if bad:
                detail.append("taille fausse (téléchargement tronqué) : " + ", ".join(x["fichier"] for x in bad))
            r.add(FAIL, "illustrations", " ; ".join(detail),
                  "Drive download_file_content puis scripts/drive_decode.py (references/environment.md)")
        else:
            r.add(OK, "illustrations", f"{len(own)} de {source or '—'} + {len(wanted) - len(own)} génériques")
        if not own:
            r.add(INFO, "carrousel", f"{source} : aucune illustration dédiée au manifeste (génériques et code seulement, "
                                     "c'est normal)")

    # Voix.
    q = cfg["qa"]
    qa_max = float((q.get("max_duration_by_video") or {}).get(vid, q["max_duration"]))
    limit = qa_max - float(cfg["video"]["tail_seconds"])
    voice_level = WARN if a.no_voice else FAIL
    try:
        from pipeline.tts import cache_key, cache_paths, lock_path, request_spec
        lock = lock_path(vid)
        if lock.exists():
            key = json.loads(lock.read_text(encoding="utf-8"))["cache_key"]
            locked = True
        else:
            key = cache_key(request_spec(s["texte"], cfg["tts"]["voice_id"], cfg))
            locked = False
        mp3, meta = cache_paths(key)
    except Exception as e:  # noqa: BLE001
        r.add(FAIL, "voix", f"clé de cache incalculable : {e}", "vérifie config.yaml (tts) et scripts.json")
        return r, info
    info["voice"] = {"cache_key": key, "cached": mp3.exists() and meta.exists(), "locked": locked}
    if not (mp3.exists() and meta.exists()):
        r.add(voice_level, "voix", f"absente du cache (cache/tts/{key}.*)",
              "recette voix : references/voice-elevenlabs-mcp.md (crédits ElevenLabs vérifiés d'abord)")
    else:
        m = json.loads(meta.read_text(encoding="utf-8"))
        d = probe_duration(mp3)
        info["voice"].update(generation_id=m.get("generation_id"), duration_s=round(d, 2) if d else None,
                             aligned=m.get("alignment_matched_words"))
        detail = (f"prise {m.get('generation_id') or '—'}, {d:.2f} s, {m.get('alignment_matched_words', '?')} mots "
                  f"alignés" + (", verrouillée" if locked else ""))
        if d is not None and d > limit:
            r.add(FAIL, "voix", f"{detail} : dépasse la limite {limit:.1f} s (QA {qa_max:g} s)",
                  "demande à l'utilisateur (accélérer ≤ 4 %, durée plus longue dans config.yaml "
                  "qa.max_duration_by_video, ou script plus court)")
        else:
            r.add(OK, "voix", f"{detail} (limite {limit:.1f} s)")
        repo = root.parent
        if not (git_tracked(repo, mp3) and git_tracked(repo, meta)):
            r.add(WARN, "voix versionnée", f"cache/tts/{key}.* pas encore commité",
                  f"git add wth-videos/cache/tts/{key}.mp3 wth-videos/cache/tts/{key}.json, commit, push")
        b = root / "build" / vid
        prepared = [n for n in ("tts.json", "words.json", "audio.wav") if (b / n).exists()]
        stale = False
        if (b / "tts.json").exists():
            try:
                stale = json.loads((b / "tts.json").read_text(encoding="utf-8")).get("cache_key") != key
            except json.JSONDecodeError:
                stale = True
        if len(prepared) < 3 or stale:
            gone = [n for n in ("tts.json", "words.json", "audio.wav") if n not in prepared]
            why = ("tts.json pointe vers une autre voix" if stale else "manque " + ", ".join(gone))
            r.add(FAIL, "voix préparée", f"build/{vid}/ : {why}",
                  f"make voice ID={vid} (dans wth-videos/ ; aucun appel réseau, voix en cache)")
        else:
            r.add(OK, "voix préparée", f"build/{vid}/tts.json, words.json, audio.wav")

    # Storyboard, mise en scène, QA : informations pour choisir la prochaine étape.
    sb = root / "scripts" / "storyboards" / f"{vid}.json"
    if sb.exists():
        try:
            version = json.loads(sb.read_text(encoding="utf-8")).get("version", "sans version")
        except json.JSONDecodeError:
            version = "JSON illisible"
        sb_info = {"exists": True, "version": version, "check": None}
        if (root / "build" / vid / "words.json").exists():
            c = subprocess.run([sys.executable, "-m", "pipeline.story", vid, "--check"], cwd=root,
                               capture_output=True, text=True)
            out = [x.strip() for x in (c.stdout + c.stderr).strip().splitlines() if x.strip()]
            errors = [x.lstrip("✘ ").strip() for x in out if x.startswith("✘")] or out[-1:]
            sb_info["check"] = "ok" if c.returncode == 0 else "refused"
            sb_info["check_errors"] = errors[:6]
            if c.returncode == 0:
                r.add(OK, "storyboard", f"{version} : --check OK")
            else:
                r.add(INFO, "storyboard", f"{version} : refusé par --check ({'; '.join(errors)[:240]})",
                      "skill wth-storyboard, revise.wf.js (ou retouche à la main)")
        else:
            r.add(INFO, "storyboard", f"{version} (contrôle impossible sans words.json)")
        info["storyboard"] = sb_info
    else:
        info["storyboard"] = {"exists": False}
        r.add(INFO, "storyboard", "absent", "skill wth-storyboard (storyboard.wf.js)")
    single, pkg = root / "scripts" / "story" / f"{vid}.py", root / "scripts" / "story" / vid / "__init__.py"
    if single.exists() and pkg.exists():
        r.add(FAIL, "mise en scène", f"scripts/story/{vid}.py ET scripts/story/{vid}/ : refusé par pipeline.story",
              "garde le paquet, archive l'autre hors de scripts/story/")
    elif single.exists() or pkg.exists():
        r.add(INFO, "mise en scène", f"scripts/story/{vid}{'.py' if single.exists() else '/'} présente",
              f"make story-staging ID={vid} dit si le film entier est rendable")
    info["spec"] = single.exists() or pkg.exists()
    qa = root / "output" / "qa" / f"{vid}.json"
    if qa.exists():
        try:
            qd = json.loads(qa.read_text(encoding="utf-8"))
            r.add(INFO, "QA existante", f"mode {qd.get('mode') or 'classique'}, {'OK' if qd.get('ok') else 'en échec'} "
                                        f"({qd.get('checked_at', '?')})")
            info["qa"] = {"mode": qd.get("mode"), "ok": qd.get("ok")}
        except json.JSONDecodeError:
            pass
    return r, info


def main():
    p = argparse.ArgumentParser(description="Contrôle avant production WTH")
    p.add_argument("ids", nargs="+")
    p.add_argument("--root", default=str(default_root()))
    p.add_argument("--json", action="store_true")
    p.add_argument("--no-voice", action="store_true", help="voix absente = alerte (avant la recette voix)")
    p.add_argument("--no-clean", action="store_true", help="ne lance pas make clean-tmp si le disque est bas")
    a = p.parse_args()
    root = Path(a.root).resolve()
    sys.path.insert(0, str(root))
    os.chdir(root)
    from pipeline import common  # noqa: E402
    cfg = common.load_config()
    scripts = common.load_scripts()
    try:
        videos_csv = common.videos()
    except OSError:
        videos_csv = {}
    rows = manifest_rows(root)

    env = check_env(root, a)
    per = {}
    for vid in a.ids:
        rep, info = check_video(root, vid, scripts, videos_csv, rows, cfg, a, common)
        per[vid] = (rep, info)
    blocking = [("environnement", i) for i in env.blocking] + [(v, i) for v, (rep, _) in per.items()
                                                                  for i in rep.blocking]
    if a.json:
        print(json.dumps({
            "ok": not blocking,
            "env": env.items,
            "videos": {v: {"ok": not rep.blocking, "checks": rep.items, **info} for v, (rep, info) in per.items()},
            "missing": [{"where": w, **i} for w, i in blocking],
        }, ensure_ascii=False, indent=2))
        sys.exit(1 if blocking else 0)

    def show(rep):
        for i in rep.items:
            line = f"  {MARK[i['level']]} {i['name']}" + (f" : {i['detail']}" if i["detail"] else "")
            if i["fix"] and i["level"] != OK:
                line += f"\n      → {i['fix']}"
            print(line)

    print("Environnement")
    show(env)
    for vid, (rep, info) in per.items():
        print(f"\n{vid}" + (f" « {info.get('title')} »" if info.get("title") else ""))
        show(rep)
    if blocking:
        print("\nManque :")
        for where, i in blocking:
            print(f"  ✘ {where} — {i['name']} : {i['detail']}" + (f"\n      → {i['fix']}" if i["fix"] else ""))
        sys.exit(1)
    print("\nRien ne manque.")


if __name__ == "__main__":
    main()
