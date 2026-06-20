from snowflake.ml.registry import Registry
from snowflake.ml.dataset import Dataset

from snowflake import snowpark
from snowflake.ml import dataset

df = session.sql(
    "select uniform(0, 10, random(1)) as x, uniform(0, 10, random(2)) as y from table(generator(rowcount => 100))"
)

from snowflake.snowpark.context import get_active_session
session = get_active_session()

from snowflake.ml.dataset import Dataset

# Materialize DataFrame contents into a Dataset
ds1 = Dataset.create_from_dataframe(session, "my_dataset", "version1", input_dataframe=df)

# 1. Load the specific version of your dataset
dataset = Dataset.get_dataset(
    session=session, name="customer_churn_dataset", version="v1_2_0")

# 2. Convert to a Snowpark DataFrame for the registry
dataset_df = dataset.read.to_snowpark_dataframe()

# 3. Log the model with sample input data to establish lineage
registry = Registry(session=session)
registry.log_model(
    model=my_model,
    model_name="customer_churn_model",
    version="v1.0.0",
    sample_input_data=dataset_df)