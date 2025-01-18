from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))


class BaseConfig:
    FILENAME_MAPPING = {
        'HISTORICAL_FACTS_FILENAME': 'historical_facts_data.json',
        'PAST_LAUNCHES_FILENAME': 'nsf_past_launches.csv',
        'NEXT_LAUNCH_FILENAME': 'nsf_next_launch.json'
    }


class LocalConfig(BaseConfig):
    DATA_DIR_NAME = 'data'


class LambdaConfig(BaseConfig):
    BUCKET_NAME = "app-space-exploration-bucket"


ENV = os.getenv("ENV", "local")
CONFIG = LocalConfig() if ENV == "local" else LambdaConfig()
