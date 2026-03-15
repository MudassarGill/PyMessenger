import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from backend.models import User
from backend.logger_manager import LoggerManager

STORAGE_DIR = Path(__file__).parent / "storage"
USERS_FILE = STORAGE_DIR / "users.json"

logger = LoggerManager()


class UserAlreadyExistsError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class UserManager:
    """Manages all user-related operations with file-based persistence."""

    def __init__(self):
        STORAGE_DIR.mkdir(parents=True, exist_ok=True)
        if not USERS_FILE.exists():
            USERS_FILE.write_text("[]", encoding="utf-8")

    def _read_users(self) -> List[dict]:
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write_users(self, users: List[dict]):
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=2, ensure_ascii=False)

    def get_all_users(self) -> List[User]:
        """Returns a list of all registered User objects."""
        return [User.from_dict(u) for u in self._read_users()]

    def add_user(self, user: User) -> User:
        """Save a new user to users.json. Raises if username already exists."""
        users = self._read_users()
        if any(u["username"] == user.username for u in users):
            raise UserAlreadyExistsError(f"Username '{user.username}' already exists.")
        users.append(user.to_dict())
        self._write_users(users)
        logger.log_register(user.username)
        return user

    def check_login(self, username: str) -> Optional[User]:
        """Validate user login. Returns User object if found, else None."""
        users = self._read_users()
        for u in users:
            if u["username"] == username.lower():
                logger.log_login(username)
                return User.from_dict(u)
        return None

    def get_user(self, username: str) -> Optional[User]:
        """Retrieve a specific user by username."""
        users = self._read_users()
        for u in users:
            if u["username"] == username.lower():
                return User.from_dict(u)
        return None

    def update_heartbeat(self, username: str) -> bool:
        """Stamp current timestamp as last_active for the given user."""
        users = self._read_users()
        found = False
        for u in users:
            if u["username"] == username.lower():
                u["last_active"] = datetime.now().isoformat()
                found = True
                break
        if found:
            self._write_users(users)
        return found

    def get_online_users(self, threshold_seconds: int = 12) -> List[User]:
        """Returns list of users who sent a heartbeat within threshold_seconds."""
        return [u for u in self.get_all_users() if u.is_online(threshold_seconds)]

