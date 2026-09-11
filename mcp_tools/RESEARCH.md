# MCP Tools & Servers Research for PPTmaker

## Overview
This document catalogs free/open-source MCP (Model Context Protocol) servers and tools that can enhance the PPTmaker framework with additional capabilities.

---

## 1. Web Search & Research Tools

### MCP Server: Brave Search
- **Purpose**: Real-time web search for research agent
- **Features**: 
  - Privacy-focused search results
  - News, web, and location search
  - No API key required for basic usage
- **Integration**: Connect to Research Agent for fact-gathering
- **Setup**: `mcp-server-brave-search`
- **URL**: https://github.com/modelcontextprotocol/servers/tree/main/src/brave-search

### MCP Server: Fetch
- **Purpose**: Web page content extraction
- **Features**:
  - Convert URLs to clean markdown/text
  - Extract main content, ignore navigation/ads
  - Support for paywalled content (limited)
- **Integration**: Research Agent can fetch full articles from search results
- **Setup**: `mcp-server-fetch`
- **URL**: https://github.com/modelcontextprotocol/servers/tree/main/src/fetch

### MCP Server: Google Search (via SerpAPI free tier)
- **Purpose**: Comprehensive web search
- **Features**: 100 free searches/month
- **Integration**: Alternative to Brave for broader coverage
- **Note**: Requires free API key registration

---

## 2. File System & Data Tools

### MCP Server: Filesystem
- **Purpose**: Read/write files on local system
- **Features**:
  - Safe file operations within designated directories
  - Read configs, templates, saved presentations
  - Write generated content before final export
- **Integration**: All agents can use for reading templates/saving drafts
- **Setup**: `mcp-server-filesystem`
- **URL**: https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem

### MCP Server: SQLite
- **Purpose**: Local database for caching and history
- **Features**:
  - Store presentation metadata
  - Cache research results
  - Track user preferences and templates
- **Integration**: Orchestrator for workflow state management
- **Setup**: `mcp-server-sqlite`

---

## 3. Visual & Design Assets

### MCP Server: Unsplash (via API)
- **Purpose**: Free high-quality stock images
- **Features**:
  - Search images by keyword
  - Download attribution-free images
  - 50 requests/hour on free tier
- **Integration**: Theme Agent for visual recommendations
- **Note**: Requires free API key
- **URL**: https://unsplash.com/developers

### MCP Server: IconFinder (free tier)
- **Purpose**: Icons for presentations
- **Features**: Limited free icons with attribution
- **Integration**: Theme Agent for slide graphics
- **Alternative**: Use built-in python-pptx shapes (no API needed)

---

## 4. Data Visualization

### MCP Server: Chart.js via Puppeteer
- **Purpose**: Generate chart images
- **Features**:
  - Create bar, line, pie charts programmatically
  - Export as PNG/SVG for embedding
- **Integration**: Builder Agent for data slides
- **Setup**: Custom implementation or use python-pptx native charts

### Native Alternative: python-pptx Charts
- **Built-in**: python-pptx supports charts natively
- **Types**: Bar, column, line, pie, scatter, area
- **Recommendation**: Use native charts instead of external MCP for simplicity

---

## 5. Content Enhancement

### MCP Server: Grammar Checker (LanguageTool)
- **Purpose**: Grammar and spell checking
- **Features**:
  - Free tier: 10k characters/request
  - Multi-language support
  - Style suggestions
- **Integration**: Content Agent for quality assurance
- **URL**: https://languagetool.org/http-api/

### MCP Server: Wikipedia
- **Purpose**: Quick factual lookups
- **Features**:
  - Free, no API key required
  - Summaries, full articles, images
- **Integration**: Research Agent for background information
- **Setup**: `mcp-server-wikipedia` (community implementations)

---

## 6. Developer & Utility Tools

### MCP Server: Git
- **Purpose**: Version control for generated presentations
- **Features**: Track changes, branch for variations
- **Integration**: Optional, for advanced users
- **Setup**: `mcp-server-git`

### MCP Server: Time
- **Purpose**: Timestamp and scheduling
- **Features**: Current time, timezone conversion
- **Integration**: Orchestrator for timeline tracking
- **Setup**: `mcp-server-time`

### MCP Server: Memory
- **Purpose**: Persistent conversation memory
- **Features**: Store user preferences across sessions
- **Integration**: Remember brand colors, preferred styles
- **Setup**: `mcp-server-memory`

---

## Recommended Core Stack for PPTmaker

### Essential (Free, No API Key):
1. **Filesystem MCP** - File operations
2. **SQLite MCP** - State management
3. **Time MCP** - Timestamps
4. **python-pptx native** - Charts and shapes

### Highly Recommended (Free with API Key):
1. **Brave Search MCP** - Research capabilities
2. **Fetch MCP** - Content extraction
3. **Unsplash API** - Stock images
4. **LanguageTool** - Grammar checking

### Optional Enhancements:
1. **Memory MCP** - User preference persistence
2. **Git MCP** - Version control
3. **Wikipedia MCP** - Quick facts

---

## Integration Strategy

### Phase 1: Core Functionality
- Use built-in python-pptx for all PowerPoint operations
- Implement basic Research Agent with prompt-based knowledge
- No external MCP dependencies initially

### Phase 2: Enhanced Research
- Add Brave Search MCP for real-time data
- Integrate Fetch MCP for deep-dive content
- Enable Wikipedia MCP for factual verification

### Phase 3: Visual Enhancement
- Connect Unsplash for image suggestions
- Implement LanguageTool for content polish
- Add Memory MCP for personalization

### Phase 4: Advanced Features
- SQLite for presentation history
- Git for version tracking
- Custom chart generation pipeline

---

## Configuration Example (opencode.json)

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/workspace/output"]
    },
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "${BRAVE_API_KEY}"
      }
    },
    "fetch": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-fetch"]
    },
    "time": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-time"]
    }
  }
}
```

---

## Cost Summary

| Tool | Free Tier | Paid Upgrade |
|------|-----------|--------------|
| Brave Search | 2000 req/month | $0.001/search after |
| Unsplash | 50 req/hour | Higher limits |
| LanguageTool | 10k chars/req | Premium features |
| python-pptx | Unlimited | N/A (open source) |
| Filesystem MCP | Unlimited | N/A (local) |
| SQLite MCP | Unlimited | N/A (local) |

**Total Cost**: $0 for basic usage, optional upgrades for heavy usage

---

## Next Steps

1. Start with core python-pptx functionality (no MCP)
2. Add filesystem and time MCP servers (zero config)
3. Optionally integrate Brave Search for enhanced research
4. Test each integration thoroughly before production
5. Document MCP setup in README for end users
