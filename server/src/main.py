from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from auth.jwt import issue_token, get_email_from_token
from auth.github import get_github_access_token, get_github_user, get_github_user_email
from integration.github import get_github_repos
from storage.userrepo import read_user_by_email, create_user, write_github_token

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


# TODO: Replace this call with get_user_repo
@app.get("/user")
async def get_user(email: str = Depends(get_email_from_token), status_code=200):
    try:

        user = await read_user_by_email(email)
        return user

    except Exception as e:
        print(f"Unexpected exceptions: {str(e)}")
        raise e


# TODO: Add type definition for reponse
@app.get("/user/repos")
async def get_user_repos(email: str = Depends(get_email_from_token), status_code=200):
    try:

        user = await read_user_by_email(email)
        github_token = user.oauth[0]['token']  # TODO: Replace this with find call
        print(github_token)
        github_repos = await get_github_repos(github_token)

        return github_repos

    except Exception as e:
        print(f"Unexpected exceptions: {str(e)}")
        raise e


# TODO: Make this call properly return the Token model
@app.post("/auth/")
async def handle_auth(session_code: str, status_code=200):
    try:
        github_token = await get_github_access_token(session_code)

        if github_token is None:
            raise HTTPException(status_code=401, detail="Invalid session code")

        github_user = await get_github_user(github_token)

        email = github_user["email"]
        name = github_user["name"]
        profile_url = github_user["avatar_url"]
        github_username = github_user["login"]

        if email is None:
            """
            Fetch email address for user who marked their email as private.
            This step is requred as email field from get_github_user method returns null,
            When user have marked their email private.
            """
            email = await get_github_user_email(github_username, github_token)

        user_check_result = await read_user_by_email(email)

        oauth_payload = dict(type="github", token=github_token)

        if user_check_result is None:
            """Sign-up case"""

            user_payload = dict(
                email=email, name=name, profileUrl=profile_url, oauthInUse=oauth_payload
            )

            new_user = await create_user(user_payload)

            return issue_token(new_user.email)

        else:
            """Sign-in case"""
            # TODO: Store a new github token
            # await write_github_token(email, github_token)
            return issue_token(user_check_result.email)

    except Exception as e:
        # TODO: Proper logging and error handling
        print(f"Unexpected exceptions: {str(e)}")
        raise e
