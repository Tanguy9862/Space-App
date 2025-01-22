import os

# Default environment that will be used if none is specified (used in config_loader.py)
DEFAULT_ENVIRONMENT = 'local'

# File and directory names
DATA_DIRECTORY_NAME = 'data'
HISTORICAL_FACTS_FILENAME = 'historical_facts_data.json'
PAST_LAUNCHES_FILENAME = 'nsf_past_launches.csv'
NEXT_LAUNCH_FILENAME = 'nsf_next_launch.json'

# AWS Configuration (if running in an AWS environment)
AWS_BUCKET_NAME = 'app-space-exploration-bucket'
AWS_SECRET_NAME = 'space-exploration-app/environment-config'
AWS_REGION_NAME = 'us-east-1'

# GCP Configuration (if running in a GCP environment)
GCP_BUCKET_NAME = 'space-exploration-bucket-test'
GCP_SECRET_NAME = 'space-exploration-secret-env-config'
GCP_PROJECT_ID = 'spacexploration'

# Local configuration to access GCP resources (only for development/testing)
# This sets the path to the service account key JSON file for authentication.
# If None, GCP authentication will rely on the default application credentials (ADC).
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'spacexploration-gcp-bucket-access.json' or None
