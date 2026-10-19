"""Publication des carrousels V2 Pro : Drive -> Cloudinary -> Metricool.

Les appels passent par les connecteurs Cloudinary et Metricool (les API ne sont pas joignables
depuis la machine). Ce module prépare, pour chaque carrousel, la liste exacte des appels à faire
et fait le bilan de ce qui a été exécuté.

  python3 -m pipeline.carousel_jobs jobs      écrit data/jobs/WTH-XXX.json
  python3 -m pipeline.carousel_jobs show WTH-004              appels à faire, prêts à copier
  python3 -m pipeline.carousel_jobs record WTH-004 slide 01 URL existing
  python3 -m pipeline.carousel_jobs record WTH-004 post tiktok update|create ID UUID
  python3 -m pipeline.carousel_jobs record WTH-004 error "message"
  python3 -m pipeline.carousel_jobs status    bilan à partir de data/v2pro_state/WTH-XXX.json
  python3 -m pipeline.carousel_jobs verify    compare au calendrier relu (data/metricool_verification.jsonl)

Entrées : data/publication_plan.json (date, heure, texte), data/metricool_actions.json
(post V1 à remplacer ou post à créer, par réseau), data/drive_v2pro_files.json (id Drive des
slides 01 à 09).
"""
import json
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

from .common import ROOT, read_json, write_json

DATA = ROOT / "data"
JOBS = DATA / "jobs"
STATE = DATA / "v2pro_state"
BLOG_ID = "6791889"
TZ = "Europe/Paris"
CLOUD = "byfnwwcw"
NETWORKS = ("tiktok", "instagram", "facebook")


def public_id(carousel, num):
    return f"WTH-V2-Pro-{carousel.split('-')[1]}-{num}"


def media_url(carousel, num):
    # URL sans version : sert toujours la version courante de l'asset.
    return f"https://res.cloudinary.com/{CLOUD}/image/upload/{public_id(carousel, num)}.png"


def network_data(network, plan):
    if network == "tiktok":
        return {"tiktokData": {"privacyOption": "PUBLIC_TO_EVERYONE", "title": plan["accroche"],
                               "autoAddMusic": True, "photoCoverIndex": 0}}
    if network == "instagram":
        return {"instagramData": {"type": "POST", "showReelOnFeed": True, "isAiGenerated": False}}
    return {"facebookData": {"type": "POST"}}


def post_info(network, plan, media):
    info = {
        "autoPublish": True,
        "draft": False,
        "descendants": [],
        "firstCommentText": "",
        "hasNotReadNotes": False,
        "providers": [{"network": network}],
        "publicationDate": {"dateTime": f"{plan['date']}T{plan['heure']}:00", "timezone": TZ},
        "shortener": False,
        "smartLinkData": {"ids": []},
        "text": plan["texte"],
        "media": media,
        "mediaAltText": [],
    }
    info.update(network_data(network, plan))
    return json.dumps(info, ensure_ascii=False)


def iso_date(plan):
    local = datetime.fromisoformat(f"{plan['date']}T{plan['heure']}:00").replace(tzinfo=ZoneInfo(TZ))
    return local.isoformat()


def build_job(carousel, plan, actions, drive):
    nums = sorted(drive["files"])
    if nums != [f"{i:02d}" for i in range(1, 10)]:
        raise SystemExit(f"{carousel} : slides Drive incomplètes {nums}")
    uploads = [{
        "resource_type": "image",
        "upload_request": {
            "file": f"https://drive.google.com/uc?export=download&id={drive['files'][n]}",
            "public_id": public_id(carousel, n),
            "asset_folder": f"WTH-V2/{carousel}",
            "display_name": public_id(carousel, n),
            "overwrite": False,
            "tags": ["WTH-V2-Pro", carousel],
        },
    } for n in nums]
    media = [media_url(carousel, n) for n in nums]
    posts = []
    for net in NETWORKS:
        (act,) = [a for a in actions if a["network"] == net]
        info = post_info(net, plan, media)
        if act["op"] == "update":
            posts.append({"network": net, "tool": "updateScheduledPost", "remplace": act["remplace"],
                          "args": {"blogId": BLOG_ID, "id": act["id"], "uuid": act["uuid"], "info": info}})
        else:
            posts.append({"network": net, "tool": "createScheduledPost",
                          "args": {"blogId": BLOG_ID, "date": iso_date(plan), "info": info}})
    return {"carrousel": carousel, "date": plan["date"], "heure": plan["heure"],
            "uploads": uploads, "media": media, "posts": posts}


def jobs():
    plan = {e["id"]: e for e in read_json(DATA / "publication_plan.json")}
    actions = read_json(DATA / "metricool_actions.json")
    drive = read_json(DATA / "drive_v2pro_files.json")
    missing = sorted(set(plan) - set(drive))
    if missing:
        raise SystemExit(f"Slides Drive introuvables : {', '.join(missing)}")
    JOBS.mkdir(exist_ok=True)
    for carousel, entry in plan.items():
        acts = [a for a in actions if a["carrousel"] == carousel]
        write_json(JOBS / f"{carousel}.json", build_job(carousel, entry, acts, drive[carousel]))
    print(f"{len(plan)} jobs écrits dans {JOBS.relative_to(ROOT)}")


def show(carousel):
    job = read_json(JOBS / f"{carousel}.json")
    print(f"{carousel} — {job['date']} {job['heure']}")
    print("UPLOADS (mcp__Cloudinary__upload-asset, resource_type image, upload_request :)")
    for u in job["uploads"]:
        print(json.dumps(u["upload_request"], ensure_ascii=False))
    for post in job["posts"]:
        args = post["args"]
        print(f"\nPOST {post['network']} : {post['tool']}")
        for key in ("blogId", "id", "uuid", "date"):
            if key in args:
                print(f"{key}: {args[key]}")
        print("info: " + args["info"])


def record(carousel, kind, *values):
    path = STATE / f"{carousel}.json"
    state = read_json(path) if path.exists() else {"carrousel": carousel, "cloudinary": [], "posts": {}}
    if kind == "slide":
        num, url, existing = values
        pid = public_id(carousel, num)
        state["cloudinary"] = [u for u in state["cloudinary"] if u["public_id"] != pid]
        state["cloudinary"].append({"public_id": pid, "secure_url": url, "existing": existing == "true"})
        state["cloudinary"].sort(key=lambda u: u["public_id"])
    elif kind == "post":
        network, op, post_id, uuid = values
        state["posts"][network] = {
            "op": op, "id": post_id, "uuid": uuid, "draft": False, "autoPublish": True, "media": 9,
            "plannerUrl": f"https://app.metricool.com/planner/calendar?blogId={BLOG_ID}&openWithPostUuid={uuid}"}
    elif kind == "error":
        state.setdefault("errors", []).append(" ".join(values))
    else:
        raise SystemExit(f"type inconnu : {kind}")
    STATE.mkdir(exist_ok=True)
    write_json(path, state)


def status():
    plan = read_json(DATA / "publication_plan.json")
    done, todo = [], []
    for entry in plan:
        path = STATE / f"{entry['id']}.json"
        state = read_json(path) if path.exists() else {}
        slides = sum(1 for u in state.get("cloudinary", []) if u.get("secure_url"))
        posts = [n for n in NETWORKS if state.get("posts", {}).get(n, {}).get("id")]
        line = f"{entry['id']} {entry['date']} {entry['heure']}  slides {slides}/9  posts {','.join(posts) or '-'}"
        if state.get("errors"):
            line += "  ERREURS : " + " | ".join(state["errors"])
        (done if slides == 9 and len(posts) == 3 else todo).append(line)
    print(f"Terminés : {len(done)}/{len(plan)}")
    for line in todo:
        print("  à faire :", line)


def verify(listing="data/metricool_verification.jsonl"):
    """Compare le calendrier relu dans Metricool (une ligne JSON par post) aux posts attendus."""
    expected = {}
    for entry in read_json(DATA / "publication_plan.json"):
        state = read_json(STATE / f"{entry['id']}.json")
        for net, post in state["posts"].items():
            expected[post["uuid"]] = (entry["id"], f"{entry['date']}T{entry['heure']}:00", net,
                                      entry["texte"].split("\n", 1)[0])
    seen, problems, others = set(), [], []
    for line in (ROOT / listing).read_text(encoding="utf-8").splitlines():
        post = json.loads(line)
        exp = expected.get(post["uuid"])
        if exp is None:
            others.append(post)
            continue
        carousel, when, net, first = exp
        seen.add(post["uuid"])
        checks = {"date": post["dateTime"] == when, "réseau": post["network"] == net,
                  "brouillon": post["draft"] is False, "auto": post["autoPublish"] is True,
                  "9 slides": post["media"] == 9, "png": post["ext"] == "png",
                  "texte": first.startswith(post["first"].rstrip("…").strip()[:40])}
        bad = [k for k, ok in checks.items() if not ok]
        if bad:
            problems.append(f"{carousel} {net} {post['dateTime']} : {', '.join(bad)}")
    missing = [f"{c} {n} {w}" for u, (c, w, n, _) in expected.items() if u not in seen]
    print(f"Attendus : {len(expected)}  retrouvés : {len(seen)}  autres posts : {len(others)}")
    for label, items in (("écarts", problems), ("absents", missing)):
        for item in items:
            print(f"  {label} : {item}")
    for post in others:
        print(f"  autre : {post['dateTime']} {post['network']} draft={post['draft']} « {post['first']} »")


if __name__ == "__main__":
    command, *args = sys.argv[1:] or ["status"]
    {"jobs": jobs, "show": show, "record": record, "status": status, "verify": verify}[command](*args)
