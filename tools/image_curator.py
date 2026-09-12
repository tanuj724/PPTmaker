"""
PPTmaker - Multi-Source Image Curator & Asset Processor MCP Server
Handles automated searching, downloading, cropping, and color calibration of presentation assets.
"""
import io
import json
import os
import time
import urllib.parse
import urllib.request
from typing import Dict, List, Optional, Tuple

from PIL import Image, ImageEnhance
from mcp.server.mcpserver import MCPServer

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) PPTmaker/2.0 (image-curator@pptmaker.ai)"

mcp = MCPServer("image_curator")


class ImageCurator:
    def __init__(self, output_dir: str = "assets_curated"):
        self.out_dir = os.path.abspath(output_dir)
        os.makedirs(self.out_dir, exist_ok=True)

    def fetch_wikimedia_file(self, filename: str, target_size: Tuple[int, int] = (1200, 900)) -> Optional[bytes]:
        clean = filename.replace("File:", "").replace(" ", "_")
        urls = [
            f"https://commons.wikimedia.org/wiki/Special:FilePath/{urllib.parse.quote(clean)}?width={target_size[0]}",
            f"https://commons.wikimedia.org/wiki/Special:FilePath/{urllib.parse.quote(clean)}",
            f"https://commons.wikimedia.org/wiki/Special:Redirect/file/{urllib.parse.quote(clean)}",
        ]
        for url in urls:
            try:
                req = urllib.request.Request(
                    url,
                    headers={
                        "User-Agent": USER_AGENT,
                        "Referer": "https://commons.wikimedia.org/",
                        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
                    },
                )
                with urllib.request.urlopen(req, timeout=20) as resp:
                    data = resp.read()
                    if len(data) > 2048:
                        return data
            except Exception:
                continue
            time.sleep(1)
        return None

    def search_and_download(self, query: str, target_size: Tuple[int, int] = (1200, 900)) -> Optional[bytes]:
        api_url = (
            f"https://commons.wikimedia.org/w/api.php?action=query&generator=search"
            f"&gsrsearch={urllib.parse.quote(query)}&gsrnamespace=6&gsrlimit=6"
            f"&prop=imageinfo&iiprop=url|size|mime&format=json"
        )
        try:
            req = urllib.request.Request(api_url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                pages = data.get("query", {}).get("pages", {})
                for pid, pdata in pages.items():
                    title = pdata.get("title", "")
                    if any(title.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png"]):
                        raw = self.fetch_wikimedia_file(title, target_size)
                        if raw:
                            return raw
        except Exception:
            pass
        return None

    @staticmethod
    def cover_crop(img: Image.Image, target_size: Tuple[int, int]) -> Image.Image:
        tw, th = target_size
        iw, ih = img.size
        scale = max(tw / iw, th / ih)
        img = img.resize((int(iw * scale) + 1, int(ih * scale) + 1), Image.LANCZOS)
        nw, nh = img.size
        left = (nw - tw) // 2
        top = (nh - th) // 2
        return img.crop((left, top, left + tw, top + th))

    @staticmethod
    def apply_dark_overlay(img: Image.Image, factor: float = 0.48, tint: Tuple[int, int, int] = (14, 22, 38)) -> Image.Image:
        overlay = Image.new("RGB", img.size, tint)
        return Image.blend(img, overlay, factor)

    @staticmethod
    def polish_image(img: Image.Image) -> Image.Image:
        img = ImageEnhance.Color(img).enhance(1.08)
        img = ImageEnhance.Contrast(img).enhance(1.06)
        return img

    def curate_asset(
        self,
        slot_id: str,
        filename_or_query: str,
        target_size: Tuple[int, int] = (1200, 900),
        mode: str = "plain",
        darken_factor: float = 0.48,
        tint: Tuple[int, int, int] = (14, 22, 38),
    ) -> Optional[str]:
        dest_path = os.path.join(self.out_dir, f"{slot_id}.jpg")
        raw = self.fetch_wikimedia_file(filename_or_query, target_size)
        if not raw:
            raw = self.search_and_download(filename_or_query, target_size)
        if not raw:
            return None
        try:
            img = Image.open(io.BytesIO(raw)).convert("RGB")
            img = self.cover_crop(img, target_size)
            if mode == "dark":
                img = self.apply_dark_overlay(img, factor=darken_factor, tint=tint)
            img = self.polish_image(img)
            img.save(dest_path, "JPEG", quality=86, optimize=True)
            return dest_path
        except Exception:
            return None

    def batch_curate(self, asset_manifest: Dict[str, Tuple[str, Tuple[int, int], str]]) -> Dict[str, str]:
        results = {}
        for slot, (query_or_file, size, mode) in asset_manifest.items():
            path = self.curate_asset(slot, query_or_file, target_size=size, mode=mode)
            if path:
                results[slot] = path
            time.sleep(1.5)
        return results


_curator = ImageCurator()


@mcp.tool()
def curate_single_asset(
    slot_id: str,
    filename_or_query: str,
    width: int = 1200,
    height: int = 900,
    mode: str = "plain",
    darken_factor: float = 0.48,
) -> str:
    """Fetch, crop, and process a single image asset for a presentation slide.

    Args:
        slot_id: Unique identifier for the slide slot (e.g. 'title', 'slide_2_hero').
        filename_or_query: Wikimedia filename (e.g. 'File:Foo.jpg') or a search query.
        width: Target width in pixels.
        height: Target height in pixels.
        mode: 'plain' for normal, 'dark' for darkened hero overlay.
        darken_factor: Overlay darkness when mode='dark' (0.0-1.0).

    Returns:
        Path to the saved JPEG, or error message.
    """
    path = _curator.curate_asset(
        slot_id=slot_id,
        filename_or_query=filename_or_query,
        target_size=(width, height),
        mode=mode,
        darken_factor=darken_factor,
    )
    if path:
        return json.dumps({"status": "success", "path": path, "slot_id": slot_id})
    return json.dumps({"status": "error", "message": f"Failed to fetch/process image for slot '{slot_id}'"})


@mcp.tool()
def curate_batch_assets(
    manifest: str,
) -> str:
    """Process multiple image assets at once for a full presentation.

    Args:
        manifest: JSON string mapping slot_id -> {"query": str, "width": int, "height": int, "mode": str}.
                  Example: {"title": {"query": "File:Panorama.jpg", "width": 1920, "height": 1080, "mode": "dark"},
                            "slide_2": {"query": "mountain landscape", "width": 800, "height": 600, "mode": "plain"}}

    Returns:
        JSON with results per slot.
    """
    try:
        raw_manifest = json.loads(manifest)
    except json.JSONDecodeError:
        return json.dumps({"status": "error", "message": "Invalid JSON manifest"})

    parsed = {}
    for slot, info in raw_manifest.items():
        query = info.get("query", slot)
        width = info.get("width", 1200)
        height = info.get("height", 900)
        mode = info.get("mode", "plain")
        parsed[slot] = (query, (width, height), mode)

    results = _curator.batch_curate(parsed)
    return json.dumps({"status": "success", "results": results, "total": len(raw_manifest), "succeeded": len(results)})


@mcp.tool()
def search_wikimedia(
    query: str,
    limit: int = 6,
) -> str:
    """Search Wikimedia Commons for images matching a query. Returns titles and URLs without downloading.

    Args:
        query: Search terms for Wikimedia Commons.
        limit: Max number of results (1-20).

    Returns:
        JSON list of matching image results.
    """
    limit = max(1, min(limit, 20))
    api_url = (
        f"https://commons.wikimedia.org/w/api.php?action=query&generator=search"
        f"&gsrsearch={urllib.parse.quote(query)}&gsrnamespace=6&gsrlimit={limit}"
        f"&prop=imageinfo&iiprop=url|size|mime&format=json"
    )
    try:
        req = urllib.request.Request(api_url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            pages = data.get("query", {}).get("pages", {})
            results = []
            for pid, pdata in pages.items():
                title = pdata.get("title", "")
                info_list = pdata.get("imageinfo", [])
                for info in info_list:
                    if info.get("mime", "").startswith("image/"):
                        results.append({
                            "title": title,
                            "url": info.get("url", ""),
                            "width": info.get("width", 0),
                            "height": info.get("height", 0),
                            "mime": info.get("mime", ""),
                        })
            return json.dumps({"status": "success", "results": results, "count": len(results)})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


if __name__ == "__main__":
    mcp.run()
