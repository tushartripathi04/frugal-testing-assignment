
import asyncio
import json
import math
import random
import time

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI(title="Frugal Testing Canvas Lab")

BASE_DIR = Path(__file__).parent


@app.get("/")
def home():
    return FileResponse(BASE_DIR / "index.html")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.websocket("/ws")
async def websocket_stream(websocket: WebSocket):

    await websocket.accept()

    x = 180
    y = 150
    sequence = 0

    try:
        while True:

            sequence += 1

            # Initial loading state, followed by active states.
            status = "loading" if sequence == 1 else "active"

            # Simulate coordinate drift.
            x += random.choice([-8, -4, 4, 8])

            if x < 100:
                x = 100

            if x > 540:
                x = 540

            y = 150 + random.randint(-15, 15)

            balance = "1250.50"

            message = {
                "sequence": sequence,
                "status": status,
                "x": x,
                "y": y,
                "balance": balance,
                "timestamp": time.time_ns() // 1000,
            }

            await websocket.send_text(
                json.dumps(message)
            )

            await asyncio.sleep(1)

    except WebSocketDisconnect:
        print("Canvas client disconnected.")

    except Exception as error:
        print("WebSocket error:", error)
