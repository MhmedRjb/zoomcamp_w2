if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    pu_locs = data['PULocationID']
# CHECK MEMORY USAGE 
    memory_usage = pu_locs.memory_usage(deep=True) / (1024 ** 2)  # Convert to megabytes
    print(f"Memory usage of DataFrame: {memory_usage:.2f} MB")
    print (data.info())
    zerofareamount=data[data['fare_amount'] == 0].shape
    print (f"fare_amount of 0 is {zerofareamount}")
    print (data.info())



    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
