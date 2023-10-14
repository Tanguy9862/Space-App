import pandas as pd
from iso3166 import countries
from numpy import where

# PANDAS CONFIGURATION:
# pd.options.display.float_format = '{:,.2f}'.format
# pd.set_option('display.max_columns', None)


def clean_past_launches_data(df):
    df['Country'] = df.Location.str.rsplit(',').str[-1].str.strip()
    df.loc[(df.Country == "Russia"), "Country"] = "Russian Federation"
    df.loc[(df.Country == "New Mexico"), "Country"] = "USA"
    df.loc[(df.Country == "Yellow Sea"), "Country"] = "China"
    df.loc[(df.Country == "Shahrud Missile Test Site"), "Country"] = "Iran"
    df.loc[(df.Country == "Pacific Missile Range Facility"), "Country"] = "USA"
    df.loc[(df.Country == "Barents Sea"), "Country"] = "Russian Federation"
    df.loc[(df.Country == "Gran Canaria"), "Country"] = "USA"

    def get_country_name(x):
        if x != "IRN" and x != "PRK":
            try:
                return countries.get(x).alpha3
            except KeyError:
                return 'Unknown'
        else:
            return x

    df['country_code'] = df.Country.apply(lambda x: get_country_name(x))
    df.loc[df['Country'] == 'Iran', 'country_code'] = 'IRN'
    df.loc[df['Country'] == 'North Korea', 'country_code'] = 'PRK'

    # PRICE COL FORMAT:
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

    # MISSION_STATUS_BINARY:
    df['Mission_Status_Binary'] = where(df.Mission_Status != "Success", "Failure", "Success")

    # YEAR_LAUNCH:
    df['YEAR_LAUNCH'] = pd.DatetimeIndex(df['Date']).year

    return df
