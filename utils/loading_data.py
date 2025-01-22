import pandas as pd
import json
import logging
from io import StringIO
from google.cloud import storage

from config import CONFIG, GCPConfig, LocalConfig


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
            last_update = '[LOCAL ENVIRONMENT] No date available'
        except Exception as e:
            logging.warning(f'[+] Error loading file from {filepath}: {e}')
        else:
            logging.info(f'[+] {filename} successfully loaded!')
            return data, last_update

    # Loading data from GCP using Cloud Storage
    elif isinstance(CONFIG, GCPConfig):
        logging.info(f'[GCP] -> Attempting to load data file from Bucket: {CONFIG.BUCKET_NAME}, Key: {filename}')
        try:
            client = storage.Client()
            bucket = client.get_bucket(CONFIG.BUCKET_NAME)
            blob = bucket.blob(filename)

            if not blob.exists():
                raise FileNotFoundError(f"Blob {filename} does not exist in bucket {CONFIG.BUCKET_NAME}.")

            # Attempt to get the last update timestamp
            if blob.updated:
                last_update = blob.updated.strftime('%Y-%m-%d %H:%M:%S UTC')
            else:
                logging.warning(f"[GCP] -> No 'updated' timestamp available for blob: {filename}")
                last_update = "Unknown"

            if file_type == 'json':
                data = json.loads(blob.download_as_text())
            else:
                csv_content = blob.download_as_text()
                data = pd.read_csv(StringIO(csv_content))

        except Exception as e:
            logging.warning(f'[+] Failed to load file from GCP bucket: {e}')
        else:
            logging.info(f'[+] Data file ({filename}) successfully loaded from GCP!')
            return data, last_update

    raise RuntimeError(
        f"Invalid CONFIG detected. CONFIG must be an instance of either LocalConfig or GCPConfig. "
        f"Current CONFIG: {type(CONFIG).__name__}"
    )

