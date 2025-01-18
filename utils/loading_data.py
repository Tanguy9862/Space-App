import pandas as pd
import boto3
import json
import logging
from io import StringIO

from config import CONFIG, LambdaConfig, LocalConfig


def load_data(data_type: str, file_type: str):

    filename = CONFIG.FILENAME_MAPPING[data_type]

    # Loading data from local environment
    if isinstance(CONFIG, LocalConfig):

        filepath = f'{CONFIG.DATA_DIR_NAME}/{filename}'
        logging.info(f'[LOCAL ENV] -> Trying to load data for: {filename}')

        try:
            if file_type == 'json':
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = pd.read_csv(filepath)
            last_update = '[LOCAL ENVIRONMENT] No date available'
        except Exception as e:
            logging.warning(f'[+] Error loading file from {filepath}: {e}')
        else:
            logging.info(f'[+] {filename} successfully loaded!')
            return data, last_update

    # Loading data from AWS using S3 bucket
    elif isinstance(CONFIG, LambdaConfig):
        s3 = boto3.client('s3')
        logging.info(f'[AWS ENV] -> Attempting to load data file from Bucket: {CONFIG.BUCKET_NAME}, Key: {filename}')

        try:
            response = s3.get_object(Bucket=CONFIG.BUCKET_NAME, Key=filename)
            last_update = f"{response['LastModified'].strftime('%Y-%m-%d %H:%M:%S')} UTC"
            if file_type == 'json':
                data = json.load(response['Body'])
            else:
                csv_content = response['Body'].read().decode('utf-8')
                data = pd.read_csv(StringIO(csv_content))
        except s3.exceptions.NoSuchKey:
            logging.warning(f'[+] No data file found in S3 at Key: {filename}')
        else:
            logging.info(f'[+] Data file ({filename}) successfully loaded from S3!')
            return data, last_update

    raise RuntimeError(
        f"Invalid CONFIG detected. CONFIG must be an instance of either LocalConfig or LambdaConfig. "
        f"Current CONFIG: {type(CONFIG).__name__}"
    )

