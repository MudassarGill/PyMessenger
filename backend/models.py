from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class User:
    """Represents a registered user in PyMessenger."""
    username: str
    display_name: str
    last_active: str = ""          # ISO timestamp of last heartbeat

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "display_name": self.display_name,
            "last_active": self.last_active,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        return cls(
            username=data["username"],
            display_name=data["display_name"],
            last_active=data.get("last_active", ""),
        )

    def is_online(self, threshold_seconds: int = 12) -> bool:
        """Return True if user sent a heartbeat within threshold_seconds."""
        if not self.last_active:
            return False
        try:
            last = datetime.fromisoformat(self.last_active)
            diff = (datetime.now() - last).total_seconds()
            return diff <= threshold_seconds
        except ValueError:
            return False

    def login(self, user_manager) -> bool:
        return user_manager.check_login(self.username)

    def logout(self):
        pass

    @classmethod
    def register(cls, username: str, display_name: str, user_manager) -> "User":
        user = cls(username=username.lower(), display_name=display_name)
        user_manager.add_user(user)
        return user


@dataclass
class Message:
    """Represents a single chat message in PyMessenger."""
    sender: str
    receiver: str
    text: str
    timestamp: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    seen: bool = False             # True when receiver has read the message

    def to_dict(self) -> dict:
        return {
            "from": self.sender,
            "to": self.receiver,
            "message": self.text,
            "timestamp": self.timestamp,
            "seen": self.seen,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Message":
        return cls(
            sender=data["from"],
            receiver=data["to"],
            text=data["message"],
            timestamp=data.get("timestamp", ""),
            seen=data.get("seen", False),
        )
