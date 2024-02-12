import io
import pandas as pd
import requests
from io import BytesIO
import warnings
import os 
parquet_dfs = {}

# Suppress warnings temporarily
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    
    months = [f'{i:02}' for i in range(1, 13)]
    output = pd.DataFrame()

    for mon in months: 
        url = f'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022-{mon}.parquet'
        df = pd.read_parquet(url)
        
        output = pd.concat([output, df], ignore_index=True)
        print(mon, df.shape, "full:", output.shape)
        output.to_parquet("gree_taxi_2022.parquet")
