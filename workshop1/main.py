import dlt
import duckdb
from people import people_1, people_2
generators_pipeline = dlt.pipeline(destination='duckdb', dataset_name='homework')

info = generators_pipeline.run(people_1(),table_name="people1",write_disposition="replace")
info = generators_pipeline.run(people_2(),table_name="people2",write_disposition="replace")

info = generators_pipeline.run(people_1(),table_name="people_append",write_disposition="replace")
info = generators_pipeline.run(people_2(),table_name="people_append",write_disposition="append")

info = generators_pipeline.run(people_1(),table_name="people_merge",write_disposition="replace")
info = generators_pipeline.run(people_2(),table_name="people_merge",write_disposition="merge",primary_key="ID")


# the outcome metadata is returned by the load and we can inspect it by printing it.
print(info)
conn = duckdb.connect(f"{generators_pipeline.pipeline_name}.duckdb")

# let's see the tables
conn.sql(f"SET search_path = '{generators_pipeline.dataset_name}'")
print('Loaded tables: ')


def show_table(table_name):
    table = conn.sql(f"SELECT * FROM {table_name}")
    return table

show_table("people1")
show_table("people2")
people_append=show_table("people_append").df()
people_merge=show_table("people_merge").df()

print (f"Sum of Ages {people_append['age'].sum()}")
# Sum of Ages 353
print (f"Sum of Ages {people_merge['age'].sum()}")
# Sum of Ages 266