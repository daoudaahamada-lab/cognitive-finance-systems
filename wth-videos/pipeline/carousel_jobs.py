"""Publication des carrousels V2 Pro : Drive -> Cloudinary -> Metricool.

Les appels passent par les connecteurs Cloudinary et Metricool (les API ne sont pas joignables
depuis la machine). Ce module prépare, pour chaque carrousel, la liste exacte des appels à faire
et fait le bilan de ce qui a été exécuté.

  python3 -m pipeline.carousel_jobs jobs      écrit data/jobs/WTH-XXX.json
  python3 -m pipeline.carousel_jobs status    bilan à partir de data/v2pro_state/WTH-XXX.json

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


def status():
    plan = read_json(DATA / "publication_plan.json")
    done, todo = [], []
    for entry in plan:
        path = STATE / f"{entry['id']}.json"
        state = read_json(path) if path.exists() else {}
        slides = sum(1 for u in state.get("cloudinary", []) if u.get("secure_url"))
        posts = [n for n in NETWORKS if state.get("posts", {}).get(n, {}).get("id")]
        line = f"{entry['id']} {entry['date']} {entry['heure']}  slides {slides}/9  posts {','.join(posts) or '-'}"
        (done if slides == 9 and len(posts) == 3 else todo).append(line)
    print(f"Terminés : {len(done)}/{len(plan)}")
    for line in todo:
        print("  à faire :", line)


if __name__ == "__main__":
    {"jobs": jobs, "status": status}[sys.argv[1] if len(sys.argv) > 1 else "status"]()
