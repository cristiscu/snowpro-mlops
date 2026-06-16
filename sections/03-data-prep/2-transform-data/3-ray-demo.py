import ray
from snowflake.ml.ray.datasource.stage_parquet_file_datasource import SFStageParquetDataSource
from snowflake.ml.data.data_connector import DataConnector

def preprocess_batch(batch: pd.DataFrame) -> pd.DataFrame:
   batch['AGE_SCALED'] = (batch['age'] - batch['age'].mean())
      / batch['age'].std()
   return batch

def filter_by_value(row):
    return row['city'] != 'LA'

ray_ds = ray.data.read_datasource(data_source)
filtered_ds = ray_ds.filter(filter_by_value)
transformed_ds = filtered_ds.map_batches(process_batch)
data_connector = DataConnector.from_ray_dataset(transformed_ds)
