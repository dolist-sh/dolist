# Import all classes & modules for infra layer
import requests, jwt, sqlalchemy
from logger import logger

from infra.auth.github import GitHubOAuthService
from infra.auth.jwt import JWTService
from infra.integration.github import GitHubService

from infra.pubsub.sqs import parse_queue, failed_hook_queue
from infra.pubsub.pub import ParseMsgPublisher

from infra.storage.db import engine
from infra.storage.model import (
    user_schema,
    monitored_repo_schema,
    parsed_comment_schema,
)
from infra.storage.mrepodb import MonitoredRepoDBAccess
from infra.storage.userdb import UserDBAccess

# Resolve dependencies of classes at infra layer
github_oauth_service = GitHubOAuthService(requests)
jwt_service = JWTService(jwt)
github_service = GitHubService(requests, logger)

mrepodb = MonitoredRepoDBAccess(
    sqlalchemy, engine, monitored_repo_schema, parsed_comment_schema, logger
)
userdb = UserDBAccess(engine, user_schema)

publisher = ParseMsgPublisher(parse_queue, failed_hook_queue, mrepodb, userdb, logger)


# Import all usecases
from app.interactors.auth import GitHubAuthUseCase, WorkerAuthUseCase
from app.interactors.user import GetUserUseCase, GetUserGitHubReposUseCase
from app.interactors.webhook import GitHubPushHookUseCase
from app.interactors.mrepo import (
    GetMonitoredRepoUseCase,
    GetMonitoredReposUseCase,
    WriteParseResultUseCase,
    AddMonitoredReposUseCase,
)

github_auth_usecase = GitHubAuthUseCase(
    userdb=userdb, github_auth=github_oauth_service, jwt=jwt_service
)

worker_auth_usecase = WorkerAuthUseCase(
    userdb=userdb, github_auth=github_oauth_service, jwt=jwt_service
)

get_user_usecase = GetUserUseCase(userdb=userdb, github=github_service, logger=logger)

get_user_github_repos_usecase = GetUserGitHubReposUseCase(
    userdb=userdb, github=github_service, logger=logger
)
github_push_hook_usecase = GitHubPushHookUseCase(publisher=publisher)

get_mrepo_usecase = GetMonitoredRepoUseCase(
    userdb=userdb, mrepodb=mrepodb, github=github_service
)
get_mrepos_usecase = GetMonitoredReposUseCase(
    userdb=userdb, mrepodb=mrepodb, github=github_service
)
write_parse_result_usecase = WriteParseResultUseCase(
    userdb=userdb, mrepodb=mrepodb, github=github_service
)
add_mrepos_usecase = AddMonitoredReposUseCase(
    userdb=userdb, mrepodb=mrepodb, github=github_service
)


from app.interactors.auth import AuthInteractor
from app.interactors.mrepo import MonitoredRepoInteractor
from app.interactors.user import UserInteractor
from app.interactors.webhook import WebhookInteractor

# All dependencies of interactors are instantiated classes from infra layer
# Resolve dependencies of interactors
auth_interactor = AuthInteractor(
    auth_github=github_auth_usecase, auth_worker=worker_auth_usecase
)
user_interactor = UserInteractor(
    get_user_github_repos=get_user_github_repos_usecase, get_user=get_user_usecase
)
mrepo_interactor = MonitoredRepoInteractor(
    get_mrepo=get_mrepo_usecase,
    get_mrepos=get_mrepos_usecase,
    add_mrepos=add_mrepos_usecase,
    write_parse_result=write_parse_result_usecase,
)
webhook_interactor = WebhookInteractor(github_push_hook=github_push_hook_usecase)
