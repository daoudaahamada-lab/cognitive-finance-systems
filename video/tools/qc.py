# -*- coding: utf-8 -*-
"""Contrôles automatiques du MP4 final : métadonnées, silences, sous-titres, calculs, captures."""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MP4 = os.path.join(ROOT, "dist", "agentic-wealth_audit-cgp_fr.mp4")
SRT = os.path.join(ROOT, "dist", "agentic-wealth_audit-cgp.fr.srt")
FR = os.path.join(ROOT, "dist", "frames")
os.makedirs(FR, exist_ok=True)
sys.path.insert(0, os.path.join(ROOT, "script"))
from script import SCENES  # noqa: E402

res = {}
pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", MP4],
                               capture_output=True, text=True).stdout)
res["duree_s"] = float(pr["format"]["duration"])
res["streams"] = [{k: s.get(k) for k in ("codec_type", "codec_name", "width", "height", "r_frame_rate", "sample_rate", "channels", "duration")} for s in pr["streams"]]
res["taille_mo"] = round(int(pr["format"]["size"]) / 1e6, 1)

# silences > 2,5 s à -45 dB dans la piste finale
sd = subprocess.run(["ffmpeg", "-hide_banner", "-i", MP4, "-af", "silencedetect=noise=-45dB:d=2.5", "-vn", "-f", "null", "-"],
                    capture_output=True, text=True).stderr
res["silences_sup_2_5s"] = re.findall(r"silence_start: ([\d.]+)", sd)
# plus longue pause de voix (sans la nappe) d'après la timeline
tl = json.load(open(os.path.join(ROOT, "build", "timeline.json")))
sents = [s for sc in tl["scenes"] for b in sc["beats"] for s in b["sentences"]]
gaps = [(round(b["start"] - a["end"], 2), round(a["end"], 1)) for a, b in zip(sents, sents[1:])]
res["pause_voix_max_s"] = max(gaps)
res["pauses_voix_sup_2s"] = [g for g in gaps if g[0] > 2.0]
# loudness
ln = subprocess.run(["ffmpeg", "-hide_banner", "-i", MP4, "-af", "ebur128", "-vn", "-f", "null", "-"], capture_output=True, text=True).stderr
m = re.findall(r"I:\s+(-?[\d.]+) LUFS", ln)
res["lufs_integre"] = float(m[-1]) if m else None

# sous-titres
srt = open(SRT, encoding="utf-8").read()
cues = re.findall(r"(\d\d:\d\d:\d\d,\d\d\d) --> (\d\d:\d\d:\d\d,\d\d\d)\n(.*?)\n\n", srt, re.S)
res["srt_cues"] = len(cues)
res["srt_lignes_max"] = max(len(c[2].split("\n")) for c in cues)
res["srt_car_max_ligne"] = max(len(l) for c in cues for l in c[2].split("\n"))
res["tirets_cadratin_srt"] = srt.count("\u2014") + srt.count("\u2013")
txt = " ".join(b[1] for s in SCENES for b in s["beats"])
res["tirets_cadratin_script"] = txt.count("\u2014") + txt.count("\u2013")
web = "".join(open(os.path.join(ROOT, "web", f), encoding="utf-8").read() for f in os.listdir(os.path.join(ROOT, "web")) if f.endswith(".js") and f != "timeline.js")
res["tirets_cadratin_ecran"] = web.count("\u2014") + web.count("\u2013")
res["mots_prononces"] = len(re.findall(r"[\wÀ-ÿ'-]+", txt))
res["calculs"] = {"8+9+7": 8 + 9 + 7, "4+6+4": 4 + 6 + 4, "gains 4+3+3": 4 + 3 + 3, "10x46": 10 * 46, "460x60": 460 * 60,
                  "note 13+6+7+9+10": 13 + 6 + 7 + 9 + 10}

# captures aux moments clés (ancre -> temps)
anchors = {}
for sc in tl["scenes"]:
    anchors["scene:" + sc["id"]] = sc["start"]
    for b in sc["beats"]:
        anchors[b["id"]] = b
def at(bid, k=None, off=0.0):
    b = anchors[bid]
    return (b["sentences"][k]["start"] if k is not None else b["start"]) + off
shots = [("01_accroche", at("h_460", None, 4.0)), ("02_titre", at("t_disc", None, 4)), ("03_cabinet", at("c_relay", None, 2.5)),
         ("04_audit_note", at("a_not", None, 3)), ("05_domaines", at("a_rule", None, 4)), ("06_agent1_sources", at("p_2b", None, 3.8)),
         ("07_agent1_brief", at("p_7", 3, 1.5)), ("08_agent1_cr", at("p_10", 2, 2.0)), ("09_agent1_taches", at("p_11b", 2, 1.0)),
         ("10_agent2_kanban", at("d_amb", 2, 2.5)), ("11_agent2_humain", at("d_human", 1, 2.5)), ("12_agent3_brouillon", at("s_karim", 2, 1.5)),
         ("13_agent3_cockpit", at("s_arb", 1, 1.0)), ("14_donnees", at("x_flow", 1, 6.0)), ("15_bilan", at("b_cap", None, 3)),
         ("16_bilan_euros", at("b_not", 1, 4)), ("17_planning", at("y_not3", None, 2)), ("18_cta", at("y_cta2", None, 5)), ("19_fin", res["duree_s"] - 1.0)]
for name, t in shots:
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", MP4, "-frames:v", "1", "-q:v", "3",
                    os.path.join(FR, f"{name}_{int(t // 60):02d}m{t % 60:04.1f}s.jpg")], check=True)
res["captures"] = sorted(os.listdir(FR))
json.dump(res, open(os.path.join(ROOT, "build", "qc.json"), "w"), ensure_ascii=False, indent=1)
print(json.dumps(res, ensure_ascii=False, indent=1))
