"""Upload d'une vidéo validée par le contrôle qualité sur Cloudinary (WTH-V2/videos/WTH-Vxx)."""
import argparse
import os
from datetime import datetime, timezone

from .common import OUTPUT, env, load_config, read_json, write_json

UPLOADS = OUTPUT / "uploads.json"


def upload(video_id):
    env("CLOUDINARY_URL")
    import cloudinary
    import cloudinary.uploader

    cfg = load_config()["cloudinary"]
    mp4 = OUTPUT / f"WTH-{video_id}.mp4"
    qa = OUTPUT / "qa" / f"{video_id}.json"
    if not qa.exists() or not read_json(qa)["ok"]:
        raise SystemExit(f"{video_id} : contrôle qualité absent ou en échec, upload refusé.")
    overwrite = os.environ.get("OVERWRITE") == "1"
    public_id = cfg["public_id_pattern"].format(id=video_id)
    res = cloudinary.uploader.upload_large(
        str(mp4), resource_type="video", public_id=public_id, asset_folder=cfg["folder"],
        display_name=public_id, use_filename=False, unique_filename=False, overwrite=overwrite,
        invalidate=overwrite)
    uploads = read_json(UPLOADS) if UPLOADS.exists() else {}
    uploads[video_id] = {
        "public_id": res["public_id"],
        "asset_id": res.get("asset_id"),
        "secure_url": res["secure_url"],
        "version": res.get("version"),
        "bytes": res.get("bytes"),
        "duration": res.get("duration"),
        "existing": res.get("existing", False),
        "uploaded_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    write_json(UPLOADS, uploads)
    note = " (déjà présent, non écrasé : OVERWRITE=1 pour remplacer)" if res.get("existing") else ""
    print(f"{video_id} -> {res['secure_url']}{note}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("id")
    upload(p.parse_args().id)


if __name__ == "__main__":
    main()
