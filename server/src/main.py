from fastapi import FastAPI, Request, Response, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from infra.auth.jwt import (
    verify_machine_token,
    get_email_from_token,
)

from infra.storage.userdb import (
    read_user,
    read_user_by_email,
)
from infra.storage.mrepodb import (
    create_monitored_repo,
    read_monitored_repo_by_fullname,
    read_monitored_repo,
    create_parse_report,
)

from infra.integration.github import (
    get_github_repo,
    register_push_github_repo,
    get_github_repo_last_commit,
)

from infra.pubsub.pub import publish_parse_msg

from app.domain.auth import CreateMachineTokenInput, MachineToken
from app.domain.user import User
from app.domain.mrepo import AddMonitoredReposInput, AddParsedResultInput, MonitoredRepo

from logger import logger
from typing import List
import json


from app.interactors.auth import AuthInteractor
from app.interactors.user import UserInteractor

user_interactor = UserInteractor()
auth_interactor = AuthInteractor()

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
        user = await user_interactor.execute_get_user(email)
        return user

    except ValueError as e:
        logger.info(f"Can't find the requested user {get_user.__name__}: {str(e)}")
        raise HTTPException(status_code=404, detail={str(e)})

    except Exception as e:
        logger.critical(f"Unexpected exceptions at {get_user.__name__}: {str(e)}")
        raise e


# TODO: Add type definition for reponse
@app.get("/user/repos")
async def get_user_github_repos(
    email: str = Depends(get_email_from_token), status_code=200
):
    try:
        output = await user_interactor.execute_get_user_github_repos(email)
        return output

    except ValueError as e:
        logger.critical(f"Request failed at {get_user_github_repos.__name__}: {str(e)}")
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

        # Find the monitored repository -> If the repo exists and status is active proceed
        mrepo = await read_monitored_repo(payload["mrepoId"])
        user = await read_user(mrepo.userId)

        # Call GitHub API to get the latest commit (payload: repo fullname, oauth token, branch)
        oauth_token = user.oauth[0]["token"]

        gh_call_output = await get_github_repo_last_commit(
            oauth_token, mrepo.fullName, mrepo.defaultBranch
        )

        commit = gh_call_output["commit"]

        await create_parse_report(commit, payload)

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
        token = await auth_interactor.execute_github_auth(session_code)
        return token
    except ValueError as e:
        logger.critical(f"Invalid auth request. {handle_auth.__name__}: {str(e)}")
        raise HTTPException(status_code=401, detail={str(e)})
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
        token = await auth_interactor.execute_worker_auth(payload)
        response.status_code = 201
        return token
    except ValueError as e:
        logger.critical(f"Invalid auth request {handle_auth_worker.__name__}: {str(e)}")
        raise HTTPException(status_code=401, detail={str(e)})
    except Exception as e:
        logger.critical(
            f"Unexpected exceptions at {handle_auth_worker.__name__}: {str(e)}"
        )
        raise e


@app.post("/webhook/github/push")
async def process_gh_push_hook(payload=Depends(get_json_body), status_code=200):
    try:
        # Payload: https://docs.github.com/en/developers/webhooks-and-events/webhooks/webhook-events-and-payloads#push
        repo_fullname = payload["repository"]["full_name"]

        await publish_parse_msg(repo_fullname, "github")
        return "success"
    except Exception as e:
        logger.critical(
            f"Unexpected exceptions at {process_gh_push_hook.__name__}: {str(e)}"
        )
        raise e
