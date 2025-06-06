import os
import json
import asyncio
from datetime import datetime
from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from groq_api import generate_quest
import argparse

load_dotenv()

app = FastAPI()
app.mount("/overlay", StaticFiles(directory="./overlay"), name="overlay")
templates = Jinja2Templates(directory="./templates")

connected_websockets = []

state = {
    "mode": "idle",
    "idea": None,
    "votes": {"yes": 0, "no": 0},
    "voters": set(),
    "quest": "",
    "history": [],
    "dev_mode": os.getenv("DEV_MODE", "false").lower() == "true"
}

@app.get("/", response_class=HTMLResponse)
async def root():
    return HTMLResponse("Stream Quest Architect is running.")

@app.get("/dev")
async def dev_ui(request: Request):
    return templates.TemplateResponse("dev_ui.html", {"request": request})

@app.post("/submit_idea")
async def submit_idea(request: Request):
    data = await request.json()
    idea = data.get("idea", "").strip()
    if not idea:
        return {"error": "No idea provided"}

    if state["mode"] == "vote":
        return {"error": "Vote already in progress"}

    state.update({
        "mode": "vote",
        "idea": idea,
        "votes": {"yes": 0, "no": 0},
        "voters": set()
    })
    await broadcast_state()
    asyncio.create_task(handle_vote_period())
    return {"status": "Voting started"}

@app.get("/streamer")
async def streamer_panel(request: Request):
    return templates.TemplateResponse("streamer_controls.html", {"request": request})

@app.post("/quest_complete")
async def quest_complete():
    if state["mode"] != "quest":
        return {"error": "No active quest to complete"}
    await switch_overlay("quest_completed.html")
    await asyncio.sleep(6)
    await switch_overlay("index.html")
    return {"status": "Quest marked as complete"}

@app.post("/quest_skip")
async def quest_skip():
    if state["mode"] != "quest":
        return {"error": "No active quest to skip"}
    await switch_overlay("quest_skipped.html")
    await asyncio.sleep(6)
    await switch_overlay("index.html")
    return {"status": "Quest was skipped"}

@app.post("/submit_vote")
async def submit_vote(request: Request):
    data = await request.json()
    user = data.get("user")
    vote = data.get("vote")

    if state["mode"] != "vote":
        return {"error": "No active vote"}

    if user in state["voters"]:
        return {"error": "Already voted"}

    if vote not in ("yes", "no"):
        return {"error": "Invalid vote"}

    state["votes"][vote] += 1
    state["voters"].add(user)
    await broadcast_state()
    return {"status": f"Vote '{vote}' counted for {user}"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_websockets.append(websocket)
    serializable_state = get_serializable_state()
    await websocket.send_json(serializable_state)
    try:
        while True:
            await websocket.receive_text()
    except:
        connected_websockets.remove(websocket)

async def handle_vote_period():
    await asyncio.sleep(120) 
    yes_votes = state["votes"]["yes"]
    no_votes = state["votes"]["no"]
    passed = yes_votes > no_votes and yes_votes >= 1

    if passed:
        state["mode"] = "generating"
        await broadcast_state()
        quest = await generate_quest(state["idea"])
        state.update({
            "mode": "quest",
            "quest": quest,
            "history": [quest] + state["history"]
        })
        await broadcast_state()
        await asyncio.sleep(20 * 60) 
        state.update({
            "mode": "idle",
            "idea": None,
            "quest": "",
            "votes": {"yes": 0, "no": 0},
            "voters": set()
        })
        await broadcast_state()
    else:
        state.update({
            "mode": "idle",
            "idea": None,
            "votes": {"yes": 0, "no": 0},
            "voters": set()
        })
        await broadcast_state()

async def switch_overlay(filename):
    with open("overlay/current_view.txt", "w") as f:
        f.write(filename)


def get_serializable_state():
    return {
        **state,
        "voters": list(state["voters"]) 
    }

async def broadcast_state():
    serializable = get_serializable_state()
    for ws in connected_websockets:
        try:
            await ws.send_json(serializable)
        except:
            pass


@app.get("/current_overlay")
async def get_current_overlay():
    path = "overlay/current_view.txt"
    if not os.path.exists(path):
        return HTMLResponse("Overlay not set.")

    with open(path, "r") as f:
        filename = f.read().strip()

    with open(f"overlay/{filename}", "r") as f:
        html = f.read()

    return HTMLResponse(html)

@app.get("/refresh_overlay")
async def refresh_overlay():
    return {"status": "Overlay refresh triggered"}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dev", action="store_true", help="Run in dev mode without Twitch")
    args = parser.parse_args()

    if args.dev:
        import uvicorn
        print("Running in DEV mode at http://localhost:5000")
        uvicorn.run(app, host="0.0.0.0", port=5000)
    else:
        bot = Bot()
        loop = asyncio.get_event_loop()
        loop.create_task(broadcast_state())
        loop.create_task(bot.start())
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=5000)
