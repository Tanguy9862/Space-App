import logging
from user_config import (
    DEFAULT_ENVIRONMENT,
    DATA_DIRECTORY_NAME,
    HISTORICAL_FACTS_FILENAME,
    PAST_LAUNCHES_FILENAME,
    NEXT_LAUNCH_FILENAME,
    AWS_BUCKET_NAME,
    GCP_BUCKET_NAME,
)
from utils.config_loader import get_env_variable

ENV = get_env_variable("ENV", DEFAULT_ENVIRONMENT)


class BaseConfig:
    FILENAME_MAPPING = {
        'HISTORICAL_FACTS_FILENAME': HISTORICAL_FACTS_FILENAME,
        'PAST_LAUNCHES_FILENAME': PAST_LAUNCHES_FILENAME,
        'NEXT_LAUNCH_FILENAME': NEXT_LAUNCH_FILENAME
    }


class LocalConfig(BaseConfig):
    ENV = 'local'
    DATA_DIR_NAME = DATA_DIRECTORY_NAME


class AWSConfig(BaseConfig):
    ENV = 'aws'
    BUCKET_NAME = AWS_BUCKET_NAME


class GCPConfig(BaseConfig):
    ENV = 'gcp'
    BUCKET_NAME = GCP_BUCKET_NAME


def get_config():
    if ENV == 'aws':
        return AWSConfig()
    elif ENV == 'gcp':
        return GCPConfig()
    return LocalConfig()


CONFIG = get_config()
