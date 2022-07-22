from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth.jwt import issue_token
from auth.github import get_github_access_token, get_github_user, get_github_user_email

from typing import Union

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
    return {"data": "stay present, be in the flow..!"}


@app.post("/auth/")
async def handle_auth(session_code: str):
    try:

        access_token_res = await get_github_access_token(session_code)

        token = access_token_res["access_token"]

        user_res = await get_github_user(token)

        email = user_res["email"]
        name = user_res["name"]
        profile_url = user_res["avatar_url"]
        github_username = user_res["login"]

        if email is None:
            email = await get_github_user_email(github_username, token)

        # TODO: Check if user exists in DB

        # TODO: Create actual User object
        # user = dict(
        #    email=email,
        #    name=name,
        #    profileUrl=profile_url,
        #    githubUsername=github_username,
        # )
        return issue_token(email)
    except e as error:
        # TODO: Proper logging and error handling
        print(error)
