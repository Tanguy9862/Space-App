import boto3
import logging
from typing import Optional, Dict


def get_secret_from_aws(secret_name: str, region_name: str) -> Optional[Dict[str, str]]:
    """
    Retrieve secrets from AWS Secrets Manager.

    Args:
        secret_name (str): Name of the secret in AWS Secrets Manager.
        region_name (str): AWS region where the secret is stored.

    Returns:
        Optional[Dict[str, str]]: A dictionary of secrets if found, None otherwise.
    """
    try:
        session = boto3.session.Session()
        client = session.client(service_name="secretsmanager", region_name=region_name)

        response = client.get_secret_value(SecretId=secret_name)
        secrets = eval(response["SecretString"])  # Convert JSON string to dictus
        logging.info(f"Successfully retrieved secrets from AWS Secrets Manager for: {secret_name}")
        return secrets
    except Exception as e:
        logging.error(f"Failed to retrieve secrets from AWS Secrets Manager: {e}")
        return None

