# PPTmaker - Agentic Presentation Generator

## Step 0: Project Setup & Dependencies

### 1. Create and Activate Virtual Environment (Windows)

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` and add your Gemini API key.

### 4. Run the Project

```bash
python main.py
```