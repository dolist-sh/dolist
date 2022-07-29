from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from auth.jwt import issue_token, get_email_from_token
from auth.github import get_github_access_token, get_github_user, get_github_user_email
from integration.github import get_github_repos, parse_github_repo
from storage.userrepo import read_user_by_email, create_user, write_github_token

from domain.user import User
from dolistparser import ParsedComment
from typing import Union, List

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://15.188.137.121",
    "http://ec2-15-188-137-121.eu-west-3.compute.amazonaws.com",
]

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


@app.get("/repo/tasks")
async def get_repo_tasks(
    repo_name: str,
    branch: str,
    email: str = Depends(get_email_from_token),
    status_code=200,
    response_model=List[ParsedComment],
):
    try:

        user = await read_user_by_email(email)
        github_token = user.oauth[0]["token"]

        tasks = await parse_github_repo(github_token, repo_name, branch)

        return tasks
    except Exception as e:
        print(f"Unexpected exceptions: {str(e)}")
        raise e


# TODO: Replace this call with get_user_repo
@app.get("/user")
async def get_user(
    email: str = Depends(get_email_from_token), status_code=200, response_model=User
):
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
        github_token = user.oauth[0]["token"]  # TODO: Replace this with find call

        github_repos = await get_github_repos(github_token)

        return github_repos

    except Exception as e:
        print(f"Unexpected exceptions: {str(e)}")
        raise e


# TODO: Make this call properly return the Token model
@app.get("/auth")
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

            await create_user(user_payload)

            return issue_token(user_payload.email)

        else:
            """Sign-in case"""
            await write_github_token(email, github_token)

            return issue_token(user_check_result.email)

    except Exception as e:
        # TODO: Proper logging and error handling
        print(f"Unexpected exceptions: {str(e)}")
        raise e
