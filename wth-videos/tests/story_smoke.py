"""Test hors rendu de l'outillage Story (pipeline/story.py, qa.py, render.py), sur la voix et la mise en scène de V01.

    python3 -m tests.story_smoke [--qa]      --qa : + contrôles image de la QA story sur l'extrait validé

Aucun rendu Remotion : seulement la construction des props, le contrôle du storyboard et les garde-fous. Les sorties
vont dans un dossier temporaire (WTH_BUILD, WTH_OUTPUT), où sont copiés build/V01/words.json, tts.json et audio.wav.
- une fenêtre de V01 sans les découpes de sous-titres imposées (CAPTION_GROUPS) se construit, avec les groupes du film ;
- le film entier sur la mise en scène partielle de V01 s'arrête en nommant les scènes non mises en scène
  (--allow-partial : props_film_partiel*.json, meta.partial) ; --staging le dit sans rien écrire ; un film partiel
  ne va jamais dans output/ et la QA « Mise en scène complète » le refuse ;
- QA story : pas de trou de sous-titres avant le premier mot (silence d'attaque), textes des pistes contrôlés ;
- verrou de rendu tenu par le rendu lui-même (processus Python tué : le verrou reste pris jusqu'à la fin du rendu ;
  SIGTERM : tout le groupe du rendu est arrêté, dossier temporaire supprimé) ;
- --check sur V01.json : aucune erreur, sauf « idees_cles » tant que le storyboard v3 ne l'a pas ;
- mise en scène en paquet (scripts/story/Vxx/__init__.py + parties), règle des illustrations de carrousel, garde-fou
  qui protège un film Story contre le montage classique et `make motion` ;
- bras à cinématique inverse (pipeline/story_kit.py, s'il existe) : longueurs d'os constantes sur un trajet, et
  image par image sur la figurine articulée (entrée, marche, tapotement, relecture, trait, tampon, sortie) ;
- macros du kit : pop, move et morph posent les clés documentées (.claude/skills/wth-story-build/references/kit.md).
"""
import contextlib
import fcntl
import io
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TMP = Path(tempfile.mkdtemp(prefix="wth-story-smoke-"))
# Avant tout import de pipeline : build/ et output/ temporaires.
os.environ["WTH_BUILD"] = str(TMP / "build")
os.environ["WTH_OUTPUT"] = str(TMP / "output")

from pipeline import motion, qa, render, story  # noqa: E402
from pipeline.common import read_json  # noqa: E402

VID = "V01"
EXCERPT = (25.612, 41.309)   # extrait validé (S11-S14)
NO_OVERRIDE = (41.309, 47.3)  # S15-S16 : aucune des découpes imposées de V01 n'y tombe
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
    assert path.name == "props_film_partiel_nocap.json" and props["frameOffset"] == 0, path.name
    assert props["meta"]["partial"] is True and props["meta"]["unstaged_scenes"] == unstaged, props["meta"].get("partial")
    words = read_json(TMP / "build" / VID / "words.json")["words"]
    assert sum(len(g["words"]) for g in props["captions"]) == len(words), "film : tous les mots sous-titrés"
    assert not qa.caption_gaps(props, from_first_word=True), f"images sans sous-titre : {qa.caption_gaps(props)[:3]}"
    return f"refusé ({', '.join(unstaged)}) ; --allow-partial -> {path.name}"


@case("film partiel : jamais dans output/, refusé par la QA")
def partial_film():
    out = story.partial_outputs(VID)
    build = (TMP / "build").resolve()
    for kind in ("props", "silent", "mp4"):
        for cap in (True, False):
            assert out[kind][cap].resolve().is_relative_to(build), f"{kind} {cap} : {out[kind][cap]} hors de build/"
    assert out["mp4"][True].name == "film_partiel.mp4"
    dur = story.audio_duration(TMP / "build" / VID / "audio.wav")
    _, props = story.build_props(VID, 0.0, dur, captions=True, allow_partial=True)
    probe = {"format": {"tags": {"wth_mode": "story", "wth_partial": "1"}}}
    r = qa.story_staging_check(probe, props)
    assert not r["ok"] and "scènes non mises en scène" in r["value"], r
    done = {**props, "meta": {**props["meta"], "partial": False, "unstaged_scenes": [], "storyboard_beats_missing": [],
                              "unstaged_before_frame": None}}
    assert not qa.story_staging_check({"format": {"tags": {"wth_partial": "1"}}}, done)["ok"], "balise wth_partial ignorée"
    assert qa.story_staging_check({"format": {"tags": {}}}, done)["ok"], "film complet refusé"
    return f"rendus partiels dans build/{VID}/story/ ; QA : {r['value'][:70]}…"


@case("film partiel : chaîne complète (rendu simulé)")
def partial_chain():
    out_mp4 = TMP / "output" / f"WTH-{VID}.mp4"
    fake_mp4(out_mp4, {"wth_mode": "motion"})                 # film livré (motion) : ne doit pas bouger
    before = qa.sha1_file(out_mp4)
    real = story.remotion_render

    def fake_render(props_path, silent):                     # vidéo muette du bon nombre d'images, sans Remotion
        n = read_json(props_path)["durationInFrames"]
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=0xF6F0E4:s=108x192:r=30",
                        "-frames:v", str(n), "-pix_fmt", "yuv420p", str(silent)], check=True)
    story.remotion_render = fake_render
    try:
        dur = story.audio_duration(TMP / "build" / VID / "audio.wav")
        res = story.excerpt(VID, 0.0, dur, captions=True, sheets=True, allow_partial=True)
    finally:
        story.remotion_render = real
    film = TMP / "build" / VID / "story" / "film_partiel.mp4"
    assert res[True] == film and res[False].name == "film_partiel_sans_sous_titres.mp4", res
    assert out_mp4.exists() and qa.sha1_file(out_mp4) == before, "film livré déplacé ou modifié"
    assert not (TMP / "build" / VID / "archive").exists(), "film livré archivé par un rendu partiel"
    assert not (TMP / "build" / VID / story.STORY_SIDECAR).exists(), "story_render.json écrit par un rendu partiel"
    tags = qa.mp4_tags(qa.ffprobe(film))
    assert tags.get("wth_partial") == "1" and tags.get("wth_mode") == "story", tags
    sheets = list((TMP / "build" / VID / "review" / "film_partiel" / "sheets").glob("*.jpg"))
    assert sheets, "pas de planches de revue du film partiel"
    return f"{film.name} (wth_partial=1), output/ inchangé, pas de fiche, {len(sheets)} planches"


@case("--staging : mise en scène pas prête, sans rien écrire")
def staging_check():
    before = sorted(p.name for p in (TMP / "build" / VID).rglob("*") if p.is_file())
    ready, msg = story.check_staging(VID)
    assert not ready and "scènes sans aucun temps fort" in msg, msg
    after = sorted(p.name for p in (TMP / "build" / VID).rglob("*") if p.is_file())
    assert after == before, f"fichiers écrits : {sorted(set(after) - set(before))}"
    specs = TMP / "specs_wip"
    (specs / "V01").mkdir(parents=True)        # paquet en cours d'écriture : une partie manque encore
    (specs / "V01" / "__init__.py").write_text("from . import p9\n\n\ndef build(story):\n    p9.part(story)\n")
    old = story.SPECS
    story.SPECS = specs
    try:
        ready, msg2 = story.check_staging(VID)
    finally:
        story.SPECS = old
    assert not ready and "en erreur" in msg2, msg2
    return f"{msg[:60]}… ; paquet incomplet : {msg2[:50]}…"


@case("QA story : sous-titres et textes des pistes")
def qa_story_texts():
    words = [{"w": "Bonjour", "start": 0.08, "end": 0.4}, {"w": "à", "start": 0.45, "end": 0.5},
             {"w": "toi", "start": 0.55, "end": 0.9}]
    caps = story.caption_track(words, 30, 0, 40)
    props = {"frameOffset": 0, "durationInFrames": 40, "captions": caps}
    assert caps[0]["from"] == 2 and qa.caption_gaps(props) == [(0, 2)]
    assert qa.caption_gaps(props, from_first_word=True) == [], qa.caption_gaps(props, from_first_word=True)
    ents = {"entities": [
        {"id": "verdict", "type": "text", "p": {"text": "Brouillon"},
         "t": {"text": [{"f": 0, "v": "Brouillon"}, {"f": 30, "v": "Validé"}]}},
        {"id": "pill", "type": "pill", "p": {"text": "Avant"}, "t": {"text": [{"f": 0, "v": "Avant"}, {"f": 9, "v": "Après"}]}},
        {"id": "c", "type": "counter", "p": {"prefix": "env. ", "suffix": " €"}, "t": {"value": [{"f": 0, "v": 0}]}}]}
    texts = qa.entity_texts(ents)
    want = {"Brouillon", "Validé", "Avant", "Après", "env. ", " €"}
    assert want <= set(texts), f"textes manquants : {want - set(texts)}"
    return "aucun trou avant le premier mot (images 0-1) ; pistes text et préfixe / suffixe contrôlés"


def _lock_busy(path):
    with open(path, "a+") as fh:
        try:
            fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return True
        fcntl.flock(fh, fcntl.LOCK_UN)
        return False


def _locked_child(cmd, tmpdir):
    """Processus Python qui lance `cmd` par motion.run_locked (verrou de TMP/build), et attend que le verrou soit pris."""
    code = f"from pipeline import motion; motion.run_locked({cmd!r}, 'test du verrou', cwd='.')"
    env = dict(os.environ, TMPDIR=str(tmpdir))
    proc = subprocess.Popen([sys.executable, "-c", code], cwd=ROOT, env=env)
    for _ in range(100):
        if _lock_busy(motion.RENDER_LOCK):
            return proc
        time.sleep(0.05)
    proc.kill()
    raise AssertionError("le verrou n'a jamais été pris")


@case("verrou de rendu tenu par le rendu")
def lock_held_by_render():
    assert motion.RENDER_LOCK.resolve().is_relative_to(TMP), motion.RENDER_LOCK   # jamais le vrai verrou
    tmpdir = TMP / "tmp_lock"
    tmpdir.mkdir()
    # 1. Python tué (SIGKILL) : le rendu orphelin garde le verrou jusqu'à sa fin.
    proc = _locked_child(["sh", "-c", "sleep 2.37"], tmpdir)
    proc.kill()
    proc.wait()
    time.sleep(0.3)
    assert _lock_busy(motion.RENDER_LOCK), "verrou rendu alors que le rendu orphelin tourne encore"
    t0 = time.time()
    while _lock_busy(motion.RENDER_LOCK) and time.time() - t0 < 10:
        time.sleep(0.1)
    assert not _lock_busy(motion.RENDER_LOCK), "verrou jamais rendu après la fin du rendu"
    for d in tmpdir.iterdir():          # TMPDIR du rendu tué : laissé (make clean-tmp le supprime sous le verrou)
        shutil.rmtree(d)
    # 2. SIGTERM : tout le groupe du rendu est arrêté, le verrou rendu, le dossier temporaire supprimé.
    proc = _locked_child(["sh", "-c", "sleep 30.37"], tmpdir)
    t0 = time.time()
    proc.send_signal(signal.SIGTERM)
    proc.wait(timeout=15)
    stopped = time.time() - t0
    alive = subprocess.run(["pgrep", "-f", "^sleep 30.37"], capture_output=True, text=True).stdout.split()
    for pid in alive:
        os.kill(int(pid), signal.SIGKILL)
    assert not alive, "rendu encore en vie après SIGTERM"
    assert not _lock_busy(motion.RENDER_LOCK), "verrou encore pris après SIGTERM"
    assert not list(tmpdir.iterdir()), f"dossier temporaire laissé : {list(tmpdir.iterdir())}"
    return f"tenu après SIGKILL du parent, rendu à la fin du rendu ; SIGTERM : groupe arrêté en {stopped:.1f} s"


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
    sb["scenes"][-1]["beats"] = []                    # scène sans temps fort : le film entier serait irréalisable
    errors, _ = story.check_storyboard(VID, words, sb)
    want = [sb["scenes"][3]["id"] + " commence", "mot introuvable", "texte du script",
            sb["scenes"][-1]["id"] + " : aucun temps fort"]
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


def _keys(S, id, track):
    """Clés d'une piste après la valeur initiale : (image, valeur, durée, assouplissement, arc)."""
    return [(k["f"], k["v"], k.get("d", 0), k.get("e"), k.get("arc")) for k in S.ents[id]["t"][track][1:]]


@case("kit : clés de pop, move, morph")
def kit_keys():
    try:
        from pipeline import story_kit as K
    except ImportError:
        raise SkipTest("pipeline/story_kit.py absent (E4)")
    S = story.Story("VZZ", [], {"scenes": []})
    kit = K.Kit(S)
    for id, pos, sc in (("a", [100, 200], 0), ("b", [300, 400], 1), ("c", [500, 600], 0)):
        S.add(id, "shape", z=1)
        S.set(id, pos=pos, scale=sc)
    P, M, MV = story.POP, story.MORPH, story.MOVE
    # pop : échelle 0 -> 1 en POP (ease-out) ; déjà à 0 : pas de clé à f - 1
    assert kit.pop("a", 10) == 10 + P
    assert _keys(S, "a", "scale") == [(10, 1, P, "out", None)], _keys(S, "a", "scale")
    # pop depuis un point : 0 à f - 1, naît en from_pt et glisse à sa place
    kit.pop("a", 40, scale=2, from_pt=[0, 0])
    assert _keys(S, "a", "scale")[1:] == [(39, 0, 0, None, None), (40, 2, P, "out", None)], _keys(S, "a", "scale")
    assert _keys(S, "a", "pos") == [(39, [0, 0], 0, None, None), (40, [100, 200], P, "out", None)], _keys(S, "a", "pos")
    assert S.val("a", "scale", 39) == 0 and S.val("a", "scale", 40 + P - 1) == 2
    # move : pos (+ arc) et scale, MOVE en ease-in-out
    assert kit.move("b", 20, [350, 420], arc=30, scale=1.5) == 20 + MV
    assert _keys(S, "b", "pos") == [(20, [350, 420], MV, "inOut", 30)], _keys(S, "b", "pos")
    assert _keys(S, "b", "scale") == [(20, 1.5, MV, "inOut", None)], _keys(S, "b", "scale")
    # morph apparié b -> c : b se réduit vers la place de c, c naît à la place de b, mêmes images
    assert kit.morph(["b"], ["c"], 60) == 60 + M
    assert _keys(S, "b", "scale")[-1] == (60, 0, M, "out", None)
    assert _keys(S, "b", "pos")[-1] == (60, [500, 600], M, "out", None)
    assert _keys(S, "b", "opacity") == [(60 + M, 0, 0, None, None)]
    assert _keys(S, "c", "pos") == [(59, [350, 420], 0, None, None), (60, [500, 600], M, "out", None)]
    assert _keys(S, "c", "scale") == [(60, 1, M, "out", None)]
    assert S.val("b", "scale", 60 + M - 1) == 0 and S.val("c", "scale", 60 + M - 1) == 1
    return "pop (0 à f - 1, from_pt), move (arc, scale), morph apparié : clés et valeurs attendues"


@case("figurine : bras de longueur fixe image par image")
def rig_arm():
    try:
        from pipeline import story_kit as K
    except ImportError:
        raise SkipTest("pipeline/story_kit.py absent (E4)")
    import math
    S = story.Story("VZZ", [], {"scenes": []})
    kit = K.Kit(S)
    sheet = K.Sheet(3)
    sheet.add(kit, "fiche", [("Dossier", "12 docs", "bars"), ("Contrat", "AV 2019", "shield"),
                             ("Objectif", "retraite", "cal")], pos=[390, 820], scale=0.9)
    S.add("tampon", "stamp", z=11.8, parent="fiche", text="OK", w=200, h=68, size=36)
    S.set("tampon", pos=[118, 196], rot=-8, scale=0, opacity=0)
    toi = K.Figure(kit, "toi", pos=[880, 955], show=False)

    def ticks(n):
        return [sheet.world(S, i, "tick", n=n) for i in range(3)]
    f = toi.enter(10)
    f = toi.walk(f + 2, toi.place_for(ticks(f), f))
    hit = toi.tap(f + 2, ticks(f)[0])
    hits = toi.trace(hit + 6, ticks(hit))
    a, b = (S.to_world("fiche", q, hits[-1]) for q in sheet.value_span(2))
    end = toi.strike(hits[-1] + 2, a, b, line="fiche_L3")
    h2 = toi.stamp(end + 12, "tampon", shake="fiche")
    last = toi.exit(toi.rest(h2 + 14) + 2)
    assert not kit.warnings, kit.warnings
    G = story.GEOM["FIGURE"]
    worst, frames = 0.0, 0
    for n in range(last + 1):
        s = S.world_scale("toi", n)
        if s < 0.05:
            continue
        lean = S.val("toi", "lean", n, 0)   # épaule calculée comme entities.tsx Limb (penché autour du pied)
        sh = K.rotate_about(G["shoulder"], lean, G["pivot"]) if lean else G["shoulder"]
        A, E, B = S.to_world("toi", sh, n), S.val("toi_bras", "elbow", n), S.val("toi_stylo", "pos", n)
        worst = max(worst, abs(math.dist(A, E) - G["arm"]["upper"] * s), abs(math.dist(E, B) - G["arm"]["fore"] * s))
        frames += 1
    assert worst < 0.01, f"écart de longueur {worst:.3f} px"
    assert math.dist(toi.tip(hit), ticks(hit)[0]) < 0.5, "pointe hors de la cible au contact"
    off = max(math.dist(toi.tip(n), t) for n, t in zip(hits, ticks(hits[0])))
    assert off < 0.5, f"relecture : pointe à {off:.2f} px des coches"
    return f"écart max {worst:.1e} px sur {frames} images (entrée, marche, tapotement, relecture, trait, tampon, sortie)"


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
