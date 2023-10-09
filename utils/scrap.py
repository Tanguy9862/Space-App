import datetime as dt
import logging
import config
from wikipedia_space_scraper.scraper import scrape_wikipedia_data
from next_launch_scraper.scraper import scrape_next_launch_data
from past_launches_scraper.scraper import scrape_past_launches_data


def main():
    config.DATE_UPDATE = dt.datetime.now().strftime('%Y-%m-%d %H:%M')
    logging.basicConfig(filename='app.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

    # fn à faire + boucle

    try:
        scrape_wikipedia_data()
    except Exception as e:
        logging.error(f"Error while scraping Wikipedia data: {e}")

    try:
        scrape_next_launch_data()
    except Exception as e:
        logging.error(f"Error while scraping next launch data: {e}")

    try:
        scrape_past_launches_data()
    except Exception as e:
        logging.error(f"Error while scraping past launches data: {e}")


if __name__ == '__main__':
    main()
