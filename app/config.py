# 1. Standard library imports
import json
import os
import sys
from typing import Optional

import firebase_admin
# 2. Third party imports
from decouple import config
from firebase_admin import credentials, db
from google.cloud import firestore
from loguru import logger
from pydantic import BaseModel

from app.core.gateway.distance_matrix_osm_impl import DistanceMatrixGateway, DistanceMatrixOsmImpl
from app.core.gateway.hive_backend_impl import HiveBackendGateway, HiveBackendGatewayImpl
from app.core.gateway.open_ai_impl import OpenAIGateway, OpenAIGatewayImpl
from app.core.repositories.all_tables import HiveQueriesRepoImpl
from app.core.repositories.cache_firestore_repo_impl import CacheQueriesRepo, CacheFirestoreRepoImpl
from app.core.repositories.models.all_tables_repo import HiveQueriesRepo
from app.logic.query_generator_ai.index import QueryGeneratorAIUC, QueryGeneratorAIUCImpl
from security.logger_gcp_config import configure_logger as gcp_configure_logger

# 3. Utilities

from security.secret_manager import set_env_vars_from_gcp_secret_manager

logger.add(sys.stdout, level="DEBUG")


class Configuration(BaseModel):
    ENVIRONMENT: str
    GCP_PROJECT_ID: Optional[str] = None
    GCP_SECRET_NAME: Optional[str] = None
    GCP_SECRET_VERSION: Optional[str] = None


def manage_configuration_secrets(configuration: Configuration):
    if "local" in configuration.ENVIRONMENT:
        logger.info("Local Configuration. Loading from .env file")
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(config("PROJECT_ROOT"),
                                                                    "creds/google-creds-phoenix.json")
    elif configuration.ENVIRONMENT in ["staging", "production"]:
        logger.info(f"{configuration.ENVIRONMENT} Configuration. Loading from secret manager")
        # Set common secrets
        set_env_vars_from_gcp_secret_manager(
            configuration.GCP_PROJECT_ID,
            configuration.GCP_SECRET_NAME,
            configuration.GCP_SECRET_VERSION
        )
    else:
        raise Exception("Invalid environment")


def new_configuration():
    environment = config("ENVIRONMENT", default="local")

    configuration = Configuration(ENVIRONMENT=environment)
    if environment != "local":
        configuration.ENVIRONMENT = config("ENVIRONMENT", default="local")
        configuration.GCP_PROJECT_ID = config("GCP_PROJECT_ID", None)
        configuration.GCP_SECRET_NAME = config("GCP_SECRET_NAME", None)
        configuration.GCP_SECRET_VERSION = config("GCP_SECRET_VERSION", None)

    # Manage logger
    if configuration.ENVIRONMENT == "local":
        pass
    else:
        gcp_configure_logger()
    # Manage secrets
    manage_configuration_secrets(configuration)
    return configuration


def di_configuration(binder, _=new_configuration()):
    config_db = {
        "user": config("DB_USER"),
        "password": config("DB_PASSWORD"),
        "database": config("DB_NAME"),
        "charset": 'utf8mb4'
    }
    if config("ENVIRONMENT", "local") != "local":
        config_db["unix_socket"] = config("DB_SOCKET")
    else:
        config_db["host"] = config("DB_HOST")

    cred = credentials.Certificate(json.loads(config("FILE_SIGNER_CREDS").replace("'", '"')))
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://phoenix-247205.firebaseio.com/'
    })
    # CORE
    #   gateways
    binder.bind(DistanceMatrixGateway, DistanceMatrixOsmImpl(config("OSM_BASE_URL")))
    binder.bind(HiveBackendGateway, HiveBackendGatewayImpl(
        base_url=config("HIVE_BACKEND_URL"),
        api_token=config("HIVE_BACKEND_API_KEY")
    ))

    #   repos
    binder.bind(HiveQueriesRepo, HiveQueriesRepoImpl(config_db))
    binder.bind(OpenAIGateway, OpenAIGatewayImpl(config("OPENAI_API_KEY")))
    binder.bind(CacheQueriesRepo, CacheFirestoreRepoImpl(firestore_client=firestore.AsyncClient()))
    # LOGIC
    #   use cases
    binder.bind(QueryGeneratorAIUC, QueryGeneratorAIUCImpl())
