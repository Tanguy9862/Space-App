import os
from dotenv import load_dotenv
from typing import Optional
from user_config import AWS_SECRET_NAME, AWS_REGION_NAME
from utils.aws_secrets_manager import get_secret_from_aws

# Load .env file for local environments
load_dotenv()


def get_env_variable(var_name: str, default: Optional[str] = None) -> str:
    """
    Retrieve an environment variable from the system, AWS, or GCP Secret Manager.

    Args:
        var_name (str): The name of the environment variable to retrieve.
        default (Optional[str]): The default value to use if the variable is not found.

    Returns:
        str: The value of the environment variable.

    Raises:
        RuntimeError: If the variable is not found and no default is provided.
    """
    # Step 1: Check system environment variables
    value = os.getenv(var_name)
    if value:
        return value

    # Step 2: Check AWS Secrets Manager
    aws_secrets = get_secret_from_aws(secret_name=AWS_SECRET_NAME, region_name=AWS_REGION_NAME)
    if aws_secrets and var_name in aws_secrets:
        return aws_secrets[var_name]

    # Step 4: Use default value if available
    if default:
        return default

    # If not found, raise an error
    raise RuntimeError(f"Environment variable '{var_name}' not found.")
