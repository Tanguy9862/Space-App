from google.cloud import secretmanager
import logging
from typing import Optional, Dict


def get_secret_from_gcp(secret_name: str, project_id: str) -> Optional[Dict[str, str]]:
    """
    Retrieve secrets from GCP Secret Manager.

    Args:
        secret_name (str): Name of the secret in GCP Secret Manager.
        project_id (str): GCP project ID where the secret is stored.

    Returns:
        Optional[Dict[str, str]]: A dictionary of secrets if found, None otherwise.
    """
    try:
        client = secretmanager.SecretManagerServiceClient()
        secret_path = f"projects/{project_id}/secrets/{secret_name}/versions/latest"

        response = client.access_secret_version(request={"name": secret_path})
        secret_payload = response.payload.data.decode("UTF-8")
        secrets = eval(secret_payload)  # Convert JSON string to dict
        logging.info(f"Successfully retrieved secrets from GCP Secret Manager for: {secret_name}")
        return secrets
    except Exception as e:
        logging.error(f"Failed to retrieve secrets from GCP Secret Manager: {e}")
        return None
