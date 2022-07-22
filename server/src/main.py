from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth.jwt import issue_token
from auth.github import get_github_access_token, get_github_user, get_github_user_email
from storage.userrepo import read_user_by_email, create_user

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

        user_check_result = await read_user_by_email(email)

        if user_check_result is None:
            """Sign-up case"""

            oauth_payload = dict(type="github", token=token)
            user_payload = dict(
                email=email, name=name, profileUrl=profile_url, oauthInUse=oauth_payload
            )

            new_user = await create_user(user_payload)

            print("This is a new user object")
            print(new_user)

            return issue_token(new_user.email)

        else:
            """Sign-in case"""
            print("This is a sign-in case")
            return issue_token(user_check_result.email)

    except Exception as e:
        # TODO: Proper logging and error handling
        print(f"Unexpected exceptions: {str(e)}")
        raise e
