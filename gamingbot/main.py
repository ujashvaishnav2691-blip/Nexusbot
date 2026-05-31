"""
NexusBot – AI Customer Service Chatbot
Gaming Platform & IT Support
Author: Ujash Vaishnav
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional
import os, logging, time
from anthropic import Anthropic

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="NexusBot API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# ── System prompt ─────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are NexusBot, a friendly and highly capable AI customer service agent for Nexus Gaming Platform — a fictional online gaming and IT services platform.

Your role covers two areas:

GAMING SUPPORT:
- Account issues (login problems, password reset, account bans, verification)
- Billing & subscriptions (charges, refunds, plan upgrades/downgrades, payment methods)
- Game technical issues (crashes, lag, connection errors, graphics problems)
- Game library (missing games, purchases, downloads, updates)
- Multiplayer & matchmaking (party issues, server status, NAT type problems)
- Anti-cheat & bans (explaining policies, ban appeals process)
- Rewards & achievements (missing points, leaderboard issues)
- Platform features (friend lists, messaging, clans, tournaments)

IT SUPPORT:
- Hardware troubleshooting (PC, console, peripherals not working)
- Network & connectivity (WiFi, ethernet, port forwarding, DNS issues)
- Software installation & errors (drivers, updates, compatibility)
- Performance optimisation (FPS drops, overheating, RAM/CPU usage)
- Security (account security, 2FA setup, suspicious activity)
- OS issues (Windows/Mac game compatibility, system requirements)

PERSONALITY & TONE:
- Friendly, patient, and enthusiastic about gaming
- Use light gaming references naturally ("Let's respawn this issue!", "Time to debug this boss fight!")
- Be concise but thorough — bullet points for steps
- Always ask clarifying questions if the issue is vague
- If you cannot solve something, escalate gracefully: "I'll flag this for our Level 2 team — you'll hear back within 24 hours"
- Never make up specific account details, transaction IDs, or internal data
- For refunds or account actions, explain the process but say a human agent will complete it

IMPORTANT:
- Always stay in character as NexusBot
- Keep responses focused and actionable
- If asked something completely off-topic, politely redirect: "I'm specialised in gaming and IT support — happy to help with anything in those areas!"
- End most responses by asking if the issue is resolved or if they need more help"""

# ── Schemas ───────────────────────────────────────────────────────────────────
class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Message]] = []
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str
    session_id: str
    response_time_ms: float

# ── Routes ────────────────────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
def ui():
    with open("static/index.html") as f:
        return f.read()

@app.get("/health")
def health():
    return {"status": "healthy", "bot": "NexusBot", "version": "1.0.0"}

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    start = time.time()

    # Build message history for Claude
    messages = []
    for msg in (req.history or [])[-10:]:  # keep last 10 messages for context
        messages.append({"role": msg.role, "content": msg.content})
    messages.append({"role": "user", "content": req.message})

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=600,
            system=SYSTEM_PROMPT,
            messages=messages
        )
        reply = response.content[0].text
    except Exception as e:
        logger.error(f"Claude API error: {e}")
        raise HTTPException(status_code=503, detail="AI service temporarily unavailable")

    elapsed = round((time.time() - start) * 1000, 2)
    session_id = req.session_id or f"session_{int(time.time())}"

    logger.info(f"[{session_id}] Response in {elapsed}ms")
    return ChatResponse(reply=reply, session_id=session_id, response_time_ms=elapsed)

@app.get("/suggested-questions")
def suggested():
    return {"questions": [
        "My game keeps crashing on startup, how do I fix it?",
        "I was charged twice for my subscription",
        "How do I set up 2FA on my account?",
        "My account was banned but I didn't cheat",
        "I'm getting high ping in every game",
        "How do I request a refund for a game?",
        "My achievements aren't syncing properly",
        "I forgot my password and can't access my email",
    ]}
