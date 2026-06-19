# OSS preprocessing

import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

df = pd.DataFrame({
    'age': [34, 23, 54, 31],
    'city': ['SF', 'NY', 'SF', 'LA'],
    'income': [120000, 95000, 135000, 99000]})

numeric_features = ['age', 'income']
numeric_transformer = StandardScaler()
categorical_features = ['city']
categorical_transformer = OneHotEncoder()

preprocessor = ColumnTransformer(transformers=[
   ('num', numeric_transformer, numeric_features),
   ('cat', categorical_transformer, categorical_features)])

pipeline = Pipeline(steps=[('preprocessor', preprocessor)])
X_processed = pipeline.fit_transform(df)
print(X_processed)

# ------------------------------------------------------
# Snowflake ML preprocessors

from snowflake.snowpark import Session
from snowflake.ml.modeling.preprocessing import StandardScaler
from snowflake.ml.modeling.preprocessing import OneHotEncoder
from snowflake.ml.modeling.pipeline import Pipeline

session = Session.builder.configs(...).create()

df = session.table('CUSTOMER_DATA')

scaler = StandardScaler(
   input_cols=['AGE', 'INCOME'],
   output_cols = ['AGE_SCALED', 'INCOME_SCALED'])
encoder = OneHotEncoder(
   input_cols=['CITY'], 
   output_cols=['CITY_ENCODED'])

pipeline = Pipeline(steps=[('scaling', scaler), ('encoding', encoder)])
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
