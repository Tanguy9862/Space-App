import os

# Default environment that will be used if none is specified (used in config_loader.py)
DEFAULT_ENVIRONMENT = 'local'

# File and directory names
DATA_DIRECTORY_NAME = 'data'
HISTORICAL_FACTS_FILENAME = 'historical_facts.json'
PAST_LAUNCHES_FILENAME = 'nsf_past_launches.csv'
NEXT_LAUNCH_FILENAME = 'nsf_next_launch.json'

# GCP Configuration (if running in a GCP environment)
GCP_PROJECT_ID = 'your-gcp-project-id'
GCP_BUCKET_NAME = 'your-gcp-bucket-name'
GCP_SECRET_NAME = 'your-gcp-secret-name'  # The name of the secret in GCP Secret Manager, used to store the
# environment configuration (e.g., ENV=gcp)

# Local configuration to access GCP resources (only for development/testing)
# This sets the path to the service account key JSON file for authentication.
# If None, GCP authentication will rely on the default application credentials (ADC).
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'spacexploration-gcp-bucket-access.json' or None
