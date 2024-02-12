import io
import pandas as pd
import requests
from io import BytesIO
import warnings
import os 

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    parquet_dfs = {}

    # Suppress warnings temporarily
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        
        months = [f'{i:02}' for i in range(1, 13)]
        output = pd.DataFrame()

        taxi_dtypes = {
        'VendorID': pd.Int64Dtype(),
        'store_and_fwd_flag': str,
        'RatecodeID': pd.Int64Dtype(),
        'PULocationID': pd.Int64Dtype(),
        'DOLocationID': pd.Int64Dtype(),
        'passenger_count': pd.Int64Dtype(),
        'trip_distance': float,
        'fare_amount': float,
        'extra': float,
        'mta_tax': float,
        'tip_amount': float,
        'tolls_amount': float,
        'ehail_fee': str,
        'improvement_surcharge': float,
        'total_amount': float,
        'payment_type': pd.Int64Dtype(),
        'trip_type': pd.Int64Dtype(),
        'congestion_surcharge': float,
        'lpep_pickup_datetime' :'datetime64[ns]',
        'lpep_dropoff_datetime':'datetime64[ns]'
        }
        parse_dates = ['lpep_pickup_datetime', 'lpep_dropoff_datetime']

        for mon in months: 
            url = f'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022-{mon}.parquet'
            df = pd.read_parquet(url,)
            
            output = pd.concat([output, df], ignore_index=True)
            print(mon, df.shape, "full:", output.shape)
            

    return output


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
