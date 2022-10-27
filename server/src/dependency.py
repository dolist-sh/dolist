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

github_auth_usecase, worker_auth_usecase = GitHubAuthUseCase(
    userdb, github_oauth_service, jwt_service
), WorkerAuthUseCase(userdb, github_oauth_service, jwt_service)

get_user_usecase, get_user_github_repos_usecase = GetUserUseCase(
    userdb, github_service, logger
), GetUserGitHubReposUseCase(userdb, github_service, logger)


from app.interactors.auth import AuthInteractor
from app.interactors.mrepo import MonitoredRepoInteractor
from app.interactors.user import UserInteractor
from app.interactors.webhook import WebhookInteractor

# All dependencies of interactors are instantiated classes from infra layer
# Resolve dependencies of interactors
auth_interactor = AuthInteractor(github_auth_usecase, worker_auth_usecase)
user_interactor = UserInteractor(get_user_github_repos_usecase, get_user_usecase)
mrepo_interactor = MonitoredRepoInteractor(userdb, mrepodb, github_service)
webhook_interactor = WebhookInteractor(publisher)
