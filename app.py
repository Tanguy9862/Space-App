import dash
import logging
from dash import html
from wikipedia_space_scraper.scraper import scrape_wikipedia_data
from next_launch_scraper.scraper import scrape_next_launch_data
from past_launches_scraper.scraper import scrape_past_launches_data
from assets.footer import footer
from pages.nav import navbar

logging.basicConfig(filename='app.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

app = dash.Dash(
    __name__,
    use_pages=True,
    update_title=False,
    suppress_callback_exceptions=True,
    prevent_initial_callbacks=True,
)

app.layout = html.Div(
    [
        navbar(),
        dash.page_container,
        footer
    ],
)

if __name__ == "__main__":
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

    app.run_server(debug=False)
