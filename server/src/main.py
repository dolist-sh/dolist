from curses.ascii import HT
from fastapi import FastAPI, Request, Response, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from auth.jwt import (
    issue_token,
    issue_machine_token,
    verify_machine_token,
    get_email_from_token,
)
from auth.github import get_github_access_token, get_github_user, get_github_user_email

from storage.userdb import (
    read_user,
    read_user_by_email,
    create_user,
    write_github_token,
)
from storage.mrepodb import (
    create_monitored_repo,
    read_monitored_repo_by_fullname,
    read_monitored_repo,
)

from integration.github import (
    get_github_repo,
    get_github_repo_list,
    register_push_github_repo,
    get_github_repo_last_commit,
)

from pubsub.pub import publish_parse_msg

from domain.auth import CreateMachineTokenInput, MachineToken
from domain.user import User
from domain.mrepo import AddMonitoredReposInput, AddParsedResultInput, MonitoredRepo

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

        created_repos: List[MonitoredRepo] = []
        oauth_token = user.oauth[0]["token"]

        if len(payload["repos"]) > 0:
            for repo in payload["repos"]:
                repo = dict(repo)
                github_repo_check = await get_github_repo(oauth_token, repo["fullName"])

                # fmt: off
                if github_repo_check["status"] == "fail":
                    logger.warning(f"Non-existing GitHub repository was requested for monitoring | user_id: {user_id} | repo_fullname: {repo['fullName']}")

                if github_repo_check["status"] == "success":
                    duplication_check_result = await read_monitored_repo_by_fullname(repo["fullName"], "github")

                    # TODO: Handle the case of inactive repository included in the request
                    if duplication_check_result is None:
                        """ New repository """
                        new_repo = await create_monitored_repo(repo, user_id)
                        created_repos.append(new_repo)
                        await register_push_github_repo(oauth_token, repo["fullName"])
                    else:
                        """ Already monitored repository """
                        logger.warning(f"Already monitored repository was included in the {add_monitored_repos.__name__} | user_id: {user_id} | repo_name: {repo['fullName']}")
                # fmt: on

        if len(created_repos) > 0:
            logger.info(f"{len(created_repos)} repositories added for monitoring")
            response.status_code = 201
            return
        elif (len(created_repos) == 0) and (len(payload["repos"]) > 0):
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


@app.post("/monitoredrepo/parse/result", status_code=200)
async def write_parse_result(
    response: Response,
    payload: AddParsedResultInput = Depends(get_json_body),
    is_auth_req: bool = Depends(verify_machine_token),
):
    try:
        if is_auth_req is not True:
            raise HTTPException(status_code=401, detail="Unauthorized request")

        print(payload)

        # Find the monitored repository -> If the repo exists and status is active proceed
        mrepo = await read_monitored_repo(payload["mrepoId"])
        user = await read_user(mrepo.userId)

        print(mrepo)
        print(user)

        # Call GitHub API to get the latest commit (payload: repo fullname, oauth token, branch)
        oauth_token = user.oauth[0]["token"]

        gh_call_output = await get_github_repo_last_commit(
            oauth_token, mrepo.fullName, mrepo.defaultBranch
        )

        commit = gh_call_output["commit"]

        print(commit)

        # Start the transaction

        # Write a new record in the parsed result table

        # Load all previously parsed comments from DB
        # Find comments from DB (new, neutral, old) that doesn't exists in the payload -> mark these as resolved

        # Find comments from payload that doesn't exist yet in the DB

        # Mark previously new comments from DB to neutral
        # Write all new comments from payload to DB

        # Mark neutral comment older than certain duration to old (threshold tbd)

        # Update the last updated timestamps

        # Commit the transaction

        response.status_code = 201
        return
    except HTTPException as e:
        logger.warning(f"HTTP exception at {write_parse_result.__name__}: {str(e)}")
    except Exception as e:
        logger.critical(
            f"Unexpected exceptions at {write_parse_result.__name__}: {str(e)}"
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


@app.post("/auth/worker")
async def handle_auth_worker(
    response: Response,
    payload: CreateMachineTokenInput = Depends(get_json_body),
    status_code=200,
    response_model=MachineToken,
):
    try:
        from config import WORKER_OAUTH_CLIENT_ID, WORKER_OAUTH_CLIENT_SECRET

        client_id = payload["client_id"]
        client_secret = payload["client_secret"]

        if (client_id != WORKER_OAUTH_CLIENT_ID) or (
            client_secret != WORKER_OAUTH_CLIENT_SECRET
        ):
            raise HTTPException(status_code=401, detail="Invalid auth request")

        machine_token = issue_machine_token(payload)
        response.status_code = 201
        return machine_token
    except Exception as e:
        logger.critical(
            f"Unexpected exceptions at {handle_auth_worker.__name__}: {str(e)}"
        )
        raise e


@app.post("/webhook/github/push")
async def process_gh_push_hook(payload=Depends(get_json_body), status_code=200):
    try:
        # Payload: https://docs.github.com/en/developers/webhooks-and-events/webhooks/webhook-events-and-payloads#push
        print(payload)
        repo_fullname = payload["repository"]["full_name"]

        await publish_parse_msg(repo_fullname, "github")
        return "success"
    except Exception as e:
        logger.critical(
            f"Unexpected exceptions at {process_gh_push_hook.__name__}: {str(e)}"
        )
        raise e
