# DataConnector
DataConnector.from_dataframe(sess.table("…"))       # dc (DataConnector)
DataConnector.from_dataset(ds)                      # dc (DataConnector)
dc.to_pandas()                                      # pandas dataframe
ShardedDataConnector.from_dataframe(df)             # sdc (w/ Snowflake PyTorch)

# ---------------------------------------------------------
# DataSource API
ds = SFStageParquetDataSource(
   stage_location="@stage/path/", 
   database="…", schema="…", file_pattern='*.parquet')

ray_ds = ray.data.read_datasource(ds)
dc = DataConnector.from_ray_dataset(ray_ds)

# ---------------------------------------------------------
# DataSink
dsink = SnowflakeTableDatasink(
   table_name="…", database="…", schema="…",
   auto_create_table=True, override=True)

transf_ds = ray_ds.map_batches(ex_transf_batch_function)
transf_ds.write_datasink(dsink)
