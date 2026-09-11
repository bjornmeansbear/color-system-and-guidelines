#!/usr/bin/env python3
"""
Pull down images and metadata from an are.na channel.

- Image blocks  -> downloaded to images/       (chairs photographed/saved directly)
- Link blocks   -> preview image downloaded to links/, plus source metadata
                   (e.g. Vitra Design Museum collection pages, Unsplash, ECAL, etc.)
- Channel blocks (sub-channels connected into chair-ness) are listed but NOT
  recursed into -- some of them (like "sitting", 1847 blocks) belong to other
  people and are far bigger than this channel itself. Ask before pulling those.

Writes manifest.csv summarizing every block and where its file landed.

Usage:
    python3 fetch_arena.py --channel <slug> [--out .]
"""
import argparse
import csv
import json
import re
import time
import urllib.request
import urllib.error
from pathlib import Path

API_BASE = "https://api.are.na/v3"
USER_AGENT = "arena-archive-script/1.0 (personal are.na export)"


def plain_text(value):
    """are.na returns rich text as {markdown, html, plain}; older blocks as a str."""
    if isinstance(value, dict):
        return value.get("plain") or value.get("markdown") or ""
    return value or ""


def slugify(text, maxlen=60):
    text = (text or "").strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:maxlen] or "untitled"


def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)


def fetch_all_contents(channel_slug):
    blocks = []
    page = 1
    while True:
        url = f"{API_BASE}/channels/{channel_slug}/contents?per=100&page={page}"
        data = get_json(url)
        blocks.extend(data["data"])
        if not data["meta"]["has_more_pages"]:
            break
        page += 1
        time.sleep(0.2)
    return blocks


def download(url, dest_path):
    if dest_path.exists():
        return "skipped (exists)"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req) as resp, open(dest_path, "wb") as f:
            f.write(resp.read())
        return "downloaded"
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        return f"error: {e}"


def ext_from_url(url, fallback="jpg"):
    m = re.search(r"\.([a-zA-Z0-9]{2,5})(?:\?|$)", url)
    return m.group(1).lower() if m else fallback


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--channel", required=True,
                    help="are.na channel slug to pull")
    ap.add_argument("--out", default=".")
    args = ap.parse_args()

    out_dir = Path(args.out)
    images_dir = out_dir / "images"
    links_dir = out_dir / "links"
    images_dir.mkdir(parents=True, exist_ok=True)
    links_dir.mkdir(parents=True, exist_ok=True)

    print(f"Fetching contents of are.na/{args.channel} ...")
    blocks = fetch_all_contents(args.channel)
    print(f"Got {len(blocks)} blocks.")

    manifest_rows = []

    for b in blocks:
        btype = b["type"]
        bid = b["id"]
        title = b.get("title")
        source = b.get("source") or {}
        source_url = source.get("url", "")
        domain = re.sub(r"^www\.", "", re.sub(r"^https?://", "", source_url).split("/")[0]) if source_url else ""

        row = {
            "id": bid,
            "type": btype,
            "title": title or "",
            "description": plain_text(b.get("description")).strip(),
            "image_url": "",
            "image_url_large": "",
            "source_url": source_url,
            "domain": domain,
            "local_path": "",
            "status": "",
        }

        if btype == "Image":
            img = b.get("image") or {}
            src = img.get("src")
            if src:
                ext = ext_from_url(src, ext_from_url(img.get("filename", ""), "jpg"))
                fname = f"{bid}-{slugify(title or img.get('filename'))}.{ext}"
                dest = images_dir / fname
                status = download(src, dest)
                row["image_url"] = src
                # are.na also serves a resized variant through its image proxy.
                # The local archive keeps the original; a hotlinked page wants
                # this one -- measured at ~14% of the original's transfer size.
                row["image_url_large"] = (img.get("large") or {}).get("src") or src
                row["local_path"] = str(dest.relative_to(out_dir))
                row["status"] = status
            else:
                row["status"] = "no image src"

        elif btype == "Link":
            img = b.get("image")
            if img:
                # prefer large, fall back to top-level src
                src = (img.get("large") or {}).get("src") or img.get("src")
                if src:
                    ext = ext_from_url(src)
                    fname = f"{bid}-{slugify(title or domain)}.{ext}"
                    dest = links_dir / fname
                    status = download(src, dest)
                    row["image_url"] = src
                    row["image_url_large"] = src
                    row["local_path"] = str(dest.relative_to(out_dir))
                    row["status"] = status
                else:
                    row["status"] = "no preview image src"
            else:
                row["status"] = "no preview image"

        elif btype == "Channel":
            row["status"] = f"sub-channel, not recursed (counts: {b.get('counts')})"

        else:
            row["status"] = "skipped (no image for this block type)"

        manifest_rows.append(row)
        if row["status"] not in ("skipped (no image for this block type)",):
            print(f"[{btype:9s}] {bid} {row['status']:20s} {title or domain or ''}")

    manifest_path = out_dir / "manifest.csv"
    with open(manifest_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "type", "title", "description", "source_url", "domain",
                                    "image_url", "image_url_large", "local_path",
                                    "status"])
        writer.writeheader()
        writer.writerows(manifest_rows)

    print(f"\nWrote manifest to {manifest_path}")
    print(f"Images: {images_dir}  |  Link previews: {links_dir}")


if __name__ == "__main__":
    main()
