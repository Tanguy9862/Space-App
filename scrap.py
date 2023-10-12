import logging
from datetime import datetime
from flask import Flask, jsonify
from wikipedia_space_scraper.scraper import scrape_wikipedia_data
from next_launch_scraper.scraper import scrape_next_launch_data
from past_launches_scraper.scraper import scrape_past_launches_data
from google.cloud import storage
from utils.cloud_storage import write_json_to_gcs

app = Flask(__name__)


@app.route('/scrape', methods=['GET'])
def scrape():
    logging.basicConfig(filename='app.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        scrape_wikipedia_data()
        write_json_to_gcs('next_launch_data.json', scrape_next_launch_data())
        scrape_past_launches_data()

        # Upload date_update.txt on google cloud storage:
        current_utc_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
        storage_client = storage.Client()
        bucket = storage_client.get_bucket('spacexploration_data')
        blob = bucket.get_blob('date_update.txt')
        blob.upload_from_string(current_utc_time)

        return jsonify({"status": "success", "message": "Scraping completed"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
