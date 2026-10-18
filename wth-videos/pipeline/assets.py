"""Télécharge depuis Cloudinary les PNG de carrousel V2 (WTH-V2-XXX-NN) dans assets/WTH-XXX/."""
import argparse

import requests

from .common import ASSETS, env, load_config, videos


def fetch(source):
    env("CLOUDINARY_URL")
    import cloudinary
    import cloudinary.search

    num = source.split("-")[1]
    prefix = load_config()["cloudinary"]["slides_public_id_pattern"].format(num=num)
    res = cloudinary.search.Search().expression(f"public_id:{prefix}*").max_results(50).execute()
    target = ASSETS / source
    count = 0
    for r in sorted(res.get("resources", []), key=lambda x: x["public_id"]):
        if r.get("format") != "png":
            continue
        nn = r["public_id"].rsplit("-", 1)[-1]
        dest = target / f"{source}-{nn}.png"
        if dest.exists():
            count += 1
            continue
        target.mkdir(parents=True, exist_ok=True)
        data = requests.get(r["secure_url"], timeout=60)
        data.raise_for_status()
        dest.write_bytes(data.content)
        count += 1
    print(f"{source} : {count} PNG dans {target}" if count else f"{source} : aucun PNG V2 sur Cloudinary (fond crème)")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("ids", nargs="*", help="Vxx ; vide = toutes les vidéos")
    args = p.parse_args()
    table = videos()
    for vid in args.ids or list(table):
        fetch(table[vid]["source"])


if __name__ == "__main__":
    main()
