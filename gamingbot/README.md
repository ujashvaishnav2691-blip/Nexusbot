# NexusBot 🎮

**AI-powered customer service chatbot for gaming platforms and IT support.**

Built with FastAPI + Claude AI (Anthropic). Deployed on Railway. Private repository.

---

## Features

- 🎮 **Gaming support** — account issues, billing, game crashes, matchmaking, bans
- 💻 **IT support** — hardware, network, software, performance, security
- 🤖 **Powered by Claude AI** — natural, context-aware conversations
- 💬 **Multi-turn memory** — remembers conversation context
- ⚡ **Real-time responses** — typically under 2 seconds
- 🎨 **Gaming UI** — dark theme, typing indicators, category sidebar
- 📱 **Responsive** — works on mobile and desktop

## Tech Stack

- **Backend**: Python, FastAPI
- **AI**: Anthropic Claude (claude-sonnet)
- **Frontend**: Vanilla JS, HTML/CSS
- **Deployment**: Railway
- **Auth**: API key via environment variable

## Local Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env
uvicorn main:app --reload --port 8000
```

Open http://localhost:8000

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Chat UI |
| POST | `/chat` | Send message, get reply |
| GET | `/health` | Health check |
| GET | `/suggested-questions` | Get example questions |

## Author

**Ujash Vaishnav** — AI Engineer, London UK  
🔗 [LinkedIn](https://linkedin.com/in/ujash-vaishnav0311)
