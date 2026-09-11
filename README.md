# 🤖 PPTmaker - Agentic Presentation Generator

An autonomous, multi-agent framework built on **Opencode** and **OmniRoute** that transforms a simple topic into a professional PowerPoint presentation. 

## 🚀 How It Works

Instead of writing code manually, you simply provide a **topic** to Opencode. The framework's specialized agents (orchestrated by skills defined in `/skills`) automatically:
1. **Research** the topic using web tools/MCP servers.
2. **Generate** structured, engaging slide content.
3. **Design** a cohesive theme and layout strategy.
4. **Build** the final `.pptx` file using `python-pptx`.

## 📂 Project Structure

```text
ppt-maker/
├── .env                  # Your API Keys (Create this!)
├── .env.example          # Template for API Keys
├── requirements.txt      # Python dependencies
├── config.py             # Configuration loader
├── opencode.json         # Opencode model routing config
├── README.md             # This file
├── OPENING_PROMPT.md     # The prompt to paste into Opencode
│
├── skills/               # Agent Instructions (The "Brain")
│   ├── orchestrator_agent.md
│   ├── research_agent.md
│   ├── content_agent.md
│   ├── theme_agent.md
│   └── builder_agent.md
│
└── mcp_tools/            # Tool Documentation
    └── RESEARCH.md       # Available free MCP servers & tools
```

## ⚙️ Setup Instructions

### 1. Prerequisites
- Python 3.9+ installed
- Git installed
- **Opencode CLI** installed and configured with **OmniRoute**
- A valid **Google Gemini API Key** (Get it from [Google AI Studio](https://aistudio.google.com/app/apikey))

### 2. Clone & Enter Directory
```bash
cd ppt-maker
```

### 3. Create Virtual Environment
**Windows:**
```cmd
python -m venv .venv
.venv\Scripts\activate
```
**Mac/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Create a `.env` file in the root directory and add your API key:
```bash
# Copy the example
copy .env.example .env   # Windows
cp .env.example .env     # Mac/Linux

# Edit .env and paste your key
GEMINI_API_KEY=your_actual_api_key_here
```

### 6. Verify Opencode Configuration
Ensure your `opencode.json` is present. It is pre-configured to route tasks to specific models via OmniRoute for optimal performance (Reasoning for planning, Chat for content, Code for building).

## 🎯 How to Run

You do **not** run a python script directly. You interact via the **Opencode CLI**.

1. **Activate your virtual environment** (if not already active).
2. **Start Opencode** in the project directory:
   ```bash
   opencode .
   ```
3. **Paste the Opening Prompt**:
   - Open the file `OPENING_PROMPT.md` in this directory.
   - Copy its **entire contents**.
   - Paste it into the Opencode chat interface.
4. **Provide Your Topic**:
   - Once the framework acknowledges the prompt, simply type:
     > "Create a presentation about [Your Topic Here]"
   - *Example:* "Create a presentation about The Future of Artificial Intelligence"

## 🛠️ Available Tools & MCP Servers

This framework is designed to leverage **MCP (Model Context Protocol)** servers for enhanced capabilities. See `mcp_tools/RESEARCH.md` for the full list of integrated free tools, including:
- **Web Search**: Brave Search, Fetch, Wikipedia
- **Visuals**: Unsplash (for stock images)
- **Utilities**: Filesystem, Time, Memory

*Note: Ensure your Opencode/OmniRoute setup has access to these MCP servers if you want the Research Agent to perform live lookups.*

## 🤖 Agent Roles

| Agent | Skill File | Responsibility |
| :--- | :--- | :--- |
| **Orchestrator** | `skills/orchestrator_agent.md` | Manages workflow, delegates tasks, ensures quality. |
| **Researcher** | `skills/research_agent.md` | Gathers facts, finds stats, validates info via MCP. |
| **Content** | `skills/content_agent.md` | Writes slide titles, bullet points, and speaker notes. |
| **Theme** | `skills/theme_agent.md` | Defines color palettes, fonts, and visual style. |
| **Builder** | `skills/builder_agent.md` | Writes & executes Python code to generate the `.pptx`. |

## 📝 License
MIT License - Feel free to modify and distribute.
