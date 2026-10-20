"""Test hors rendu de l'outillage Story (pipeline/story.py, qa.py, render.py), sur la voix et la mise en scène de V01.

    python3 -m tests.story_smoke [--qa]      --qa : + contrôles image de la QA story sur l'extrait validé

Aucun rendu Remotion : seulement la construction des props, le contrôle du storyboard et les garde-fous. Les sorties
vont dans un dossier temporaire (WTH_BUILD, WTH_OUTPUT), où sont copiés build/V01/words.json, tts.json et audio.wav.
- une fenêtre de V01 sans les découpes de sous-titres imposées (CAPTION_GROUPS) se construit, avec les groupes du film ;
- le film entier sur la mise en scène partielle de V01 s'arrête en nommant les scènes non mises en scène
  (--allow-partial : props_film.json) ;
- --check sur V01.json : aucune erreur, sauf « idees_cles » tant que le storyboard v3 ne l'a pas ;
- mise en scène en paquet (scripts/story/Vxx/__init__.py + parties), règle des illustrations de carrousel, garde-fou
  qui protège un film Story contre le montage classique et `make motion` ;
- bras à cinématique inverse (pipeline/story_kit.py, s'il existe) : longueurs d'os constantes sur un trajet.
"""
import contextlib
import io
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TMP = Path(tempfile.mkdtemp(prefix="wth-story-smoke-"))
# Avant tout import de pipeline : build/ et output/ temporaires.
os.environ["WTH_BUILD"] = str(TMP / "build")
os.environ["WTH_OUTPUT"] = str(TMP / "output")

from pipeline import qa, render, story  # noqa: E402
from pipeline.common import read_json  # noqa: E402

VID = "V01"
EXCERPT = (25.612, 41.309)   # extrait validé (S11-S14)
NO_OVERRIDE = (41.309, 50.0)  # S15-S17 : aucune des découpes imposées de V01.py n'y tombe
RESULTS = []
CASES = []


class SkipTest(Exception):
    pass


def case(name, optional=False):
    def deco(fn):
        def run():
            buf = io.StringIO()     # rapports de build_props : montrés seulement en cas d'échec
            try:
                with contextlib.redirect_stdout(buf):
                    note = fn()
                RESULTS.append((name, True, note or ""))
            except SkipTest as e:
                RESULTS.append((name, None, str(e)))
            except (AssertionError, SystemExit, Exception) as e:  # noqa: BLE001
                tail = "\n      ".join(buf.getvalue().strip().splitlines()[-6:])
                RESULTS.append((name, False, f"{type(e).__name__}: {e}" + (f"\n      {tail}" if tail else "")))
        run.__name__ = fn.__name__
        run.optional = optional
        CASES.append(run)
        return run
    return deco


def setup():
    src = ROOT / "build" / VID
    dst = TMP / "build" / VID
    dst.mkdir(parents=True)
    for name in ("words.json", "tts.json", "audio.wav"):
        if not (src / name).exists():
            raise SystemExit(f"build/{VID}/{name} absent : make voice ID={VID} avant ce test")
        shutil.copy2(src / name, dst / name)   # copy2 garde la date : ensure_audio ne refait pas audio.wav


@case("fenêtre sans découpe imposée")
def window_without_overrides():
    mod, _ = story.load_spec(VID)
    runs = getattr(mod, "CAPTION_GROUPS", None) or []
    path, props = story.build_props(VID, *NO_OVERRIDE, captions=True)
    caps = props["captions"]
    assert caps, "aucun sous-titre dans la fenêtre"
    f0, f1 = props["meta"]["window_frames"]
    words = read_json(TMP / "build" / VID / "words.json")["words"]
    inside = [i for i, w in enumerate(words) if f0 <= round(w["start"] * props["fps"]) < f1]
    assert [w["i"] for g in caps for w in g["words"]] == inside, "mots de la fenêtre manquants ou en trop"
    shown = {" ".join(w["text"] for w in g["words"]) for g in caps}
    assert not shown & {g for r in runs for g in r}, "une découpe imposée tombe dans la fenêtre : test à revoir"
    # Mêmes groupes que le film (hors premier et dernier groupes, qui peuvent déborder de la fenêtre).
    film = story.caption_track(words, props["fps"], 0, 10 ** 6, runs,
                               alert_words=getattr(mod, "ALERT_WORDS", None))
    film_groups = {tuple(w["i"] for w in g["words"]) for g in film}
    assert all(tuple(w["i"] for w in g["words"]) in film_groups for g in caps[1:-1]), "découpe différente du film"
    return f"{path.name} : {len(caps)} groupes, mêmes groupes que le film"


@case("extrait validé : props inchangées")
def excerpt_props():
    path, props = story.build_props(VID, *EXCERPT, captions=True)
    base = ROOT / "build" / VID / "baseline" / "props_S11-S14.json"
    if not base.exists():
        raise SkipTest(f"{base} absent")
    a, b = read_json(path), read_json(base)
    meta_a, meta_b = a.pop("meta"), b.pop("meta")
    assert a == b, "props de l'extrait différentes de la référence (hors meta)"
    changed = [k for k in meta_b if meta_a.get(k) != meta_b[k]]
    assert not changed, f"meta modifiée : {changed}"
    return f"identiques à {base.relative_to(ROOT)} (champs meta ajoutés : {sorted(set(meta_a) - set(meta_b)) or 'aucun'})"


@case("film entier : scènes non mises en scène")
def full_film_refused():
    sb = read_json(story.STORYBOARDS / f"{VID}.json")
    dur = story.audio_duration(TMP / "build" / VID / "audio.wav")
    _, ex = story.build_props(VID, *EXCERPT, captions=False)
    staged = set(ex["meta"]["staged_scenes"])
    unstaged = [s["id"] for s in sb["scenes"] if s["id"] not in staged]
    if not unstaged:
        path, props = story.build_props(VID, 0.0, dur)
        assert path.name == "props_film.json"
        return "mise en scène complète : le film entier se construit"
    try:
        story.build_props(VID, 0.0, dur)
    except SystemExit as e:
        msg = str(e)
    else:
        raise AssertionError("le film entier aurait dû être refusé")
    line = next((ln for ln in msg.splitlines() if "scènes sans aucun temps fort" in ln), "")
    assert line, f"message sans la liste des scènes : {msg[:200]}"
    listed = line.split(":", 1)[1].replace(" ", "").split(",")
    assert listed == unstaged, f"scènes listées {listed}, attendu {unstaged}"
    assert not (TMP / "build" / VID / "story" / "props_film.json").exists(), "props écrites malgré le refus"
    path, props = story.build_props(VID, 0.0, dur, captions=False, allow_partial=True)
    assert path.name == "props_film_nocap.json" and props["frameOffset"] == 0
    words = read_json(TMP / "build" / VID / "words.json")["words"]
    assert sum(len(g["words"]) for g in props["captions"]) == len(words), "film : tous les mots sous-titrés"
    assert not qa.caption_gaps(props), f"images sans sous-titre : {qa.caption_gaps(props)[:3]}"
    return f"refusé ({', '.join(unstaged)}) ; --allow-partial -> {path.name}"


@case("--check sur le storyboard")
def check_storyboard():
    errors, warnings = story.check_storyboard(VID, read_json(TMP / "build" / VID / "words.json")["words"])
    others = [e for e in errors if "idees_cles" not in e]
    assert not others, "; ".join(others)
    if errors:
        return "seule erreur : « idees_cles » absent (attendu tant que le storyboard v3 n'est pas écrit)"
    return "OK" + (f" ({len(warnings)} avertissement(s))" if warnings else "")


@case("--check : erreurs détectées")
def check_storyboard_errors():
    words = read_json(TMP / "build" / VID / "words.json")["words"]
    sb = read_json(story.STORYBOARDS / f"{VID}.json")
    sb["scenes"][3]["t_start"] += 0.2                 # début hors mot et trou entre deux scènes
    sb["scenes"][5]["beats"][0]["t"] += 0.5           # temps fort introuvable
    sb["scenes"][7]["texte"] += " de trop"            # texte différent du script
    errors, _ = story.check_storyboard(VID, words, sb)
    want = [sb["scenes"][3]["id"] + " commence", "mot introuvable", "texte du script"]
    missing = [w for w in want if not any(w in e for e in errors)]
    assert not missing, f"erreurs non détectées : {missing}"
    return f"{len(errors)} erreurs détectées"


@case("mise en scène en paquet")
def spec_package():
    specs = TMP / "specs"
    pkg = specs / "VZZ"
    pkg.mkdir(parents=True)
    (pkg / "p1.py").write_text("def part(story):\n    story.parts.append('p1')\n", encoding="utf-8")
    (pkg / "__init__.py").write_text("from . import p1\n\n\ndef build(story):\n    p1.part(story)\n", encoding="utf-8")
    old = story.SPECS
    story.SPECS = specs
    try:
        mod, path = story.load_spec("VZZ")
        holder = type("S", (), {"parts": []})()
        mod.build(holder)
        assert holder.parts == ["p1"], holder.parts
        h1 = story.spec_sha1(path)
        (pkg / "p1.py").write_text("def part(story):\n    story.parts.append('p1 bis')\n", encoding="utf-8")
        assert story.spec_sha1(path) != h1, "l'empreinte du paquet ignore une partie"
        (specs / "VZZ.py").write_text("def build(story):\n    pass\n", encoding="utf-8")
        try:
            story.spec_path("VZZ")
        except SystemExit:
            pass
        else:
            raise AssertionError("Vxx.py et Vxx/ ensemble auraient dû être refusés")
    finally:
        story.SPECS = old
    return "import relatif des parties, empreinte de toutes les parties"


@case("illustrations : son propre carrousel")
def carousel_rule():
    words = read_json(TMP / "build" / VID / "words.json")["words"]
    S = story.Story(VID, words, read_json(story.STORYBOARDS / f"{VID}.json"))
    try:
        S.png("WTH-999-01")
    except SystemExit as e:
        assert "autre carrousel" in str(e), e
    else:
        raise AssertionError("illustration d'un autre carrousel acceptée")
    return "WTH-999-01 refusée pour V01"


def fake_mp4(path, tags):
    path.parent.mkdir(parents=True, exist_ok=True)
    meta = [x for k, v in tags.items() for x in ("-metadata", f"{k}={v}")]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=white:s=64x64:d=0.2", *meta,
                    "-movflags", "+use_metadata_tags", str(path)], check=True)


@case("garde-fou du film Story")
def guard():
    mp4 = TMP / "output" / f"WTH-{VID}.mp4"
    fake_mp4(mp4, {"wth_mode": "story", "comment": "Made with Remotion 4.0.535"})
    for by in ("classic", "motion"):
        try:
            render.guard_motion_output(VID, by=by)
        except SystemExit as e:
            assert "Story" in str(e), e
        else:
            raise AssertionError(f"le rendu {by} écraserait le film Story")
    os.environ["WTH_FORCE"] = "1"
    try:
        render.guard_motion_output(VID, by="classic")
    finally:
        os.environ.pop("WTH_FORCE")
    assert qa.caption_source(qa.ffprobe(mp4)) == "story", "QA : film Story pris pour un rendu motion"
    fake_mp4(mp4, {"wth_mode": "motion"})
    render.guard_motion_output(VID, by="motion")       # motion peut remplacer motion
    try:
        render.guard_motion_output(VID, by="classic")
    except SystemExit:
        pass
    else:
        raise AssertionError("le montage classique écraserait le rendu motion")
    story.archive_previous(VID, mp4)
    assert not mp4.exists() and list((TMP / "build" / VID / "archive").glob("WTH-V01_motion_*.mp4")), "pas archivé"
    return "classique et motion refusés sur un film Story (FORCE=1 passe) ; ancien rendu archivé"


@case("bras IK : longueurs constantes")
def ik_arm():
    try:
        from pipeline import story_kit
    except ImportError:
        raise SkipTest("pipeline/story_kit.py absent (E4)")
    solve = getattr(story_kit, "solve_ik", None) or getattr(story_kit, "ik2", None) or getattr(story_kit, "two_bone_ik", None)
    if solve is None:
        raise SkipTest("story_kit sans solveur IK exposé (solve_ik / ik2 / two_bone_ik)")
    import math
    shoulder, l1, l2 = (0.0, 0.0), 48.0, 44.0
    worst = 0.0
    for k in range(60):                              # trajet synthétique : cercle partiellement hors d'atteinte
        a = k / 60 * 2 * math.pi
        target = (70 * math.cos(a) + 25, 70 * math.sin(a) * 0.6)
        elbow, hand = solve(shoulder, target, l1, l2)[:2]
        worst = max(worst, abs(math.dist(shoulder, elbow) - l1), abs(math.dist(elbow, hand) - l2))
    assert worst < 1e-6, f"écart de longueur {worst:.2e} px"
    return f"écart max {worst:.1e} px sur 60 images"


@case("QA story : contrôles image sur l'extrait validé", optional=True)
def picture_checks():
    base = ROOT / "build" / VID / "baseline"
    mp4, nocap = base / "WTH-V01_extrait_S11-S14.mp4", base / "extrait_sans_sous_titres.mp4"
    if not (mp4.exists() and nocap.exists()):
        raise SkipTest(f"{base} incomplet")
    res = qa.story_picture_checks(mp4, nocap, read_json(base / "props_S11-S14.json"))
    bad = [f"{r['check']} : {r['value']}" for r in res if not r["ok"]]
    assert not bad, "; ".join(bad)
    return "; ".join(f"{r['check']} ({r['value']})" for r in res)


def main():
    with_qa = "--qa" in sys.argv[1:]   # + contrôles image de la QA story sur l'extrait validé (~40 s de décodage)
    setup()
    try:
        for c in CASES:
            if with_qa or not c.optional:
                c()
    finally:
        shutil.rmtree(TMP, ignore_errors=True)
    for name, ok, note in RESULTS:
        print(f"  {'✔' if ok else '–' if ok is None else '✘'} {name} : {note}")
    failed = [n for n, ok, _ in RESULTS if ok is False]
    print("ÉCHEC : " + ", ".join(failed) if failed else "OK : outillage Story")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
