from re import M
from uuid import UUID
from fastapi import FastAPI, Response, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from .helpers import (
    verify_machine_token,
    get_email_from_token,
    get_json_body,
)

from dependency import (
    auth_interactor,
    mrepo_interactor,
    user_interactor,
    webhook_interactor,
    logger,
)

from app.domain.auth import CreateMachineTokenInput, MachineToken
from app.domain.user import User
from app.domain.mrepo import AddMonitoredReposInput, AddParsedResultInput, MonitoredRepo
from typing import List

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


# TODO: Replace this call with get_user_repo
@app.get("/user")
async def get_user(
    email: str = Depends(get_email_from_token), status_code=200, response_model=User
):
    try:
        user = await user_interactor.get_user.execute(email)
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
        output = await user_interactor.get_user_github_repos.execute(email)
        return output

    except ValueError as e:
        logger.critical(f"Request failed at {get_user_github_repos.__name__}: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))

    except Exception as e:
        logger.critical(
            f"Unexpected exceptions at {get_user_github_repos.__name__}: {str(e)}"
        )
        raise e


# TODO: Rename this endpoint to improve readability of uri, using different term for monitored repo might be good idea
@app.post("/monitoredrepos", status_code=200)
async def add_monitored_repos(
    response: Response,
    payload: AddMonitoredReposInput = Depends(get_json_body),
    email: str = Depends(get_email_from_token),
):
    try:
        new_monitored_repos = await mrepo_interactor.add_mrepos.execute(email, payload)

        if len(new_monitored_repos) > 0:
            logger.info(f"{len(new_monitored_repos)} repositories added for monitoring")
            response.status_code = 201
            return
        elif (len(new_monitored_repos) == 0) and (len(payload["repos"]) > 0):
            """The case that all repos from payload are already monitored"""
            logger.warning(
                f"HTTP exception at {add_monitored_repos.__name__}: all repositoires in the payload are already monitored"
            )
            raise HTTPException(
                status_code=422, detail="No repository to process from the payload"
            )
    except Exception as e:
        logger.critical(
            f"Unexpected exceptions at {add_monitored_repos.__name__}: {str(e)}"
        )
        raise e


@app.post("/monitoredrepos/{mrepo_id}/parse/result", status_code=200)
async def write_parse_result(
    response: Response,
    mrepo_id: UUID,
    payload: AddParsedResultInput = Depends(get_json_body),
    is_auth_req: bool = Depends(verify_machine_token),
):
    try:
        if is_auth_req is not True:
            raise HTTPException(status_code=401, detail="Unauthorized request")

        result = await mrepo_interactor.write_parse_result.execute(payload, mrepo_id)

        if result["status"] == "failed":
            logger.warning(
                f"HTTP exception at {write_parse_result.__name__}: {result['error']}"
            )
            raise HTTPException(status_code=422, detail=result["error"])
        else:
            logger.info(
                f"New parse report created for the repository: {payload['mrepoId']}"
            )
            response.status_code = 201
            return
    except Exception as e:
        logger.critical(
            f"Unexpected exceptions at {write_parse_result.__name__}: {str(e)}"
        )
        raise e


@app.get("/monitoredrepos", status_code=200)
async def get_monitored_repos(
    email: str = Depends(get_email_from_token),
    limit: int = 100,
    offset: int = 0,
    response_model=List[MonitoredRepo],
):
    try:
        result = await mrepo_interactor.get_mrepos.execute(email, limit, offset)
        return result
    except Exception as e:
        logger.critical(
            f"Unexpected exceptions at {get_monitored_repos.__name__}: {str(e)}"
        )
        raise e


@app.get("/monitoredrepos/{mrepo_id}", status_code=200)
async def get_monitored_repo(
    mrepo_id: UUID,
    email: str = Depends(get_email_from_token),
    response_model=MonitoredRepo,
):
    try:
        result = await mrepo_interactor.get_mrepo.execute(email, mrepo_id)
        return result
    except Exception as e:
        logger.critical(
            f"Unexpected exceptions at {get_monitored_repo.__name__}: {str(e)}"
        )
        raise e


# TODO: Make this call properly return the Token model
@app.get("/auth")
async def handle_auth(session_code: str, status_code=200):
    try:
        token = await auth_interactor.auth_github.execute(session_code)
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
        token = await auth_interactor.auth_worker.execute(payload)
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
        await webhook_interactor.github_push_hook.execute(payload)
    except Exception as e:
        logger.critical(
            f"Unexpected exceptions at {process_gh_push_hook.__name__}: {str(e)}"
        )
        raise e
