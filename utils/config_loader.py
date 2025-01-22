import os
from dotenv import load_dotenv
from typing import Optional
from user_config import GCP_SECRET_NAME, GCP_PROJECT_ID
from utils.gcp_secrets_manager import get_secret_from_gcp

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

    # Step 3: Check GCP Secret Manager
    gcp_secrets = get_secret_from_gcp(secret_name=GCP_SECRET_NAME, project_id=GCP_PROJECT_ID)
    if gcp_secrets and var_name in gcp_secrets:
        return gcp_secrets[var_name]

    # Step 4: Use default value if available
    if default:
        return default

    # If not found, raise an error
    raise RuntimeError(f"Environment variable '{var_name}' not found.")
