<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=32&pause=1000&color=6C63FF&center=true&vCenter=true&width=600&lines=💬+PyMessenger;WhatsApp-style+Messenger;Built+with+FastAPI+%26+Vanilla+JS" alt="PyMessenger Typing SVG" />

<br/>

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6%2B-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![HTML5](https://img.shields.io/badge/HTML5-CSS3-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

<br/>

> **PyMessenger** is a full-stack, WhatsApp-inspired local messaging application built with **Python FastAPI** on the backend and **Vanilla HTML/CSS/JS** on the frontend. It features real-time online/offline status, WhatsApp-style read receipts, file-based data persistence, and a stunning dark-mode UI — all without a database.

<br/>

[🚀 Quick Start](#-quick-start) &nbsp;•&nbsp;
[✨ Features](#-features) &nbsp;•&nbsp;
[📁 Structure](#-project-structure) &nbsp;•&nbsp;
[📡 API](#-api-reference) &nbsp;•&nbsp;
[🧠 Concepts](#-concepts-used) &nbsp;•&nbsp;
[👨‍💻 Author](#-author)

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 💬 Messaging
- Send & receive messages in real-time
- Auto-refresh every **3 seconds**
- Timestamps on every message
- Date dividers (Today / Yesterday)
- Scrollable chat history

</td>
<td width="50%">

### 🟢 Online Status
- Live **green dot** = online
- **Gray dot** = offline
- Powered by heartbeat pings every 5s
- Updates in sidebar & chat header

</td>
</tr>
<tr>
<td width="50%">

### ✅ Read Receipts
| Tick | Meaning |
|------|---------|
| `✓` gray | Sent — receiver offline |
| `✓✓` gray | Delivered — online, not read |
| `✓✓` 🟢 | **Seen** — receiver read it |

</td>
<td width="50%">

### 🎨 Modern Dark UI
- WhatsApp-inspired dark theme
- Gradient chat bubbles
- Glassmorphism effects
- Smooth micro-animations
- Fully responsive design

</td>
</tr>
</table>

**More highlights:**
- 🔐 Username-based registration & login
- 🗂️ **No database** — pure JSON file storage
- 📜 Full logging to `logs/app.log`
- 🛡️ Custom error handling & exceptions
- 📖 Auto-generated Swagger API docs

---

## 📁 Project Structure

```
PyMessenger/
│
├── 📂 backend/
│   ├── 🐍 main.py              ← FastAPI app + all REST endpoints
│   ├── 🐍 models.py            ← User & Message dataclasses
│   ├── 🐍 user_manager.py      ← Register, login, heartbeat, online status
│   ├── 🐍 message_manager.py   ← Send, fetch, mark_seen messages
│   ├── 🐍 logger_manager.py    ← Singleton logger (file + console)
│   └── 📂 storage/
│       ├── 📄 users.json       ← All registered users
│       └── 📄 messages.json    ← All messages with seen status
│
├── 📂 frontend/
│   ├── 🌐 index.html           ← Login / Register page
│   ├── 🌐 chat.html            ← Chat interface
│   ├── 🎨 style.css            ← Dark-mode UI, ticks, online dots
│   └── ⚡ app.js               ← Fetch API, heartbeat, DOM rendering
│
├── 📂 logs/
│   └── 📄 app.log              ← Auto-generated activity log
│
├── 📄 requirements.txt
└── 📄 README.md
```

---

## 🚀 Quick Start

### Prerequisites
- Python **3.10+**
- pip

### 1️⃣ Clone the repository

```bash
git clone https://github.com/MudassarGill/PyMessenger.git
cd PyMessenger
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Start the server

```bash
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

### 4️⃣ Open in browser

```
http://127.0.0.1:8000
```

> 💡 **Tip:** To test the full experience, open the app in **two browser tabs** — register two different users and chat between them!

---

## 📡 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/register` | Register a new user |
| `POST` | `/login` | Login with username |
| `POST` | `/send_message` | Send a message to a user |
| `GET`  | `/get_messages` | Get messages between two users |
| `GET`  | `/users` | Get all registered users |
| `GET`  | `/conversations` | Get all contacts of a user |
| `POST` | `/heartbeat` | Mark user as online (every 5s) |
| `GET`  | `/online_users` | Get list of currently online users |
| `POST` | `/mark_seen` | Mark messages as read |

> 📖 **Live Swagger Docs** → [`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs)

---

## 🔄 App Flow

```
┌─────────────────────────────────────────────────────────────┐
│                        PyMessenger Flow                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Browser Opens                                             │
│       │                                                     │
│       ▼                                                     │
│   Register / Login  ──►  POST /register  or  POST /login   │
│       │                                                     │
│       ▼                                                     │
│   Chat Page Loads   ──►  GET /users  (sidebar)             │
│       │                  POST /heartbeat  (every 5s)        │
│       │                  GET /online_users  (every 3s)      │
│       ▼                                                     │
│   Select Contact    ──►  GET /get_messages                  │
│       │                  POST /mark_seen  (auto-read)       │
│       ▼                                                     │
│   Send Message      ──►  POST /send_message                 │
│       │                  → Saved in messages.json           │
│       │                  → Logged in app.log                │
│       ▼                                                     │
│   Auto Refresh (3s) ──►  GET /get_messages  (ticks update) │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧠 Concepts Used

### 🐍 Python / Backend

| Concept | Implementation |
|---------|---------------|
| **OOP & Dataclasses** | `User`, `Message` with `to_dict()` / `from_dict()` |
| **File Handling** | JSON read/write for zero-database persistence |
| **Logging** | Singleton `LoggerManager` → console + `app.log` |
| **Custom Exceptions** | `UserAlreadyExistsError`, `UserNotFoundError` |
| **FastAPI** | REST endpoints, Pydantic validation, static file serving |
| **Pathlib** | Cross-platform file path management |
| **datetime** | Timestamps + heartbeat expiry via `is_online()` |

### 🌐 Frontend / JavaScript

| Concept | Implementation |
|---------|---------------|
| **Fetch API** | All HTTP calls to FastAPI endpoints |
| **DOM Manipulation** | Dynamic chat bubbles, user list, status dots |
| **setInterval** | 3s message poll + 5s heartbeat ping |
| **Session Storage** | Persist login across pages without backend sessions |
| **Read Receipts** | `mark_seen` on chat open → tick state rendering |
| **CSS Animations** | Bubble pop-in, fade-in, hover transitions |

---

## 📸 Data Storage Format

**`users.json`**
```json
[
  {
    "username": "ali",
    "display_name": "Ali Khan",
    "last_active": "2026-03-14T23:00:10.123456"
  }
]
```

**`messages.json`**
```json
[
  {
    "from": "ali",
    "to": "sara",
    "message": "Hello! 👋",
    "timestamp": "2026-03-14 23:00:10",
    "seen": true
  }
]
```

---

## 👨‍💻 Author

<div align="center">

<img src="https://avatars.githubusercontent.com/MudassarGill" width="100px" style="border-radius:50%" alt="MudassarGill"/>

### Mudassar Gill

[![GitHub](https://img.shields.io/badge/GitHub-%40MudassarGill-181717?style=for-the-badge&logo=github)](https://github.com/MudassarGill)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/MudassarGill)

*Passionate about building clean, practical Python projects.*

</div>

---

## 📄 License

This project is licensed under the **MIT License** — free to use, modify, and distribute.

---

<div align="center">

**⭐ If you found this project helpful, please give it a star!**

Made with ❤️ by [MudassarGill](https://github.com/MudassarGill)

</div>
