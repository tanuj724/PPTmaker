"""
PPTmaker - curated image downloader (v3)
Downloads hand-picked, free-licensed Wikimedia Commons images for the deck.
"""
import io
import os
import time
import urllib.parse
import urllib.request

from PIL import Image, ImageEnhance

UA = "PPTmaker/1.0 (educational presentation generator; contact: user@example.com)"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(OUT, exist_ok=True)

FILES = {
    "title": ("File:Indian Army contingent Republic Day parade 2023 Img1.jpg", (1920, 760), "dark"),
    "overview": ("File:Garhwal Rifles Contingent at the 76th Republic Day Parade (2024).jpg", (880, 1060), "plain"),
    "history": ("File:Indian cavalry, Western Front, during World War I. This is one of a number of photographs "
                "showing the Indian cavalry who fought with the Allies. In the autumn of 1914, the urgent need "
                "for trained (4687922433).jpg", (880, 1060), "plain"),
    "wars": ("File:Main Battle Tank of the Indian Army, T-90 Bhishma passes through the Rajpath, at the 72nd "
             "Republic Day Celebrations, in New Delhi on January 26, 2021.jpg", (880, 1060), "plain"),
    "structure": ("File:Indian Army Armoured Corps.jpg", (880, 1060), "plain"),
    "ethos": ("File:Admiral RK Dhowan reviewing the Passing Out Parade at the Indian Military Academy, "
              "Dehradun 01.JPG", (880, 1060), "plain"),
    "operations": ("File:HAL Dhruv and Pinaka Army day.jpg", (880, 1060), "plain"),
    "relief": ("File:Army flood relief and rescue operations, in Chennai on November 17, 2015 (3).jpg", (880, 1060), "plain"),
    "modern": ("File:The Women Officers contingent passes through the Rajpath during the 66th Republic Day "
               "Parade 2015, in New Delhi on January 26, 2015.jpg", (880, 1060), "plain"),
    "honour": ("File:INDIA GATE NEW DELHI.jpg", (880, 1060), "plain"),
    "closing": ("File:Helicopters flying in formation over the Rajpath while carrying the tricolour and flags "
                "of three services during the full dress rehearsal for the Republic Day Parade - 2006, in New "
                "Delhi on January 23,2006 (1).jpg", (1920, 760), "dark"),
}


def fetch(name, retries=4):
    clean = name.replace("File:", "")
    urls = [
        "https://commons.wikimedia.org/wiki/Special:FilePath/" + urllib.parse.quote(clean) + "?width=1600&height=2200",
        "https://commons.wikimedia.org/wiki/Special:FilePath/" + urllib.parse.quote(clean),
        "https://commons.wikimedia.org/wiki/Special:Redirect/file/" + urllib.parse.quote(clean),
    ]
    for attempt in range(retries):
        for url in urls:
            try:
                req = urllib.request.Request(
                    url, headers={"User-Agent": UA, "Referer": "https://commons.wikimedia.org/"}
                )
                with urllib.request.urlopen(req, timeout=120) as resp:
                    return resp.read()
            except Exception as e:
                last = e
        time.sleep(5)
    raise last


def cover_crop(img, target):
    tw, th = target
    iw, ih = img.size
    scale = max(tw / iw, th / ih)
    img = img.resize((int(iw * scale) + 1, int(ih * scale) + 1), Image.LANCZOS)
    nw, nh = img.size
    img = img.crop(((nw - tw) // 2, (nh - th) // 2, (nw - tw) // 2 + tw, (nh - th) // 2 + th))
    return img


def darken(img, factor=0.45, warm=(10, 24, 16)):
    overlay = Image.new("RGB", img.size, warm)
    return Image.blend(img, overlay, factor)


def polish(img):
    img = ImageEnhance.Color(img).enhance(1.07)
    img = ImageEnhance.Contrast(img).enhance(1.05)
    return img


def main():
    for slot, (fname, size, mode) in FILES.items():
        path = os.path.join(OUT, slot + ".jpg")
        try:
            raw = fetch(fname)
            img = Image.open(io.BytesIO(raw)).convert("RGB")
            img = cover_crop(img, size)
            if mode == "dark":
                img = darken(img, factor=0.40 if slot == "title" else 0.50)
            img = polish(img)
            img.save(path, "JPEG", quality=82, optimize=True)
            print("OK   {:10s} <- {}".format(slot, fname[:60]))
        except Exception as e:
            print("FAIL {:10s} -> {}".format(slot, e))
        time.sleep(4)
    print("DONE")


if __name__ == "__main__":
    main()