# Space Exploration App

## Overview

Space Exploration is a Python-based Dash application designed to provide real-time information on space exploration. The application is deployed on Google Cloud Run and updates its data daily through web scraping techniques. It offers a comprehensive view of space activities, from historical milestones to upcoming launches. The design is fully responsive, adapting to various screen sizes.

You can access the live version of the application [here](https://spacexploration-2t723npiha-uc.a.run.app/).

## Features

### Home Page

- **3D Earth Globe**: A rotating 3D Earth globe visualizing the number of space launches by country since the inception of space exploration.

### Historical Events Page

- **Cytoscape Graph**: A constellation-shaped graph representing significant historical events in space exploration. Clicking on a node reveals a description and image related to the event.

### Space Dashboard

- **Line Plot**: Displays the number of launches per year, with the ability to filter by success or failure.
- **Histogram**: Shows launches by month, updating based on the year selected from the line plot.
- **Sunburst Chart**: Represents hierarchical data from countries, organizations, down to success/failure rates.
- **Upcoming Launch Info**: A section providing details on the next upcoming launch.

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
- **Cloud Deployment**: The application is deployed on Google Cloud Run and utilizes Docker containers for daily data updates.

## Installation

To run the application locally, follow these steps:

1. Clone the repository
2. Install the required packages from `requirements.txt`
3. Run `app.py`

## Updating Data

The application is designed to update its data sources daily. The data is updated using Docker containers orchestrated by Google Cloud Run. If you wish to update the data manually, you can run the scraping scripts located in the linked repositories.

## License

This project is licensed under the Apache-2.0 License. You are free to use, modify, and distribute the code, provided that you attribute the work to the original author.

## Copyright

© 2023 Tanguy Surowiec. All rights reserved.
