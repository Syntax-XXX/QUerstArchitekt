# 🎮 Stream Quest Architect

**Stream Quest Architect** is a real-time interactive tool for streamers to crowdsource quest ideas from their viewers, vote on them, and transform the winning ideas into fully written RPG-style quests using AI. It's built with FastAPI, WebSockets, and a custom overlay system for OBS or any browser-based source.

---

## ✨ Features

- 💡 Viewers submit quest ideas via chat or dev UI
- 🗳️ Real-time voting system with cooldowns
- 🤖 AI-generated quests using Groq's LLaMA models
- 🎭 OBS/browser overlay display for current vote or quest
- 🧭 Streamer control panel to skip or complete quests
- 🧪 Dev mode (`--dev`) for local testing and manual input
- 🔁 Automatic overlay switching (quest, completed, skipped, idle)

---

## 🛠️ Requirements

- Python 3.9+
- [Groq API Key](https://console.groq.com/)
- FastAPI & Uvicorn
- OBS or a browser for overlay display

install dependencies:
pip install -r requirements.txt

---

## 🚀 Getting Started

1. Clone and configure

- git clone https://github.com/yourname/stream-quest-architect.git
- cd stream-quest-architect
- cp .env.template .env
- Edit .env

2. Run in development mode
- python main.py --dev
- Web UI: http://localhost:5000/dev

- Overlay: Add a browser source pointing to:
- http://localhost:5000/current_overlay

3. Run in production (with Twitch bot or full chat integration)
- python main.py
- (Twitch bot setup code not included here – implement as needed.)

## 🧑‍💼 Streamer Panel
- Access the control panel at:
- http://localhost:5000/streamer_controls
- ✅ Mark quest complete
- ⏭️ Skip quest
- Both actions will switch the overlay and show a brief "completed" or "skipped" screen before returning to the current quest view.

## 🧩 Overlay Views
- All overlays are located in /overlay/:

- index.html – Idle state

- quest_completed.html – 6s overlay after quest completion

- quest_skipped.html – 6s overlay after skipping

- The current view is controlled by:
- overlay/current_view.txt

## 📁 Project Structure
```
├── main.py                 # FastAPI app with WebSocket, endpoints, logic
├── groq_api.py             # AI generation via Groq API
├── overlay/                # HTML files for OBS overlay
├── templates/              # Dev UI and streamer controls
├── static/                 # Static files (CSS, JS if any)
├── .env                    # Environment variables
├── requirements.txt
└── README.md
```

## 📄 License
- MIT License. See LICENSE for more details.

## 🤝 Contributions
- Pull requests and feedback are welcome! If you want to extend this for Twitch chat integration, feel free to fork or open a feature request.

## 📷 Credits
- Built by Syntax-XXX

- Uses Groq API for AI-based quest generation

---

- if there are any questions join my [discord](https://dsc.gg/syntax-xxx)
