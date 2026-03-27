# Build AI Apps with Python in Neovim

Student code for the **Build AI Apps with Python in Neovim** video series.

Each episode folder contains the complete code from that lesson.

## Episodes

| # | Topic | Code |
|---|-------|------|
| 1 | Your First AI API Call | [episode01](episode01/) |

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install anthropic python-dotenv
```

Create a `.env` file with your API key:

```
ANTHROPIC_API_KEY=your-api-key-here
```

## Series

32 episodes covering:
- AI API fundamentals (messages, streaming, vision)
- Tool use and function calling
- RAG (retrieval-augmented generation)
- AI agents
- Real-world patterns (classification, summarization, code review)
- Production apps (FastAPI, Docker)

Taught by [CelesteAI](https://www.youtube.com/@GoCelesteAI)
