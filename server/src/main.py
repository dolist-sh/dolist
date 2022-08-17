from fastapi import FastAPI, Request, Response, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from auth.jwt import issue_token, get_email_from_token
from auth.github import get_github_access_token, get_github_user, get_github_user_email

from storage.userdb import read_user_by_email, create_user, write_github_token
from storage.mrepodb import create_monitored_repo, read_user_monitored_repo_by_fullname

from integration.github import (
    get_github_repo,
    get_github_repo_list,
    register_push_github_repo,
)
from pubsub.pub import publish_parse_req

from domain.user import User
from domain.mrepo import AddMonitoredReposInput, MonitoredRepo

from logger import logger
from typing import List
import json


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


async def get_json_body(request: Request):
    body = await request.body()
    return json.loads(body)


@app.get("/")
def read_root():
    return {"data": "stay present, be in the flow..!"}


# TODO: Replace this call with get_user_repo
@app.get("/user")
async def get_user(
    email: str = Depends(get_email_from_token), status_code=200, response_model=User
):
    try:
        user = await read_user_by_email(email)
        return user

    except Exception as e:
        logger.critical(f"Unexpected exceptions at {get_user.__name__}: {str(e)}")
        raise e


# TODO: Add type definition for reponse
@app.get("/user/repos")
async def get_user_github_repos(
    email: str = Depends(get_email_from_token), status_code=200
):
    try:
        user = await read_user_by_email(email)
        github_token = user.oauth[0]["token"]  # TODO: Replace this with find call

        from src.integration.github import GetGitHubRepoListOutput

        output: GetGitHubRepoListOutput = await get_github_repo_list(github_token)

        if output["status"] == "success":
            return output["data"]
        else:
            raise HTTPException(status_code=422, detail=output["error"])

    except Exception as e:
        logger.critical(
            f"Unexpected exceptions at {get_user_github_repos.__name__}: {str(e)}"
        )
        raise e


# TODO: Rename this endpoint to improve readability of uri, using different term for monitored repo might be good idea
@app.post("/user/monitoredrepo", status_code=200)
async def add_monitored_repos(
    response: Response,
    payload: AddMonitoredReposInput = Depends(get_json_body),
    email: str = Depends(get_email_from_token),
):
    """Add GitHub repositories are monitored repos"""
    try:
        user = await read_user_by_email(email)
        user_id = user.id

        batch: List[MonitoredRepo] = []
        oauth_token = user.oauth[0]["token"]

        if len(payload["repos"]) > 0:
            for repo in payload["repos"]:
                repo = dict(repo)
                github_repo_check = await get_github_repo(oauth_token, repo["fullName"])

                # fmt: off
                if github_repo_check["status"] == "fail":
                    logger.warning(f"Non-existing GitHub repository was requested for monitoring | user_id: {user_id} | repo_fullname: {repo['fullName']}")

                if github_repo_check["status"] == "success":
                    duplication_check_result = await read_user_monitored_repo_by_fullname(repo["fullName"], user_id )

                    # TODO: Handle the case of inactive repository included in the request
                    if duplication_check_result is None:
                        """ New repository """
                        new_repo = await create_monitored_repo(repo, user_id)
                        batch.append(new_repo)
                        await register_push_github_repo(oauth_token, repo["fullName"])
                    else:
                        """ Already monitored repository """
                        logger.warning(f"Already monitored repository was included in the {add_monitored_repos.__name__} | user_id: {user_id} | repo_name: {repo['fullName']}")
                # fmt: on

        if len(batch) > 0:
            # TODO: Remove this, github will send push webhook as soon as it's registered
            publish_parse_req(batch, oauth_token)
            response.status_code = 201
            return
        elif (len(batch) == 0) and (len(payload["repos"]) > 0):
            """When nothing to process from the requested list of repositories"""
            raise HTTPException(
                status_code=422, detail="No repository to process from the payload"
            )
    except HTTPException as e:
        logger.warning(f"HTTP exception at {add_monitored_repos.__name__}: {str(e)}")
    except Exception as e:
        logger.critical(
            f"Unexpected exceptions at {add_monitored_repos.__name__}: {str(e)}"
        )
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
        logger.critical(f"Unexpected exceptions at {handle_auth.__name__}: {str(e)}")
        raise e


@app.post("/webhook/github/push")
def process_gh_push_hook(payload=Depends(get_json_body), status_code=200):
    try:
        print(payload)
        return "okay"
    except Exception as e:
        logger.critical(
            f"Unexpected exceptions at {process_gh_push_hook.__name__}: {str(e)}"
        )
        raise e
