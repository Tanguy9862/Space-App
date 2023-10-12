from google.cloud import storage
import json
import os

BUCKET_NAME = 'spacexploration_data'


def read_from_gcs(blob_name):
    if os.path.exists('spacexploration-keys.json'):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'spacexploration-keys.json'
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    return bucket.blob(blob_name)


def write_json_to_gcs(blob_name, new_data):
    blob = read_from_gcs(blob_name)
    json_str = json.dumps(new_data)
    blob.upload_from_string(json_str, content_type='application/json')



