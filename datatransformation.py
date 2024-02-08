import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

def camel_to_snake(name):
    import re
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

@transformer
def transform(data, *args, **kwargs):
    # Remove rows where passenger count is equal to 0 and trip distance is equal to 0
    data = data[(data['passenger_count'] > 0) & (data['trip_distance'] > 0)]
    

    columns_to_rename = sum(1 for col in data.columns if col != camel_to_snake(col))
    print("Number of columns to be renamed to snake case:", columns_to_rename)
    existing_vendor_ids = data['VendorID'].unique()
    print(existing_vendor_ids)



    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date
    data['lpep_pickup_datetime'] = data['lpep_pickup_datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
    data['lpep_dropoff_datetime'] = data['lpep_dropoff_datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
    data['lpep_pickup_date'] = pd.to_datetime(data['lpep_pickup_date']).dt.strftime('%Y-%m-%d')
    # Rename columns from camel case to snake case
    data = data.rename(columns={col: camel_to_snake(col) for col in data.columns})

    columns_to_rename = sum(1 for col in data.columns if col != camel_to_snake(col))


    # Create a new column 'lpep_pickup_date' by converting 'lpep_pickup_datetime' to date
    # data['lpep_pickup_date'] = pd.to_datetime(data['lpep_pickup_datetime']).dt.date



    return data 

@test
def test_output(output, *args):
    # Assertion 1: Check that there are no records with 0 passenger count
    assert (output['passenger_count'] == 0).sum() == 0, 'There are rides with zero passengers'

    # Assertion 2: Check that passenger count is greater than 0
    assert (output['passenger_count'] > 0).all(), 'There are records with passenger count <= 0'

    # Assertion 3: Check that trip distance is greater than 0
    assert (output['trip_distance'] > 0).all(), 'There are records with trip distance <= 0'
