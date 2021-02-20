# Datopian Data Wrangling Exercise
 Scripts to normalize data and return a CSV. All CSVs here use a comma `,` as the delimiter.

## Using with this project
To use this project locally you must have [python](https://www.python.org/downloads/) installed.

1. **Clone the repository:**
    ```sh
    git clone -b main https://github.com/cynepton/data_wrangling_exercise.git
    ```
2. **Setup the virtual environment by running:**
    ```sh
    virtualenv env
    source env/Scripts/activate # for windows
    source env/bin/activate # for MacOs
    ```
    in the project root folder.
3. **Install External Dependencies:**
    ```sh
    pip install -r requirements.txt
    ```
4. **Export the EIA API key to the environment**

### EIA API key 🔑
The API call is made to `https://api.eia.gov/series/?api_key=YOUR_API_KEY&series_id=NG.RNGWHHD.D` as **GET** request. Make sure to replace `YOUR_API_KEY` with your personalised actual EIA API key. If you don't have a key, register [here](https://www.eia.gov/opendata/register.php), fill in your email and a key would be sent to your email address in less than a minute.

Export this key into the environment using:
```sh
set EIA_API_KEY=<YOUR_API_KEY>
```
or
```sh
export EIA_API_KEY=<YOUR_API_KEY>
```

## Scripts

### Get Natural Gas Prices 📆 ⛽ 💵
Located at [natural_gas_prices/get_daily_prices.py](natural_gas_prices/get_ng_prices.py), this script uses the [EIA API](http://www.eia.gov/developer) to get the **Henry Hub Natural Gas Spot Prices** in *Dollars per Million Btu*.

There are 2 functions in the [script](natural_gas_prices/get_ng_prices.py), the `get_data_list` and the `populate_csv_file`.<br>
- The **`get_data_list`** function takes the `duration type`, and returns a python list of the dates and their prices for that date. This can be used when the data needs to be further processed before exporting the data.
- The **`populate_csv_file`** function takes the `duration type` and automatically calls the API, gets the data list and populates it to CSV files located in the [data folder 📂](natural_gas_prices/data).

>For daily prices, the `date` is the actual day in the format `yyyymmdd`.<br> For weekly prices, the `date` is the friday ending close of business for that week in the date format `yyyymmdd`.<br> For Monthly prices, the `date` is in the format `yyyymm`.<br> For annual prices the `date` is in the format `yyyy`.

The `response` gotten from EIA is a `json` in the format:
```py
{
    'request': {
        'command': 'series',
        'series_id': 'NG.RNGWHHD.D'
    },
    'series': [
        {
            'series_id': 'NG.RNGWHHD.D',
            'name': 'Henry Hub Natural Gas Spot Price, Daily',
            'units': 'Dollars per Million Btu',
            'f': 'D',
            'unitsshort': '$/MMBTU',
            'description': 'Henry Hub Natural Gas Spot Price',
            'copyright': 'Thomson-Reuters',
            'source': 'Thomson-Reuters',
            'start': '19970107',
            'end': '20210217',
            'updated': '2021-02-18T13:10:27-0500',
            'data': [
                ['20210217', 23.86],
                ['20210216', 11.32]
            ]
        }
    ]
}
```

This script specifically takes the `data` list within the first dictionary item in the series list. The data item contains a list of the dates in the format `yyyymmdd` and their prices, this script then writes them to a CSV file.
