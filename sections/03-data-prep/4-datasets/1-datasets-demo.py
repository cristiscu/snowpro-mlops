ds1 = dataset.create_from_dataframe(sess, "myds", "v1", input_dataframe=df)
print(ds1.selected_version)
print(ds1.list_versions())
ds2 = ds1.create_version("v2", df)

ds_df = ds1.read.to_snowpark_dataframe()
tf_dataset = ds1.read.to_tf_dataset(batch_size=32)
pt_datapipe = ds1.read.to_torch_datapipe(batch_size=32)

import pyarrow.parquet as pq
pd_ds = pq.ParquetDataset(
   ds1.read.files(), filesystem=ds1.read.filesystem())

import dask.dataframe as dd
dd_df = dd.read_parquet(
   ds1.read.files(), filesystem=ds1.read.filesystem())
