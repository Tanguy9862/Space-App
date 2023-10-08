# Space Exploration

## Overview

Space Exploration is a Python-based Dash application designed to provide real-time insights into space exploration. The application is deployed on a web server and updates its data daily through web scraping techniques. It offers a comprehensive view of space activities, from historical milestones to upcoming launches. The design is fully responsive, adapting to various screen sizes.

## Features

### Home Page

- **3D Earth Globe**: A rotating 3D globe that visualizes the number of space launches by country since the beginning of space exploration.

### Historical Events Page

- **Cytoscape Graph**: A constellation-like graph that represents significant historical events in space exploration. Clicking on a node reveals a description and an image related to the event.

### Space Dashboard

- **Line Plot**: Displays the number of launches per year, with the ability to filter by success or failure.
- **Histogram**: Shows launches by month, which updates based on the selected year from the line plot.
- **Sunburst Chart**: Represents hierarchical data starting from countries, to organizations, to success/failure rates.
- **Upcoming Launch Info**: A section that provides details about the next upcoming launch.

## Technologies Used

- **Python**: The backend is entirely written in Python.
- **Dash**: Used for creating the web application.
- **Web Scraping**: Data is scraped from various sources using Python libraries like `requests` and `BeautifulSoup`. The scraping scripts are hosted in separate repositories:
  - [Wikipedia Space Scraper](https://github.com/Tanguy9862/Wikipedia_Space_Scraper)
  - [Next Launch Scraper](https://github.com/Tanguy9862/Next-Launch-Scraper)
  - [NextSpaceFlight Scraper](https://github.com/Tanguy9862/NextSpaceFlight-Scrapper)
- **Data Management**: Scraping scripts are packaged as reusable Python modules.
- **Data Visualization**: Utilizes Dash components and Plotly for interactive visualizations.
- **Responsive Design**: The application is designed to be fully responsive.

## Installation

To run this project locally, follow these steps:

1. Clone the repository
2. Install the required packages: `pip install -r requirements.txt`
3. Run `app.py`

## Updating Data

The application is designed to update its data sources daily. If you wish to update the data manually, you can run the scraping scripts located in the linked repositories.

## License

MIT License
