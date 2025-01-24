import pandas as pd
import boto3
import json
import logging
from io import StringIO
from google.cloud import storage

from config import CONFIG, LocalConfig


def load_data(data_type: str, file_type: str):

    filename = CONFIG.FILENAME_MAPPING[data_type]

    # Loading data from local environment
    if isinstance(CONFIG, LocalConfig):

        filepath = f'{CONFIG.DATA_DIR_NAME}/{filename}'
        logging.info(f'[LOCAL] -> Trying to load data for: {filename}')

        try:
            if file_type == 'json':
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = pd.read_csv(filepath)
            last_update = '\[LOCAL ENVIRONMENT\] No date available'
        except Exception as e:
            logging.warning(f'[+] Error loading file from {filepath}: {e}')
        else:
            logging.info(f'[+] {filename} successfully loaded!')
            return data, last_update

    raise RuntimeError(
        f"Invalid CONFIG detected. CONFIG must be an instance of either LocalConfig or LambdaConfig. "
        f"Current CONFIG: {type(CONFIG).__name__}"
    )

