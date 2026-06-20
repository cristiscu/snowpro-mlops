# OSS preprocessing

import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

data = pd.DataFrame({
    'age': [34, 23, 54, 31],
    'city': ['SF', 'NY', 'SF', 'LA'],
    'income': [120000, 95000, 135000, 99000]
})

pipeline = Pipeline(steps=[
   ('preprocessor', ColumnTransformer(transformers=[
      ('scaler', StandardScaler(), ['age', 'income']),
      ('encoder', OneHotEncoder(), ['city'])]))
])
result = pipeline.fit_transform(data)
print(result)

# ------------------------------------------------------
# Snowflake ML preprocessors

from snowflake.snowpark import Session
from snowflake.ml.modeling.preprocessing import StandardScaler
from snowflake.ml.modeling.preprocessing import OneHotEncoder
from snowflake.ml.modeling.pipeline import Pipeline

session = Session.builder.configs(...).create()
df = session.table('CUSTOMER_DATA')

pipeline = Pipeline(steps=[
   ('scaling', StandardScaler(
      input_cols=['AGE', 'INCOME'],
      output_cols = ['AGE_SCALED', 'INCOME_SCALED'])), 
   ('encoding', OneHotEncoder(
      input_cols=['CITY'], 
      output_cols=['CITY_ENCODED']))
])
result = pipeline.fit_transform(df)
result.show()

# ------------------------------------------------------
# Ray map_batches

import ray
from snowflake.ml.ray.datasource.stage_parquet_file_datasource import SFStageParquetDataSource
from snowflake.ml.data.data_connector import DataConnector

def preprocess_batch(batch: pd.DataFrame) -> pd.DataFrame:
   batch['AGE_SCALED'] = (batch['age'] - batch['age'].mean()) / batch['age'].std()
   return batch

def filter_by_value(row):
    return row['city'] != 'LA'

ray_ds = ray.data.read_datasource(data_source)
filtered_ds = ray_ds.filter(filter_by_value)
transformed_ds = filtered_ds.map_batches(process_batch)
data_connector = DataConnector.from_ray_dataset(transformed_ds)
