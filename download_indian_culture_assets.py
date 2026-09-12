"""
PPTmaker - Visual Asset Curator for Indian Culture Deck
Downloads and polishes free-licensed high-resolution Wikimedia Commons cultural imagery.
"""
import io
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from PIL import Image, ImageEnhance

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) PPTmaker/2.0 (cultural-curator@pptmaker.ai)"
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets_indian_culture")
os.makedirs(OUT_DIR, exist_ok=True)

CANDIDATES = {
    "title": [
        "File:Varanasi Ghats Ganga Aarti.jpg",
        "File:Ganga Aarti at Dashashwamedh Ghat Varanasi.jpg",
        "File:Aarti at Varanasi.jpg",
        "File:Dashashwamedh Ghat Aarti Varanasi.jpg",
        "File:Taj Mahal in March 2004.jpg",
        "File:Humayun's Tomb, Delhi.jpg"
    ],
    "architecture": [
        "File:Kailasa temple, Ellora caves, Maharashtra, India.jpg",
        "File:Kailash Temple at Ellora.jpg",
        "File:Brihadisvara Temple in Thanjavur.jpg",
        "File:Sun Temple Konark.jpg",
        "File:Kailasa temple at Ellora caves.jpg"
    ],
    "quote_portrait": [
        "File:Swami Vivekananda 1893-09-oriented.jpg",
        "File:Swami Vivekananda in Chicago 1893.jpg",
        "File:Swami Vivekananda 1893.jpg",
        "File:Swami Vivekananda.jpg"
    ],
    "festivals": [
        "File:Diwali Lamps.jpg",
        "File:Diwali oil lamps.jpg",
        "File:Diya for Diwali.jpg",
        "File:Rangoli and Diyas.jpg",
        "File:Deepawali lamps.jpg",
        "File:Holi Festival of Colours India.jpg"
    ],
    "closing": [
        "File:Floating diyas in the Ganges river during Dev Deepawali in Varanasi.jpg",
        "File:Diyas floating on Ganga river in Varanasi.jpg",
        "File:Varanasi Ghats at sunrise.jpg",
        "File:Ganga Aarti, Dashashwamedh Ghat, Varanasi.jpg",
        "File:Sunset at the Taj Mahal.jpg"
    ]
}

TARGET_SIZES = {
    "title": (1920, 1080),
    "architecture": (880, 1060),
    "quote_portrait": (760, 960),
    "festivals": (880, 1060),
    "closing": (1920, 1080)
}

MODES = {
    "title": "dark",
    "architecture": "plain",
    "quote_portrait": "plain",
    "festivals": "plain",
    "closing": "dark"
}

def fetch_file(name, target_w=1600):
    clean = name.replace("File:", "").replace(" ", "_")
    urls = [
        f"https://commons.wikimedia.org/wiki/Special:FilePath/{urllib.parse.quote(clean)}?width={target_w}",
        f"https://commons.wikimedia.org/wiki/Special:FilePath/{urllib.parse.quote(clean)}",
        f"https://commons.wikimedia.org/wiki/Special:Redirect/file/{urllib.parse.quote(clean)}"
    ]
    for url in urls:
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": UA,
                    "Referer": "https://commons.wikimedia.org/",
                    "Accept": "image/*,*/*;q=0.8"
                }
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read()
                if len(data) > 3000:
                    return data
        except Exception:
            continue
    return None

def search_wikimedia(query, target_w=1600):
    api_url = (
        f"https://commons.wikimedia.org/w/api.php?action=query&generator=search"
        f"&gsrsearch={urllib.parse.quote(query)}&gsrnamespace=6&gsrlimit=6"
        f"&prop=imageinfo&iiprop=url|size|mime&format=json"
    )
    try:
        req = urllib.request.Request(api_url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            pages = data.get("query", {}).get("pages", {})
            for pid, pdata in pages.items():
                title = pdata.get("title", "")
                if any(title.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png"]):
                    raw = fetch_file(title, target_w)
                    if raw:
                        return raw, title
    except Exception as e:
        print(f"Search error for '{query}': {e}")
    return None, None

def cover_crop(img, target):
    tw, th = target
    iw, ih = img.size
    scale = max(tw / iw, th / ih)
    img = img.resize((int(iw * scale) + 1, int(ih * scale) + 1), Image.LANCZOS)
    nw, nh = img.size
    left = (nw - tw) // 2
    top = (nh - th) // 2
    return img.crop((left, top, left + tw, top + th))

def darken(img, factor=0.45, tint=(26, 40, 54)):
    overlay = Image.new("RGB", img.size, tint)
    return Image.blend(img, overlay, factor)

def polish(img):
    img = ImageEnhance.Color(img).enhance(1.08)
    img = ImageEnhance.Contrast(img).enhance(1.06)
    return img

def main():
    manifest = {}
    for slot, candidates in CANDIDATES.items():
        out_path = os.path.join(OUT_DIR, slot + ".jpg")
        size = TARGET_SIZES[slot]
        mode = MODES[slot]
        raw_data = None
        source_name = None

        print(f"Curating slot: {slot}...")
        for cand in candidates:
            raw_data = fetch_file(cand, target_w=size[0])
            if raw_data:
                source_name = cand
                print(f"  [OK] Found directly: {cand}")
                break
            time.sleep(0.5)

        if not raw_data:
            print(f"  [Searching fallback] for {slot}...")
            query_map = {
                "title": "Varanasi Ganga Aarti evening",
                "architecture": "Kailasa temple Ellora",
                "quote_portrait": "Swami Vivekananda 1893 Chicago",
                "festivals": "Diwali lamps diyas India",
                "closing": "Varanasi Dev Deepawali Ganges"
            }
            raw_data, source_name = search_wikimedia(query_map.get(slot, "India heritage culture"), target_w=size[0])

        if raw_data:
            try:
                img = Image.open(io.BytesIO(raw_data)).convert("RGB")
                img = cover_crop(img, size)
                if mode == "dark":
                    img = darken(img, factor=0.42 if slot == "title" else 0.50)
                img = polish(img)
                img.save(out_path, "JPEG", quality=85, optimize=True)
                manifest[slot] = {
                    "file": f"assets_indian_culture/{slot}.jpg",
                    "source": source_name,
                    "dimensions": f"{size[0]}x{size[1]}",
                    "mode": mode,
                    "status": "ready"
                }
                print(f"  [SUCCESS] Saved {slot}.jpg ({size[0]}x{size[1]})")
            except Exception as e:
                print(f"  [ERROR processing] {slot}: {e}")
        else:
            print(f"  [WARNING] Could not fetch asset for {slot}")
        time.sleep(1)

    with open(os.path.join("research_json", "image_manifest_indian_culture.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print("\nVisual asset curation complete!")

if __name__ == "__main__":
    main()
