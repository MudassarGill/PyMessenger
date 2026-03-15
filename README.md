<img src="https://capsule-render.vercel.app/api?type=waving&color=6C63FF&height=200&section=header&text=PyMessenger&fontSize=60&fontColor=ffffff&fontAlignY=38&desc=WhatsApp-style+Messenger+%7C+FastAPI+%2B+Vanilla+JS&descAlignY=58&descSize=18" width="100%" alt="PyMessenger Banner"/>

<div align="center">

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&size=22&pause=1000&color=6C63FF&center=true&vCenter=true&width=500&lines=Real-time+Chat+App;Online+Status+%2B+Read+Receipts;Built+with+FastAPI+%26+Vanilla+JS;File-based+Storage+-+No+Database!)](https://git.io/typing-svg)

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6%2B-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![HTML5](https://img.shields.io/badge/HTML5%2FCSS3-Latest-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![License](https://img.shields.io/badge/License-MIT-brightgreen?style=for-the-badge)](LICENSE)

**A WhatsApp-inspired local messaging app built with Python FastAPI and Vanilla JS.**

[Quick Start](#quick-start) &nbsp;|&nbsp;
[Features](#features) &nbsp;|&nbsp;
[Project Structure](#project-structure) &nbsp;|&nbsp;
[API Reference](#api-reference) &nbsp;|&nbsp;
[Author](#author)

</div>

---

## Overview

PyMessenger is a full-stack messaging web application that runs entirely on your local machine. It uses **FastAPI** for the backend REST API and **HTML/CSS/JavaScript** for the frontend, with all data stored in simple JSON files — no database required.

---

## Features

### Messaging
- Send and receive messages between users
- Auto-refresh every 3 seconds
- Timestamps and date dividers (Today / Yesterday)
- Scrollable chat history per conversation

### Online Status
- Green dot on avatar = user is online
- Gray dot = user is offline
- Powered by a heartbeat ping every 5 seconds
- Shows in both sidebar and chat header

### Read Receipts (Tick System)

| Tick | Meaning |
|------|---------|
| single gray tick | Sent — receiver is offline |
| double gray tick | Delivered — receiver is online but has not read yet |
| double green tick | Seen — receiver opened the chat and read the message |

### UI and Design
- Dark mode inspired by WhatsApp
- Gradient chat bubbles with animations
- Responsive layout for different screen sizes
- Toast notifications for errors

### Backend and Storage
- Username-based registration and login
- All data saved in JSON files (no database)
- Full activity logging to `logs/app.log`
- Custom error handling with exceptions

---

## Project Structure

```
PyMessenger/
|
+-- backend/
|   +-- main.py                FastAPI app and all REST endpoints
|   +-- models.py              User and Message dataclasses
|   +-- user_manager.py        Register, login, heartbeat, online check
|   +-- message_manager.py     Send, fetch, mark messages as seen
|   +-- logger_manager.py      Singleton logger for file and console
|   +-- storage/
|       +-- users.json         All registered users
|       +-- messages.json      All messages with seen status
|
+-- frontend/
|   +-- index.html             Login and Register page
|   +-- chat.html              Chat interface
|   +-- style.css              Dark-mode styles, ticks, online dots
|   +-- app.js                 Fetch API, heartbeat, DOM rendering
|
+-- logs/
|   +-- app.log                Auto-generated activity log
|
+-- requirements.txt
+-- README.md
```

---

## Quick Start

### Step 1 — Clone the repository

```bash
git clone https://github.com/MudassarGill/PyMessenger.git
cd PyMessenger
```

### Step 2 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Start the server

```bash
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

### Step 4 — Open in your browser

```
http://127.0.0.1:8000
```

> **Tip:** Open the app in two browser tabs with two different users to test the full chat and read receipt experience.

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register` | Register a new user |
| POST | `/login` | Login with username |
| POST | `/send_message` | Send a message to another user |
| GET | `/get_messages` | Get messages between two users |
| GET | `/users` | Get all registered users |
| GET | `/conversations` | Get all contacts of a user |
| POST | `/heartbeat` | Mark user as online (called every 5s) |
| GET | `/online_users` | Get list of currently online users |
| POST | `/mark_seen` | Mark messages as read |

> Interactive Swagger docs available at: `http://127.0.0.1:8000/docs`

---

## Application Flow

```
User opens browser
      |
      v
Register or Login  -->  POST /register  or  POST /login
      |
      v
Chat page loads    -->  GET /users           (load sidebar)
      |            -->  POST /heartbeat       (every 5s, mark online)
      |            -->  GET /online_users     (every 3s, update dots)
      |
      v
Select a user      -->  GET /get_messages     (load conversation)
      |            -->  POST /mark_seen        (auto read receipt)
      |
      v
Send a message     -->  POST /send_message    (saved to messages.json, logged)
      |
      v
Auto refresh (3s)  -->  GET /get_messages     (ticks and messages update)
```

---

## Data Storage Format

**users.json**
```json
[
  {
    "username": "ali",
    "display_name": "Ali Khan",
    "last_active": "2026-03-14T23:00:10.123456"
  }
]
```

**messages.json**
```json
[
  {
    "from": "ali",
    "to": "sara",
    "message": "Hello!",
    "timestamp": "2026-03-14 23:00:10",
    "seen": true
  }
]
```

---

## Concepts Used

### Python and Backend

| Concept | Where Used |
|---------|------------|
| OOP and Dataclasses | `User`, `Message` with `to_dict()` and `from_dict()` |
| File Handling | JSON read and write for all persistent storage |
| Logging | Singleton `LoggerManager` writing to file and console |
| Custom Exceptions | `UserAlreadyExistsError`, `UserNotFoundError` |
| FastAPI | REST endpoints, Pydantic request validation, static file serving |
| Pathlib | Cross-platform file path management |
| datetime | Timestamps and heartbeat expiry in `is_online()` |

### Frontend and JavaScript

| Concept | Where Used |
|---------|------------|
| Fetch API | All HTTP requests to the FastAPI backend |
| DOM Manipulation | Rendering chat bubbles, user list, status dots dynamically |
| setInterval | 3-second message poll and 5-second heartbeat ping |
| Session Storage | Persist logged-in user across page navigation |
| Read Receipts | `mark_seen` called on chat open, ticks rendered by `seen` flag |
| CSS Animations | Bubble pop-in, fade-in, and hover transition effects |

---

## Author

<div align="center">

**Mudassar Gill**

[![GitHub](https://img.shields.io/badge/GitHub-MudassarGill-181717?style=for-the-badge&logo=github)](https://github.com/MudassarGill)

*Passionate about building clean and practical Python projects.*

</div>

---

## License

This project is licensed under the **MIT License** — free to use, modify, and distribute.

---

<div align="center">

If you found this project useful, please consider giving it a star on GitHub.

Made with passion by [MudassarGill](https://github.com/MudassarGill)

</div>

<img src="https://capsule-render.vercel.app/api?type=waving&color=6C63FF&height=120&section=footer" width="100%" alt="footer wave"/>
