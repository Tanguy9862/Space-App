import pandas as pd
from iso3166 import countries
from numpy import where

# DATA:
pd.options.display.float_format = '{:,.2f}'.format
pd.set_option('display.max_columns', None)

# df = pd.read_csv('assets/data/past_launches_data.csv').drop(['Unnamed: 0.1', 'Unnamed: 0'], axis=1)
df = pd.read_csv('data/past_launches_data.csv')
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
# df['Price'] = df['Price'].str.replace(',', '.')
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

# MISSION_STATUS_BINARY:
df['Mission_Status_Binary'] = where(df.Mission_Status != "Success", "Failure", "Success")
