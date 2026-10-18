"""Contrôle qualité automatique d'une vidéo -> output/qa/Vxx.json et output/qa_report.md."""
import argparse
import math
import re
import subprocess
import unicodedata
from datetime import datetime, timezone

import numpy as np

from .common import OUTPUT, build_dir, ffprobe, load_config, read_json, run, script, videos, write_json
from .subs import Measure
from .words import tokenize

QA_DIR = OUTPUT / "qa"
MOJIBAKE = re.compile(r"Ã.|Â.|â€|\ufffd|Å“|Ã©")
ACTIVE = re.compile(r"\{\\1c[^}]*\}(.*?)\{\\r\}")
TAGS = re.compile(r"\{[^}]*\}")
ALLOW = {"wealthtech", "fintech", "open", "banking", "etf", "nasdaq", "msci", "world", "regafi", "orias", "dsp2",
         "pea", "per", "dic", "amf", "acpr", "rgpd", "cgp", "ia", "crm", "pdf", "pacs", "s&p", "app", "apps",
         "abonne-toi", "toi", "agrégateur", "agrégateurs", "wealthtechhorizon"}


def parse_ass(path):
    events = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("Dialogue:"):
            continue
        parts = line.split(",", 9)
        start, end, text = parts[1], parts[2], parts[9]
        events.append({"start": ass_seconds(start), "end": ass_seconds(end), "text": text})
    return events


def ass_seconds(t):
    h, m, s = t.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


def pcm(path, rate=16000):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(rate), "-f", "f32le", "-"],
                         check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32)


def audio_offset(ref, test, rate=16000, window=20.0, max_lag=1.0):
    """Décalage (s) de la piste du MP4 par rapport à l'audio en cache, par corrélation croisée."""
    a = ref[: int(window * rate)]
    b = test[: int((window + max_lag) * rate)]
    n = 1 << math.ceil(math.log2(len(a) + len(b)))
    corr = np.fft.irfft(np.fft.rfft(b, n) * np.conj(np.fft.rfft(a, n)), n)
    lags = np.concatenate([corr[: int(max_lag * rate)], corr[-int(max_lag * rate):]])
    idx = int(np.argmax(lags))
    lag = idx if idx < int(max_lag * rate) else idx - 2 * int(max_lag * rate)
    return lag / rate


def loudness(path):
    out = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-map", "0:a", "-af", "ebur128=peak=true",
               "-f", "null", "-"]).stderr
    summary = out[out.rfind("Summary:"):]
    integrated = float(re.search(r"I:\s+(-?[\d.]+) LUFS", summary).group(1))
    peak = float(re.search(r"Peak:\s+(-?[\d.]+|-inf) dBFS", summary).group(1))
    return integrated, peak


def check(name, ok, value, expected, detail=""):
    return {"check": name, "ok": bool(ok), "value": value, "expected": expected, "detail": detail}


def spell_warnings(text):
    try:
        from spellchecker import SpellChecker
    except ImportError:
        return ["pyspellchecker absent : vérification orthographique non faite"]
    sp = SpellChecker(language="fr")
    unknown = []
    for raw in text.split():
        token = raw.strip(".,;:!?…«»\u00a0").replace("\u00a0", " ")
        for part in re.split(r"[-\s]", token):
            part = part.split("’")[-1]
            low = part.lower()
            if not part or any(c.isdigit() for c in part) or part.isupper() or low in ALLOW or not part.isalpha():
                continue
            if low not in sp:
                unknown.append(part)
    return sorted(set(unknown))


def qa_video(video_id):
    cfg = load_config()
    q, sc = cfg["qa"], cfg["subtitles"]
    s = script(video_id)
    out_dir = build_dir(video_id)
    mp4 = OUTPUT / f"WTH-{video_id}.mp4"
    tts = read_json(out_dir / "tts.json")
    wdata = read_json(out_dir / "words.json")
    words = wdata["words"]
    events = parse_ass(out_dir / "subs.ass")
    probe = ffprobe(mp4)
    results = []

    # Durée et format
    duration = float(probe["format"]["duration"])
    results.append(check("Durée", q["min_duration"] <= duration <= q["max_duration"], f"{duration:.2f} s",
                         f"{q['min_duration']:.0f} à {q['max_duration']:.0f} s"))
    vs = next(st for st in probe["streams"] if st["codec_type"] == "video")
    aus = next((st for st in probe["streams"] if st["codec_type"] == "audio"), {})
    fmt = f"{vs['codec_name']} {vs['width']}x{vs['height']} {vs['avg_frame_rate']} {vs['pix_fmt']} + {aus.get('codec_name')}"
    results.append(check("Format", fmt == f"h264 1080x1920 {cfg['video']['fps']}/1 yuv420p + aac", fmt,
                         f"h264 1080x1920 {cfg['video']['fps']}/1 yuv420p + aac"))

    # Synchronisation : début de surbrillance vs alignement, quantification à l'image, décalage audio
    active = [(e["start"], ACTIVE.search(e["text"]).group(1)) for e in events if ACTIVE.search(e["text"])]
    fps = cfg["video"]["fps"]
    if len(active) == len(words):
        diffs = [abs(t - w["start"]) for (t, _), w in zip(active, words)]
        frame_lag = [math.ceil(t * fps - 1e-6) / fps - t for t, _ in active]
        sub_err = max(diffs) + max(frame_lag)
    else:
        sub_err = float("inf")
    ref, test = pcm(tts["audio"]), pcm(mp4)
    offset = audio_offset(ref, test)
    total_ms = (sub_err + abs(offset)) * 1000
    results.append(check("Synchro sous-titres", total_ms < q["max_sync_ms"], f"{total_ms:.0f} ms",
                         f"< {q['max_sync_ms']} ms",
                         f"sous-titres/alignement + image : {sub_err * 1000:.0f} ms ; décalage audio MP4 : "
                         f"{offset * 1000:.0f} ms"))

    # Mots coupés
    tokens = [wdata["text"][a:b] for a, b in tokenize(wdata["text"])]
    shown = [w for _, w in active]
    measure = Measure(cfg["brand"]["font_bold_file"], sc["font_size"])
    widest = max((measure.width(TAGS.sub("", e["text"])) for e in events), default=0)
    ref_dur = len(ref) / 16000
    tail_rms = float(np.sqrt(np.mean(ref[-800:] ** 2))) if len(ref) else 0.0
    tail_db = 20 * math.log10(max(tail_rms, 1e-9))
    problems = []
    if shown != tokens:
        problems.append(f"{len(shown)} mots surlignés pour {len(tokens)} mots dans le texte")
    if widest > sc["max_width_px"]:
        problems.append(f"groupe trop large : {widest:.0f} px")
    if wdata.get("unmatched_chars", 0):
        problems.append(f"{wdata['unmatched_chars']} caractère(s) du texte absents de l'alignement ElevenLabs")
    if words[-1]["end"] > ref_dur - 0.02:
        problems.append("dernier mot collé à la fin du fichier audio")
    if tail_db > -40:
        problems.append(f"fin d'audio non silencieuse ({tail_db:.0f} dBFS)")
    if duration < words[-1]["end"] + 0.2:
        problems.append("vidéo coupée avant la fin du dernier mot")
    results.append(check("Aucun mot coupé", not problems, "ok" if not problems else "; ".join(problems),
                         "tous les mots, entiers, dans la largeur",
                         f"{len(tokens)} mots, groupe le plus large {widest:.0f}/{sc['max_width_px']} px"))

    # Accents et caractères
    text = s["texte"]
    ass_text = (out_dir / "subs.ass").read_text(encoding="utf-8")
    issues = []
    if unicodedata.normalize("NFC", text) != text:
        issues.append("texte non normalisé NFC")
    if MOJIBAKE.search(text) or MOJIBAKE.search(ass_text):
        issues.append("caractères mal encodés")
    missing = measure.missing_glyphs(text + s["titre"])
    if missing:
        issues.append(f"glyphes absents de la police : {''.join(missing)}")
    if wdata["text"] != text:
        issues.append("audio verrouillé sur un texte différent de scripts.json")
    unknown = spell_warnings(text)
    results.append(check("Accents et caractères", not issues, "ok" if not issues else "; ".join(issues),
                         "UTF-8 NFC, glyphes présents, aucun mojibake",
                         f"mots hors dictionnaire à relire : {', '.join(unknown)}" if unknown else
                         "aucun mot hors dictionnaire"))

    # Saturation et loudness
    integrated, true_peak = loudness(mp4)
    clipped = int(np.sum(np.abs(test) >= 0.999))
    tol = q["loudness_tolerance"]
    target = cfg["loudness"]["integrated"]
    results.append(check("Pas de saturation", clipped == 0 and true_peak <= q["max_true_peak"],
                         f"true peak {true_peak:.1f} dBTP, {clipped} échantillon(s) écrêté(s)",
                         f"≤ {q['max_true_peak']} dBTP, 0 écrêtage"))
    results.append(check("Loudness", abs(integrated - target) <= tol, f"{integrated:.1f} LUFS",
                         f"{target:.0f} ± {tol:.0f} LUFS"))

    report = {
        "id": video_id,
        "source": s["source"],
        "file": str(mp4.relative_to(OUTPUT.parent)),
        "checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "ok": all(r["ok"] for r in results),
        "checks": results,
    }
    write_json(QA_DIR / f"{video_id}.json", report)
    write_report()
    print(f"{video_id} : QA {'OK' if report['ok'] else 'ÉCHEC'}")
    for r in results:
        print(f"  {'✔' if r['ok'] else '✘'} {r['check']} : {r['value']}")
    return report


def write_report():
    lines = ["# Rapport qualité — vidéos WealthTech Horizon", ""]
    reports = [read_json(QA_DIR / f"{vid}.json") for vid in videos() if (QA_DIR / f"{vid}.json").exists()]
    lines += ["| Vidéo | Source | Résultat | Durée | Synchro | Loudness | Contrôlée le |", "|---|---|---|---|---|---|---|"]
    for r in reports:
        by = {c["check"]: c for c in r["checks"]}
        lines.append(f"| {r['id']} | {r['source']} | {'✅ OK' if r['ok'] else '❌ ÉCHEC'} | {by['Durée']['value']} | "
                     f"{by['Synchro sous-titres']['value']} | {by['Loudness']['value']} | {r['checked_at']} |")
    for r in reports:
        lines += ["", f"## {r['id']} ({r['source']}) — {'OK' if r['ok'] else 'ÉCHEC'}", "",
                  "| Contrôle | Résultat | Valeur | Attendu | Détail |", "|---|---|---|---|---|"]
        for c in r["checks"]:
            lines.append(f"| {c['check']} | {'✔' if c['ok'] else '✘'} | {c['value']} | {c['expected']} | "
                         f"{c['detail']} |")
    (OUTPUT / "qa_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("id")
    report = qa_video(p.parse_args().id)
    raise SystemExit(0 if report["ok"] else 1)


if __name__ == "__main__":
    main()
