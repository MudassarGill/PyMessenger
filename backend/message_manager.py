import json
from pathlib import Path
from typing import List
from backend.models import Message
from backend.logger_manager import LoggerManager

STORAGE_DIR = Path(__file__).parent / "storage"
MESSAGES_FILE = STORAGE_DIR / "messages.json"

logger = LoggerManager()


class MessageManager:
    """Manages all message operations with file-based persistence."""

    def __init__(self):
        STORAGE_DIR.mkdir(parents=True, exist_ok=True)
        if not MESSAGES_FILE.exists():
            MESSAGES_FILE.write_text("[]", encoding="utf-8")

    def _read_messages(self) -> List[dict]:
        try:
            with open(MESSAGES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write_messages(self, messages: List[dict]):
        with open(MESSAGES_FILE, "w", encoding="utf-8") as f:
            json.dump(messages, f, indent=2, ensure_ascii=False)

    def send_message(self, sender: str, receiver: str, text: str) -> Message:
        """Create a new message and persist it to messages.json."""
        messages = self._read_messages()
        msg = Message(sender=sender.lower(), receiver=receiver.lower(), text=text)
        messages.append(msg.to_dict())
        self._write_messages(messages)
        logger.log_message_sent(sender, receiver)
        return msg

    def get_messages(self, user1: str, user2: str) -> List[Message]:
        """Retrieve all messages exchanged between user1 and user2 (both directions)."""
        user1 = user1.lower()
        user2 = user2.lower()
        all_msgs = self._read_messages()
        filtered = [
            Message.from_dict(m)
            for m in all_msgs
            if (m["from"] == user1 and m["to"] == user2)
            or (m["from"] == user2 and m["to"] == user1)
        ]
        return sorted(filtered, key=lambda m: m.timestamp)

    def get_all_messages(self, user: str) -> List[Message]:
        """Retrieve all messages where the given user is sender or receiver."""
        user = user.lower()
        all_msgs = self._read_messages()
        filtered = [
            Message.from_dict(m)
            for m in all_msgs
            if m["from"] == user or m["to"] == user
        ]
        return sorted(filtered, key=lambda m: m.timestamp)

    def get_conversations(self, user: str) -> List[str]:
        """Returns a list of unique usernames that the given user has talked to."""
        user = user.lower()
        all_msgs = self._read_messages()
        contacts = set()
        for m in all_msgs:
            if m["from"] == user:
                contacts.add(m["to"])
            elif m["to"] == user:
                contacts.add(m["from"])
        return list(contacts)

    def mark_seen(self, sender: str, receiver: str) -> int:
        """
        Mark all messages sent by `sender` to `receiver` as seen=True.
        Called when `receiver` opens the chat with `sender`.
        Returns the number of messages marked.
        """
        sender   = sender.lower()
        receiver = receiver.lower()
        messages = self._read_messages()
        count = 0
        for m in messages:
            if m["from"] == sender and m["to"] == receiver and not m.get("seen", False):
                m["seen"] = True
                count += 1
        if count:
            self._write_messages(messages)
        return count

