"""Get all Daily Prices

This script contains the functions making calls to the EIA API and \
populating the CSV file located in natural_gas_prices/data/daily_prices.csv \
with this data.
"""
import os
import requests
import json
import csv

def get_data_list(api_key=None):
    """
    Makes an API call to the EIA API and returns a list of the daily prices.

    ### PARAMETERS
    #### api_key : str, optional
    The API key to use if no API_KEY is exported, if a value is found under \
    the `EIA_API_KEY` key, this value would take precedence over the \
    `api_key` parameter.
    """

    # Get the EIA API key from the environment variables
    # Register at https://www.eia.gov/opendata/register.php to get an API_KEY
    # Export the API_KEY to the environment using the key "EIA_API_KEY"
    API_KEY = os.getenv("EIA_API_KEY", api_key)

    # URL to get daily natural gas prices from EIA API
    URL = "https://api.eia.gov/series/?api_key={}&series_id=NG.RNGWHHD.D".format(
        API_KEY
    )

    # Make the request using the python requests library and the the API response
    # Get the response json data as a Python dictionary and store it in the
    # eia_data variable
    eia_data = json.loads(requests.get(URL).content)

    # Get the list of days and the corrsponding price in $ per million BTU
    data_list = eia_data.get("series")[0].get("data")

    # Sort the list of data to have the oldest dates first.
    # since the dates are returned in the format "20010330" which is yyyymmdd, then
    # the smaller the number the older the date
    data_list.sort(key=lambda e : e[0])

    return data_list

def populate_csv_file(filepath, data_list, header_list=None, write_mode='w',):
    """
    Writes data to a CSV file.

    ### PARAMETERS
    #### filepath : str
    The path relative to the project root directory of the CSV file

    ### data_list : list
    Python list of lists where each list represents a row and it's columns

    #### header_list : list, optional
    Python list of the headers for the CSV file. if nothing is passed or a \
    wrong data type is passed, no header row would be added.

    #### write_mode : str, optional
    Options are `w` which overrides the content of the CSV file, or `a` \
    which appends a the new data_list as rows to the CSV file.
    """
    # Open connection to the CSV file
    # The assumption is that this script will be run from the project root
    # directory
    with open( filepath, mode=write_mode, newline=''
        ) as file_to_write:

        # Instantiate CSV writer
        data_writer = csv.writer(
            file_to_write,
            delimiter=',',
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL
        )

        if type(header_list) == list:
            # Add the column names to the first row
            data_writer.writerow(header_list)

        # Write the data to the csv file per row
        for row in data_list:
            data_writer.writerow(row)

# Run the functions
data_list = get_data_list()
populate_csv_file(
    filepath='natural_gas_prices/data/daily_prices.csv',
    header_list=["Date", "Price"],
    data_list=data_list
)
