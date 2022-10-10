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
github_auth_adaptor = GitHubOAuthService(requests)
jwt_adaptor = JWTService(jwt)
github_adaptor = GitHubService(requests, logger)

mrepodb = MonitoredRepoDBAccess(
    sqlalchemy, engine, monitored_repo_schema, parsed_comment_schema, logger
)
userdb = UserDBAccess(engine, user_schema)

publisher = ParseMsgPublisher(parse_queue, failed_hook_queue, mrepodb, userdb, logger)


# Import interactors
from app.interactors.auth import AuthInteractor
from app.interactors.mrepo import MonitoredRepoInteractor
from app.interactors.user import UserInteractor
from app.interactors.webhook import WebhookInteractor

# All dependencies of interactors are instantiated classes from infra layer
# Resolve dependencies of interactors
auth_interactor = AuthInteractor(userdb, github_auth_adaptor, jwt_adaptor)
mrepo_interactor = MonitoredRepoInteractor(userdb, mrepodb, github_adaptor)
user_interactor = UserInteractor(userdb, mrepodb, github_adaptor, logger)
webhook_interactor = WebhookInteractor(publisher)
