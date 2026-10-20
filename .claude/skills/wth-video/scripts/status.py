#!/usr/bin/env python3
"""Suivi de production des vidéos WTH : wth-videos/scripts/production_status.json (versionné).

Le fichier dit, pour chaque vidéo, où en est chaque étape ; il est commité pour qu'une nouvelle session reprenne là où
la précédente s'est arrêtée. Schéma : .claude/skills/wth-video/references/status-schema.md.

    python3 .claude/skills/wth-video/scripts/status.py init                  crée le fichier / ajoute les vidéos manquantes
    python3 .claude/skills/wth-video/scripts/status.py show [V07 ...] [--json]
    python3 .claude/skills/wth-video/scripts/status.py next [V07 ...] [--json]    prochaine étape de chaque vidéo
    python3 .claude/skills/wth-video/scripts/status.py set V07 storyboard done [--note "…"] [--pending "…"]
                                                         [--issue "…"] [cle=valeur ...]
    python3 .claude/skills/wth-video/scripts/status.py merge V07 - <<'EOF'      résultat d'un workflow (JSON)
    {"spec": "done", "render": "done", "review": "fixed", "qa": "done", "open_issues": []}
    EOF
    python3 .claude/skills/wth-video/scripts/status.py checkpoint v01_full_approved done [--note "…"]
    python3 .claude/skills/wth-video/scripts/status.py issues V07 --clear

Les écritures prennent le verrou wth-videos/build/.status.lock (deux workflows peuvent écrire en même temps).
Code 1 sur une erreur d'usage (étape, état ou vidéo inconnus).
"""
import argparse
import fcntl
import json
import os
import re
import sys
import tempfile
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

STAGES = ["voice", "storyboard", "spec", "render", "review", "mute_verify", "qa", "delivered", "published"]
STAGE_FR = {"voice": "voix", "storyboard": "storyboard", "spec": "mise en scène", "render": "rendu",
            "review": "revues", "mute_verify": "contrôle sans son", "qa": "QA", "delivered": "livrée",
            "published": "publiée"}
STATES = ["pending", "in_progress", "partial", "done", "fixed", "open", "fail", "blocked", "skipped"]
# États qui laissent passer à l'étape suivante (« open » : majeurs consignés et signalés, on ne boucle pas).
PASSED = {"done", "fixed", "open", "skipped"}
SHORT = {"pending": ".", "in_progress": "cours", "partial": "part.", "done": "ok", "fixed": "corr.",
         "open": "ouvert", "fail": "ÉCHEC", "blocked": "bloqué", "skipped": "sauté"}
ACTION = {
    "voice": "recette voix : references/voice-elevenlabs-mcp.md (vérifier les crédits d'abord)",
    "storyboard": "skill wth-storyboard : storyboard.wf.js (revise.wf.js si un storyboard existe déjà)",
    "spec": "skill wth-story-build : build-review.wf.js",
    "render": "skill wth-story-build : build-review.wf.js (make story ID={id})",
    "review": "skill wth-story-build : build-review.wf.js avec from: \"review\"",
    "mute_verify": "skill wth-story-build : mute-verify.wf.js",
    "qa": "make qa ID={id} (references/qa-checklist.md de wth-story-build)",
    "delivered": "SendUserFile output/WTH-{id}.mp4 + légende et hashtags",
    "published": "references/publishing.md (dates validées par l'utilisateur d'abord)",
}
CHECKPOINTS = {
    "v01_full_approved": "V01 complète validée par l'utilisateur (avant la série V02-V15)",
    "publication_dates_approved": "dates de publication validées (avant toute programmation Metricool)",
    "elevenlabs_credits": "crédits ElevenLabs suffisants pour le prochain lot de voix",
    "publication_questions": "licence Remotion et déclaration « contenu IA » tranchées (avant publication)",
}
VID = re.compile(r"^V\d{2,3}$")
CP_NAME = re.compile(r"^[a-z0-9_]+$")


def default_root():
    # .claude/skills/wth-video/scripts/status.py -> racine du dépôt -> wth-videos
    return Path(__file__).resolve().parents[4] / "wth-videos"


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def die(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)


class Store:
    def __init__(self, root):
        self.root = Path(root)
        self.path = self.root / "scripts" / "production_status.json"
        self.lock_path = self.root / "build" / ".status.lock"

    @contextmanager
    def locked(self):
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.lock_path, "a") as fh:
            fcntl.flock(fh, fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(fh, fcntl.LOCK_UN)

    def load(self, must_exist=True):
        if not self.path.exists():
            if must_exist:
                die(f"{self.path} absent : lance d'abord « status.py init ».")
            return {"version": 1, "updated_at": None, "checkpoints": {}, "notes": [], "videos": {}}
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            die(f"{self.path} illisible ({e}) : corrige le JSON à la main (git diff aide).")
        validate(data)
        return data

    def save(self, data):
        data["updated_at"] = now()
        validate(data)
        text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
        fd, tmp = tempfile.mkstemp(dir=self.path.parent, prefix=".production_status.", suffix=".tmp")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp, self.path)


def validate(data):
    for vid, v in data.get("videos", {}).items():
        for stage, st in v.get("stages", {}).items():
            if stage not in STAGES:
                die(f"{vid} : étape inconnue « {stage} » dans le fichier de suivi (étapes : {', '.join(STAGES)})")
            if st.get("state") not in STATES:
                die(f"{vid} {stage} : état inconnu « {st.get('state')} » (états : {', '.join(STATES)})")
    for name, cp in data.get("checkpoints", {}).items():
        if cp.get("state") not in STATES:
            die(f"point de validation {name} : état inconnu « {cp.get('state')} »")


def scripts_index(root):
    p = Path(root) / "scripts" / "scripts.json"
    if not p.exists():
        return {}
    return {s["id"]: s for s in json.loads(p.read_text(encoding="utf-8"))}


def max_durations(root):
    try:
        import yaml
        cfg = yaml.safe_load((Path(root) / "config.yaml").read_text(encoding="utf-8"))
        return (cfg.get("qa") or {}).get("max_duration_by_video") or {}
    except Exception:  # noqa: BLE001 - simple information d'affichage
        return {}


def new_video(script):
    return {"title": script.get("titre", ""), "source": script.get("source", ""), "date_initiale": script.get("date", ""),
            "stages": {s: {"state": "pending"} for s in STAGES}, "open_issues": [], "notes": []}


def video(data, vid, create=False, root=None):
    if not VID.match(vid):
        die(f"identifiant de vidéo invalide : {vid} (attendu : V07)")
    vids = data.setdefault("videos", {})
    if vid not in vids:
        if not create:
            die(f"{vid} absente du suivi : « status.py init » l'ajoute si elle est dans scripts/scripts.json.")
        s = scripts_index(root).get(vid)
        if not s:
            die(f"{vid} absente de scripts/scripts.json : écris d'abord son script (SKILL.md, « Nouvelle vidéo »).")
        vids[vid] = new_video(s)
    v = vids[vid]
    for s in STAGES:
        v.setdefault("stages", {}).setdefault(s, {"state": "pending"})
    return v


def parse_value(raw):
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw


def set_stage(v, stage, state, note=None, pending=None, extras=None):
    if stage not in STAGES:
        die(f"étape inconnue « {stage} » (étapes : {', '.join(STAGES)})")
    if state not in STATES:
        die(f"état inconnu « {state} » (états : {', '.join(STATES)})")
    st = v["stages"].setdefault(stage, {})
    st["state"] = state
    st["updated_at"] = now()
    if note is not None:
        if note:
            st["note"] = note
        else:
            st.pop("note", None)
    if pending is not None:
        if pending:
            st["pending"] = pending
        else:
            st.pop("pending", None)
    elif state in ("done", "skipped"):
        # Une étape déclarée terminée sans nouveau « reste à faire » n'en a plus (sa note reste).
        st.pop("pending", None)
    for k, val in (extras or {}).items():
        if k in ("state", "updated_at"):
            die(f"« {k} » est réservé")
        if val is None:
            st.pop(k, None)
        else:
            st[k] = val
    return st


def next_stage(v):
    for s in STAGES:
        st = v["stages"].get(s, {"state": "pending"})
        if st["state"] not in PASSED or st.get("pending"):
            return s, st
    return None, None


def selected(data, ids):
    vids = data.get("videos", {})
    if not ids:
        return sorted(vids, key=lambda x: int(x[1:]))
    missing = [i for i in ids if i not in vids]
    if missing:
        die(f"absentes du suivi : {', '.join(missing)} (status.py init)")
    return ids


# ---------- commandes ----------

def cmd_init(store, args):
    with store.locked():
        data = store.load(must_exist=False)
        scripts = scripts_index(store.root)
        if not scripts:
            die(f"{store.root}/scripts/scripts.json introuvable ou vide")
        maxd = max_durations(store.root)
        added = []
        for vid in sorted(scripts, key=lambda x: int(x[1:])):
            if vid not in data["videos"]:
                data["videos"][vid] = new_video(scripts[vid])
                added.append(vid)
            v = data["videos"][vid]
            for s in STAGES:
                v["stages"].setdefault(s, {"state": "pending"})
            if vid in maxd and "max_duration_s" not in v:
                v["max_duration_s"] = maxd[vid]
        for name, label in CHECKPOINTS.items():
            data["checkpoints"].setdefault(name, {"state": "pending", "label": label})
        store.save(data)
    print(f"{store.path} : {len(data['videos'])} vidéo(s)" + (f", ajoutées : {', '.join(added)}" if added else
                                                              ", rien à ajouter"))


def cmd_show(store, args):
    data = store.load()
    ids = selected(data, args.ids)
    if args.json:
        out = dict(data)
        out["videos"] = {i: data["videos"][i] for i in ids}
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return
    print(f"Suivi : {store.path.relative_to(store.root.parent)} (mis à jour {data.get('updated_at') or '—'})")
    cps = data.get("checkpoints", {})
    if cps:
        print("Points de validation :")
        for name, cp in cps.items():
            note = f" — {cp['note']}" if cp.get("note") else ""
            print(f"  {name:28} {cp['state']}{note}")
    for n in data.get("notes", []):
        print(f"  note : {n}")
    heads = ["voix", "story", "spec", "rendu", "revue", "muet", "qa", "livré", "publié"]
    print("\n      " + "".join(f"{h:8}" for h in heads))
    for vid in ids:
        v = data["videos"][vid]
        cells = []
        for s in STAGES:
            st = v["stages"].get(s, {"state": "pending"})
            cells.append(f"{SHORT[st['state']] + ('*' if st.get('pending') else ''):8}")
        print(f"{vid:6}" + "".join(cells) + (v.get("title", "")[:38]))
    print("\n(* : reste à faire sur une étape commencée ; ok/corr./ouvert/sauté laissent passer à l'étape suivante)")
    for vid in ids:
        v = data["videos"][vid]
        lines = []
        for s in STAGES:
            st = v["stages"].get(s, {})
            bits = [st[k] for k in ("note", "pending") if st.get(k)]
            extra = {k: val for k, val in st.items() if k not in ("state", "updated_at", "note", "pending")}
            if extra:
                bits.append(", ".join(f"{k}={val}" for k, val in extra.items()))
            if bits:
                lines.append(f"  {STAGE_FR[s]} : " + " ; ".join(
                    ("À FAIRE : " + b) if b == st.get("pending") else str(b) for b in bits))
        if v.get("max_duration_s"):
            lines.append(f"  durée maximale approuvée : {v['max_duration_s']} s")
        for issue in v.get("open_issues", []):
            lines.append(f"  problème ouvert : {issue}")
        for n in v.get("notes", []):
            lines.append(f"  note : {n}")
        if lines and (args.ids or len(ids) <= 3 or args.details):
            print(f"\n{vid} — {v.get('title', '')}")
            print("\n".join(lines))
        else:
            todo = [f"{STAGE_FR[s]} : {v['stages'][s]['pending']}" for s in STAGES if v["stages"].get(s, {}).get("pending")]
            todo += [f"problème ouvert : {i}" for i in v.get("open_issues", [])]
            for t in todo:
                print(f"{vid} À FAIRE — {t[:150]}{'…' if len(t) > 150 else ''}")
    if not (args.ids or len(ids) <= 3 or args.details):
        print("\nDétail d'une vidéo : status.py show V07 (notes, prise, versions) ; toutes : status.py show --details")


def cmd_next(store, args):
    data = store.load()
    ids = selected(data, args.ids)
    v01_ok = data.get("checkpoints", {}).get("v01_full_approved", {}).get("state") == "done"
    out = []
    for vid in ids:
        s, st = next_stage(data["videos"][vid])
        action = ACTION[s].format(id=vid) if s else "rien : vidéo publiée"
        if s == "storyboard" and st["state"] in PASSED:
            action = "skill wth-storyboard : revise.wf.js (le storyboard existe ; notes = ce qui reste à faire)"
        item = {"id": vid, "stage": s, "state": st["state"] if st else None,
                "pending": st.get("pending") if st else None, "action": action}
        if s and vid != "V01" and not v01_ok and STAGES.index(s) >= STAGES.index("storyboard"):
            item["waiting"] = "attend la validation de V01 complète par l'utilisateur (point de validation v01_full_approved)"
        out.append(item)
    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return
    for it in out:
        if not it["stage"]:
            print(f"{it['id']} : terminée")
            continue
        extra = f" — reste : {it['pending']}" if it["pending"] else ""
        wait = f"\n      ⏸ {it['waiting']}" if it.get("waiting") else ""
        print(f"{it['id']} : {STAGE_FR[it['stage']]} ({it['state']}){extra}\n      → {it['action']}{wait}")


def cmd_set(store, args):
    extras = {}
    for kv in args.kv:
        if "=" not in kv:
            die(f"argument « {kv} » : attendu cle=valeur")
        k, raw = kv.split("=", 1)
        extras[k.strip()] = parse_value(raw)
    with store.locked():
        data = store.load()
        v = video(data, args.id, create=True, root=store.root)
        st = set_stage(v, args.stage, args.state, args.note, args.pending, extras)
        if args.issue:
            v.setdefault("open_issues", []).append(args.issue)
        store.save(data)
    print(f"{args.id} {args.stage} = {st['state']}" + (f" ({st['note']})" if st.get("note") else ""))


def cmd_merge(store, args):
    raw = sys.stdin.read() if args.source == "-" else Path(args.source).read_text(encoding="utf-8")
    try:
        update = json.loads(raw)
    except json.JSONDecodeError as e:
        die(f"JSON invalide : {e}")
    if not isinstance(update, dict):
        die("attendu un objet JSON")
    stages = dict(update.get("stages") or {})
    stages.update({k: val for k, val in update.items() if k in STAGES})
    unknown = [k for k in update if k not in STAGES and k not in ("stages", "open_issues", "notes", "max_duration_s")]
    if unknown:
        die(f"clés inconnues : {', '.join(unknown)} (étapes : {', '.join(STAGES)} ; open_issues, notes, max_duration_s)")
    with store.locked():
        data = store.load()
        v = video(data, args.id, create=True, root=store.root)
        changed = []
        for stage, val in stages.items():
            if isinstance(val, str):
                set_stage(v, stage, val)
            elif isinstance(val, dict) and val.get("state"):
                extras = {k: x for k, x in val.items() if k not in ("state", "note", "pending", "updated_at")}
                set_stage(v, stage, val["state"], val.get("note"), val.get("pending"), extras)
            else:
                die(f"{stage} : attendu un état (\"done\") ou un objet {{\"state\": …}}")
            changed.append(f"{stage}={v['stages'][stage]['state']}")
        if "open_issues" in update:
            v["open_issues"] = [str(x) for x in (update["open_issues"] or [])]
            changed.append(f"open_issues={len(v['open_issues'])}")
        for n in update.get("notes") or []:
            v.setdefault("notes", []).append(str(n))
        if "max_duration_s" in update:
            v["max_duration_s"] = update["max_duration_s"]
        store.save(data)
    print(f"{args.id} : " + (", ".join(changed) or "rien à changer"))


def cmd_checkpoint(store, args):
    if not CP_NAME.match(args.name):
        die("nom de point de validation : minuscules, chiffres et _ seulement")
    if args.state not in STATES:
        die(f"état inconnu « {args.state} » (états : {', '.join(STATES)})")
    with store.locked():
        data = store.load()
        cp = data.setdefault("checkpoints", {}).setdefault(args.name, {"label": CHECKPOINTS.get(args.name, "")})
        cp["state"] = args.state
        cp["updated_at"] = now()
        if args.note is not None:
            cp["note"] = args.note
        store.save(data)
    print(f"point de validation {args.name} = {args.state}")


def cmd_issues(store, args):
    with store.locked():
        data = store.load()
        v = video(data, args.id)
        if args.clear:
            v["open_issues"] = []
        if args.add:
            v.setdefault("open_issues", []).append(args.add)
        store.save(data)
        issues = v.get("open_issues", [])
    print(f"{args.id} : {len(issues)} problème(s) ouvert(s)" + "".join(f"\n  - {i}" for i in issues))


def main():
    p = argparse.ArgumentParser(description="Suivi de production WTH (scripts/production_status.json)")
    p.add_argument("--root", default=str(default_root()), help="dossier wth-videos (défaut : celui du dépôt)")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init")
    s = sub.add_parser("show")
    s.add_argument("ids", nargs="*")
    s.add_argument("--json", action="store_true")
    s.add_argument("--details", action="store_true", help="détail de chaque vidéo même sans filtre")
    s = sub.add_parser("next")
    s.add_argument("ids", nargs="*")
    s.add_argument("--json", action="store_true")
    s = sub.add_parser("set")
    s.add_argument("id")
    s.add_argument("stage", choices=STAGES)
    s.add_argument("state", choices=STATES)
    s.add_argument("kv", nargs="*", help="détails cle=valeur (valeur JSON si possible : duration_s=57.7)")
    s.add_argument("--note")
    s.add_argument("--pending", help="ce qui reste à faire sur cette étape ('' pour effacer)")
    s.add_argument("--issue", help="ajoute un problème ouvert à la vidéo")
    s = sub.add_parser("merge")
    s.add_argument("id")
    s.add_argument("source", help="fichier JSON, ou - pour l'entrée standard")
    s = sub.add_parser("checkpoint")
    s.add_argument("name")
    s.add_argument("state", choices=STATES)
    s.add_argument("--note")
    s = sub.add_parser("issues")
    s.add_argument("id")
    s.add_argument("--clear", action="store_true")
    s.add_argument("--add")
    args = p.parse_args()
    store = Store(args.root)
    {"init": cmd_init, "show": cmd_show, "next": cmd_next, "set": cmd_set, "merge": cmd_merge,
     "checkpoint": cmd_checkpoint, "issues": cmd_issues}[args.cmd](store, args)


if __name__ == "__main__":
    main()
