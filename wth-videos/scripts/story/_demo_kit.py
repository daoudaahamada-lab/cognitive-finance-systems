"""Démonstration du kit Story (pipeline/story_kit.py) : PAS une vidéo de la série. Vitrine de 6,7 s calée sur la voix
de V01, scènes S18 à S20 (« Avant, tu arrives en ayant cherché. Après, tu arrives en ayant compris. Abonne-toi pour
comprendre ton argent. ») : la figurine marche et tapote, les lignes d'une fiche s'écrivent, une jauge se vide, un
compteur compte, la pointe relit la colonne des coches, un coup de tampon, puis la fin standard (outro).

    python3 scripts/story/_demo_kit.py --props                 props -> build/kit_demo/props_demo.json
    python3 scripts/story/_demo_kit.py --stills 0 21 42 …     images fixes (images de la démo) -> build/kit_demo/stills_demo/
    python3 scripts/story/_demo_kit.py --clip                  clip avec voix et sous-titres -> build/kit_demo/demo_kit.mp4

Le constructeur est celui de pipeline.story (build_props), avec cette mise en scène à la place de scripts/story/V01.py
et des sorties sous build/kit_demo/ (rien n'est écrit dans build/V01/ ni output/).
"""
import sys
from pathlib import Path

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from pipeline.story import GEOM, STYLE  # noqa: E402
from pipeline.story_kit import Figure, Kit, Sheet  # noqa: E402

T_FROM, T_TO = 51.038, 99.0          # S18 « Avant, » -> fin de la voix
CYAN, DEEP, RED = STYLE["cyan"], STYLE["deep"], STYLE["red"]
LINES = [("Dossier", "12 docs", "bars"), ("Contrat", "AV 2019", "shield"), ("Objectif", "retraite", "cal")]
SHEET_AT, SHEET_SCALE = [390, 820], 0.9   # fiche : y 590-1050
TOI_AT = [880, 955]                  # pied à y 1050, au ras du bas de la fiche


def build(S):
    kit = Kit(S)
    sheet = Sheet(n=3)

    # ---------- distribution (état à l'ouverture de la fenêtre : rien n'est vide) ----------
    kit.steps_marker(["Avant", "Après"], y=290)
    kit.gauge("temps", [560, 410], value=1, w=480, h=40, segments=6)
    S.set("temps", fill=CYAN)                          # piste de couleur : hex, pour le fondu vers le rouge
    kit.icon("horloge", [250, 410], "clock", disc=34)
    kit.counter("minutes", [560, 500], value=0, size=56, suffix=" min")
    S.set("minutes", color=STYLE["ink"])
    rows = sheet.add(kit, "fiche", LINES, pos=SHEET_AT, scale=SHEET_SCALE, title="Brief")
    ticks = sheet.ticks(kit, "coche", DEEP)
    S.add("tampon", "stamp", z=11.8, parent="fiche", text="COMPRIS", w=232, h=68, size=36)
    S.set("tampon", pos=[118, 196], rot=-8, scale=0, handle=1, opacity=0)   # en bas à droite : à portée de main
    toi = Figure(kit, "toi", pos=TOI_AT)

    # ---------- S18 « Avant, tu arrives en ayant cherché. » ----------
    f = kit.at("S18", "Avant,", "la jauge de temps se vide, le compteur de minutes monte")
    g = kit.at("S18", "cherché.", "la jauge passe au rouge, le compteur bat")
    S.key("temps", "value", f, 0.15, g - f, "linear")
    S.key("minutes", "value", f, 45, g - f, "inOut")
    f = kit.at("S18", "arrives", "la figurine arrive en marchant ; les lignes de la fiche s'écrivent une à une")
    toi.walk(f, toi.place_for([sheet.world(S, i, "tick", n=f) for i in range(3)], f - 1))   # d'où elle relira tout
    kit.stagger(rows, f, 6, kit.type, rate=2, flash=True)
    S.key("temps", "fill", g, RED, 6, "out")
    S.key("minutes", "color", g, RED, 6, "out")
    kit.pulse("minutes", g)
    kit.shake("temps", g, amp=5)

    # ---------- S19 « Après, tu arrives en ayant compris. » ----------
    f = kit.at("S19", "Après,", "repère sur « Après » ; jauge et compteur se retirent ; la figurine tapote la coche "
               "de la 1re ligne, qui se trace au contact")
    kit.pin(f, {"fiche": {"pos": SHEET_AT, "scale": SHEET_SCALE}})
    kit.step(f, 1)
    kit.morph(["temps", "minutes", "horloge"], [], f)
    hit = toi.tap(f, sheet.world(S, 0, "tick", n=f))
    kit.draw(ticks[0], hit, 6)
    f = kit.at("S19", "arrives", "la pointe relit la colonne des coches à vitesse constante ; chaque coche se trace "
               "sous la pointe")
    hits = toi.trace(f, [sheet.world(S, i, "tick", n=f) for i in range(3)])
    for t, h in zip(ticks[1:], hits[1:]):
        kit.draw(t, h, 6)
    f = kit.at("S19", "compris.", "coup de tampon COMPRIS en bas de la fiche, la fiche tremble")
    toi.stamp(f, "tampon", shake="fiche")

    # ---------- S20 « Abonne-toi pour comprendre ton argent. » ----------
    out = kit.outro("S20", outs=["fiche", "marqueur"], press="comprendre")
    toi.exit(out["card"])
    kit.hold("S20", "argent.", "tenue : la carte de fin reste immobile")


def _main():
    import argparse
    import shutil

    from pipeline import story
    from pipeline.common import ROOT, load_config

    out = ROOT / "build" / "kit_demo"
    p = argparse.ArgumentParser(description="Démonstration du kit Story (fenêtre S18-S20 de V01)")
    p.add_argument("--props", action="store_true")
    p.add_argument("--stills", nargs="+", type=int, metavar="IMAGE")
    p.add_argument("--clip", action="store_true")
    p.add_argument("--no-captions", action="store_true")
    a = p.parse_args()
    me = sys.modules[__name__]
    story.load_spec = lambda vid: (me, Path(__file__).resolve())
    story.outputs = lambda vid, label, full: {
        "props": {True: out / "props_demo.json", False: out / "props_demo_nocap.json"},
        "silent": {True: out / "muet_demo.mp4", False: out / "muet_demo_nocap.mp4"},
        "mp4": {True: out / "demo_kit.mp4", False: out / "demo_kit_nocap.mp4"}, "wav": out / "voix_demo.wav"}
    cap = not a.no_captions
    path, props = story.build_props("V01", T_FROM, T_TO, captions=cap)
    if a.stills:
        dst = out / "stills_demo"
        with story.render_lock("images fixes démo kit") as tmp_env:
            proc = story.subprocess.run(["node", "scripts/story_stills.mjs", str(path), str(dst), *map(str, a.stills)],
                                        cwd=story.MOTION, text=True, capture_output=True,
                                        env=story.remotion_env(**tmp_env))
        if proc.returncode != 0:
            print(proc.stdout[-3000:], proc.stderr[-3000:])
            raise SystemExit("Images fixes en échec")
        print(f"{len(a.stills)} images fixes -> {dst}")
    if a.clip:
        cfg = load_config()
        f0, f1 = props["meta"]["window_frames"]
        fps = props["fps"]
        paths = story.outputs("V01", "", False)
        story.cut_audio(story.build_dir("V01") / "audio.wav", f0, f1, fps, paths["wav"])
        story.remotion_render(path, paths["silent"][cap])
        story.mux(paths["silent"][cap], paths["wav"], paths["mp4"][cap], (f1 - f0) / fps, cfg,
                  {"wth_mode": "demo", "wth_window": f"{f0}-{f1}"})
        paths["silent"][cap].unlink(missing_ok=True)
        shutil.rmtree(out / "frames", ignore_errors=True)


if __name__ == "__main__":
    _main()
