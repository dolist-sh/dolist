from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

from typing import Union

from helloworld import msg
from config import (
    GITHUB_OAUTH_CLIENT_ID,
    GITHUB_OAUTH_CLIENT_SECRET,
    GITHUB_OAUTH_CONFIRM_URI,
)

app = FastAPI()

origins = ["http://localhost", "http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"data": msg}


@app.post("/auth/")
def handle_auth(session_code: str):
    print(session_code)

    payload = {
        "client_id": GITHUB_OAUTH_CLIENT_ID,
        "client_secret": GITHUB_OAUTH_CLIENT_SECRET,
        "redirect_uri": GITHUB_OAUTH_CONFIRM_URI,
        "code": session_code,
    }

    headers = {"Accept": "application/json"}

    res = requests.post(
        f"https://github.com/login/oauth/access_token/", headers=headers, params=payload
    )
    data = res.json()

    return data
