import sys
from pathlib import Path

# Make sure `backend` package can be imported when running from project root
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from backend.models import User
from backend.user_manager import UserManager, UserAlreadyExistsError
from backend.message_manager import MessageManager
from backend.logger_manager import LoggerManager

app = FastAPI(title="PyMessenger API", version="1.0.0")

# ── Managers ─────────────────────────────────────────────────────────────────
user_mgr = UserManager()
msg_mgr = MessageManager()
logger = LoggerManager()

# ── Mount frontend static files ───────────────────────────────────────────────
FRONTEND_DIR = Path(__file__).parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


# ── Pydantic request schemas ──────────────────────────────────────────────────
class RegisterRequest(BaseModel):
    username: str
    display_name: str


class LoginRequest(BaseModel):
    username: str


class SendMessageRequest(BaseModel):
    sender: str
    receiver: str
    text: str


# ── Static page routes ─────────────────────────────────────────────────────────
@app.get("/", response_class=FileResponse)
def serve_login():
    return FileResponse(str(FRONTEND_DIR / "index.html"))


@app.get("/chat", response_class=FileResponse)
def serve_chat():
    return FileResponse(str(FRONTEND_DIR / "chat.html"))


# ── API Endpoints ──────────────────────────────────────────────────────────────

@app.post("/register")
def register(req: RegisterRequest):
    """Register a new user."""
    try:
        username = req.username.strip().lower()
        display_name = req.display_name.strip()
        if not username or not display_name:
            raise HTTPException(status_code=400, detail="Username and display name are required.")
        user = User(username=username, display_name=display_name)
        user_mgr.add_user(user)
        return {"success": True, "message": f"User '{display_name}' registered successfully!"}
    except UserAlreadyExistsError:
        raise HTTPException(status_code=409, detail=f"Username '{req.username}' is already taken.")
    except Exception as e:
        logger.log_error("register", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/login")
def login(req: LoginRequest):
    """Login an existing user."""
    try:
        username = req.username.strip().lower()
        user = user_mgr.check_login(username)
        if not user:
            raise HTTPException(status_code=401, detail="Username not found. Please register first.")
        return {
            "success": True,
            "username": user.username,
            "display_name": user.display_name,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.log_error("login", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/send_message")
def send_message(req: SendMessageRequest):
    """Send a message from one user to another."""
    try:
        sender = req.sender.strip().lower()
        receiver = req.receiver.strip().lower()
        text = req.text.strip()
        if not text:
            raise HTTPException(status_code=400, detail="Message text cannot be empty.")
        # Validate both users exist
        if not user_mgr.get_user(sender):
            raise HTTPException(status_code=404, detail=f"Sender '{sender}' not found.")
        if not user_mgr.get_user(receiver):
            raise HTTPException(status_code=404, detail=f"Receiver '{receiver}' not found.")
        msg = msg_mgr.send_message(sender, receiver, text)
        return {
            "success": True,
            "message": msg.to_dict(),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.log_error("send_message", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get_messages")
def get_messages(user1: str, user2: str):
    """Get all messages between two users."""
    try:
        messages = msg_mgr.get_messages(user1, user2)
        return {"success": True, "messages": [m.to_dict() for m in messages]}
    except Exception as e:
        logger.log_error("get_messages", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users")
def get_users():
    """Get list of all registered users."""
    try:
        users = user_mgr.get_all_users()
        return {"success": True, "users": [u.to_dict() for u in users]}
    except Exception as e:
        logger.log_error("get_users", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/conversations")
def get_conversations(user: str):
    """Get all users that a given user has exchanged messages with."""
    try:
        contacts = msg_mgr.get_conversations(user)
        result = []
        for c in contacts:
            u = user_mgr.get_user(c)
            if u:
                result.append(u.to_dict())
        return {"success": True, "contacts": result}
    except Exception as e:
        logger.log_error("get_conversations", e)
        raise HTTPException(status_code=500, detail=str(e))


# ── New: Heartbeat / Online Status / Seen Receipts ────────────────────────────

class HeartbeatRequest(BaseModel):
    username: str


class MarkSeenRequest(BaseModel):
    sender: str    # who sent the messages
    receiver: str  # who is now reading them


@app.post("/heartbeat")
def heartbeat(req: HeartbeatRequest):
    """
    Called by the frontend every ~5 s while the user is active.
    Stamps last_active on the user record so others can tell they're online.
    """
    try:
        found = user_mgr.update_heartbeat(req.username.strip().lower())
        if not found:
            raise HTTPException(status_code=404, detail="User not found.")
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        logger.log_error("heartbeat", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/online_users")
def online_users():
    """
    Returns all users whose last heartbeat was within the last 12 seconds.
    Frontend uses this to show Online/Offline badge next to each user.
    """
    try:
        online = user_mgr.get_online_users(threshold_seconds=12)
        return {
            "success": True,
            "online_users": [u.username for u in online],
        }
    except Exception as e:
        logger.log_error("online_users", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/mark_seen")
def mark_seen(req: MarkSeenRequest):
    """
    Mark all messages from `sender` → `receiver` as seen=True.
    Called when the receiver opens the conversation with the sender.
    """
    try:
        count = msg_mgr.mark_seen(
            sender=req.sender.strip().lower(),
            receiver=req.receiver.strip().lower(),
        )
        return {"success": True, "marked": count}
    except Exception as e:
        logger.log_error("mark_seen", e)
        raise HTTPException(status_code=500, detail=str(e))

