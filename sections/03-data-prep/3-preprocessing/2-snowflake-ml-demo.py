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
