import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/status")
def get_status():
    with open("src/state.json", "r") as f:
        data = json.load(f)
    return data


@app.get("/trades")
def get_trades():
    return [
        {
            "time": "09:30",
            "signal": "BUY",
            "instrument": "RELIANCE",
            "entry": 2450,
            "pnl": 120
        }
    ]