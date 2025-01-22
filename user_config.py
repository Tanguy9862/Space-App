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
