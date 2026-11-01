"""output/planning_videos.csv : id, date, heure, URL Cloudinary, légende, hashtags."""
import csv
from datetime import date

from .common import OUTPUT, load_config, load_scripts, read_json
from .upload import UPLOADS


def planning():
    heure = load_config()["planning"]["heure"]
    uploads = read_json(UPLOADS) if UPLOADS.exists() else {}
    path = OUTPUT / "planning_videos.csv"
    missing = []
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "date", "heure", "url_cloudinary", "legende", "hashtags"])
        for vid, s in sorted(load_scripts().items()):
            url = uploads.get(vid, {}).get("secure_url", "")
            if not url:
                missing.append(vid)
            w.writerow([f"WTH-{vid}", date.fromisoformat(s["date"]).strftime("%d/%m/%Y"), heure, url, s["legende"],
                        " ".join(s["hashtags"])])
    print(f"{path} écrit" + (f" ; sans URL : {', '.join(missing)}" if missing else ""))


if __name__ == "__main__":
    planning()
