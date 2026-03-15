# 💬 PyMessenger

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-CSS3-orange?style=for-the-badge&logo=html5&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6%2B-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**A WhatsApp-style local messaging web app built with FastAPI & Vanilla JS**

[Features](#-features) • [Folder Structure](#-folder-structure) • [Setup](#-setup) • [API Docs](#-api-endpoints) • [Author](#-author)

</div>

---

## 🚀 Features

- 🔐 **User Registration & Login** — simple username-based auth stored in JSON
- 💬 **Real-time Chat** — send and receive messages between users
- 🟢 **Online / Offline Status** — green dot when user is active, gray when offline
- ✅ **Read Receipts (Tick System)** — WhatsApp-style ticks on every sent message
  - `✓` gray = sent (receiver offline)
  - `✓✓` gray = delivered (receiver online, not read yet)
  - `✓✓` 🟢 green = **Seen** (receiver opened the chat)
- 🗂️ **File-based Storage** — all data persisted in `users.json` & `messages.json`
- 📜 **Logging** — every login, registration, and message tracked in `logs/app.log`
- 🎨 **Modern Dark UI** — WhatsApp-inspired dark-mode interface with smooth animations
- ⚡ **Auto-polling** — chat + online status refreshes every 3 seconds automatically
- 🛡️ **Error Handling** — try/except blocks + custom exceptions throughout

---

## 📁 Folder Structure

```
PyMessenger/
│
├── backend/
│   ├── main.py              # FastAPI app — all REST endpoints
│   ├── models.py            # User & Message dataclasses
│   ├── message_manager.py   # MessageManager — send/retrieve messages
│   ├── user_manager.py      # UserManager — register/login/list users
│   ├── logger_manager.py    # LoggerManager — file + console logging
│   └── storage/
│       ├── users.json       # Registered users
│       └── messages.json    # All messages
│
├── frontend/
│   ├── index.html           # Login / Register page
│   ├── chat.html            # Chat interface
│   ├── style.css            # Dark-mode UI styles
│   └── app.js               # Fetch API + DOM updates
│
├── logs/
│   └── app.log              # Auto-generated log file
│
├── requirements.txt
└── README.md
```

---

## 🛠️ Setup

### 1. Clone the repo

```bash
git clone https://github.com/MudassarGill/PyMessenger.git
cd PyMessenger
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the server

```bash
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

### 4. Open your browser

```
http://127.0.0.1:8000
```

> Register two users, open the app in two browser tabs, and start chatting!

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/register` | Register a new user |
| `POST` | `/login` | Login with username |
| `POST` | `/send_message` | Send a message |
| `GET`  | `/get_messages?user1=&user2=` | Get messages between two users |
| `GET`  | `/users` | List all registered users |
| `GET`  | `/conversations?user=` | Get contacts for a user |
| `POST` | `/heartbeat` | Ping to mark user as online (every 5s) |
| `GET`  | `/online_users` | Get list of currently online users |
| `POST` | `/mark_seen` | Mark messages as seen (read receipt) |

> 📖 **Interactive API docs** → `http://127.0.0.1:8000/docs`

---

## 🧠 Python Concepts Used

| Concept | Usage |
|---------|-------|
| **OOP / Dataclasses** | `User`, `Message`, `UserManager`, `MessageManager`, `LoggerManager` |
| **File Handling** | JSON read/write for persistent storage |
| **Logging** | `logging` module → `logs/app.log` |
| **Error Handling** | `try/except`, custom exceptions (`UserAlreadyExistsError`) |
| **FastAPI** | REST endpoints, Pydantic request validation |
| **Pathlib** | Cross-platform file paths |
| **datetime** | Timestamps, heartbeat expiry calculation (`is_online()`) |

---

## 🌐 Frontend Concepts Used

| Concept | Usage |
|---------|-------|
| **HTML5** | Semantic structure, forms, chat layout |
| **CSS3** | Dark mode, gradients, animations, chat bubbles, online dot badge |
| **JavaScript (ES6+)** | Fetch API, DOM manipulation, events |
| **Auto-polling** | `setInterval` refreshes chat + online status every 3 seconds |
| **Heartbeat** | `setInterval` pings `/heartbeat` every 5s to stay marked as online |
| **Session Storage** | Stores logged-in user across pages |
| **Read Receipts** | `mark_seen` called on chat open; ticks rendered from `seen` + online state |

---

## 📸 App Flow

```
User opens browser
     │
     ▼
Login / Register  ──► POST /login or /register
     │
     ▼
Chat Page loads   ──► GET /users  (sidebar user list)
     │
     ▼
Select a user     ──► GET /get_messages?user1=&user2=
     │
     ▼
Send message      ──► POST /send_message  ──► saved in messages.json + logged
     │
     ▼
Auto-refresh (3s) ──► GET /get_messages   (new bubbles appear)
```

---

## 👨‍💻 Author

<div align="center">

**Mudassar Gill**

[![GitHub](https://img.shields.io/badge/GitHub-MudassarGill-181717?style=for-the-badge&logo=github)](https://github.com/MudassarGill)

*Built with ❤️ using Python & FastAPI*

</div>

---

## 📄 License

This project is licensed under the **MIT License** — feel free to use and modify it.
