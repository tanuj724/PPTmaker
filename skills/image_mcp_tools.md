# Image-Finding MCP Tools for PPTmaker

> **Purpose**: Eliminates custom scraping/download scripts by exposing dedicated Model Context Protocol (MCP) tools that let agents search, filter, and fetch royalty-free images directly into presentations.

---

## 1. Top Image MCP Servers (Tested & Active)

| Tool / Server | Source | API Key Required? | Best For |
|---|---|---|---|
| **`hellokaton/unsplash-mcp-server`** (Python) | Unsplash API | Yes (Free: 50 req/hr) | Modern, artistic, conceptual, business photography |
| **`drumnation/unsplash-smart-mcp-server`** (TS) | Unsplash API | Yes (Free) | Orientation filtering (landscape/portrait) + auto-attribution |
| **`CaullenOmdahl/pexels-mcp-server`** (TS) | Pexels API | Yes (Free: 200 req/hr) | Authentic people, workplace, technology, sports |
| **`garylab/pexels-mcp-server`** (Python) | Pexels API | Yes (Free) | Python-native Pexels search & direct image download |
| **`yanexr/wikimedia-image-search-mcp`** (TS) | Wikimedia Commons | **No** | History, military, geography, government, news |
| **`romulorasec/imagebank-mcp`** (TS) | Pexels + Unsplash + Pixabay | Yes (aggregates keys) | Multi-provider unified search with WebP optimization |

---

## 2. Recommended Configuration (`opencode.json`)

To enable seamless image retrieval inside PPTmaker, add any of these servers to your `opencode.json`:

```json
{
  "$schema": "https://opencode.ai/schema.json",
  "mcpServers": {
    "unsplash": {
      "command": "python",
      "args": ["-m", "unsplash_mcp_server"],
      "env": {
        "UNSPLASH_ACCESS_KEY": "${UNSPLASH_ACCESS_KEY}"
      }
    },
    "pexels": {
      "command": "npx",
      "args": ["-y", "pexels-mcp-server"],
      "env": {
        "PEXELS_API_KEY": "${PEXELS_API_KEY}"
      }
    },
    "wikimedia": {
      "command": "npx",
      "args": ["-y", "wikimedia-image-search-mcp"]
    }
  }
}
```

---

## 3. How Agents Use Image MCP Tools

### Workflow Integration
1. **Content Agent** outputs a `visual_suggestion` per slide:
   ```json
   {
     "slide_number": 4,
     "visual_query": "Indian Army tank battle exercise",
     "aspect_ratio": "landscape",
     "preferred_source": "wikimedia"
   }
   ```
2. **Theme / Builder Agent** invokes the MCP tool:
   - For historical/factual topics: `wikimedia.search_images(query="T-90 Bhishma tank", width=1200)`
   - For business/tech topics: `unsplash.search_photos(query="collaboration team", orientation="landscape")`
   - For lifestyle/work topics: `pexels.search_photos(query="software developer dark mode")`
3. Tool downloads image directly to `./assets/slide_{n}.jpg` and returns the file path + metadata (credit, alt-text).
4. **Builder Agent** embeds the image using python-pptx `slide.shapes.add_picture()`.

---

## 4. Why This Beats Custom Scripts

- **Zero Fragile Scraping**: Uses official JSON APIs with stable response formats.
- **No Rate-Limit Bans**: Respects platform headers, auth tokens, and backoff.
- **Automatic Metadata**: Captures photographer credits, license URLs, and captions.
- **One Tool for All Decks**: The same MCP command works across *any* topic — Climate Change, AI, History, Pitch Decks.
