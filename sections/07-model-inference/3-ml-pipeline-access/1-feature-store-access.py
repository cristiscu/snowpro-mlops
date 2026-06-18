from snowflake.ml.feature_store import setup_feature_store

setup_feature_store(
    session=session,
    database="<FS_DATABASE_NAME>",
    schema="<FS_SCHEMA_NAME>",
    warehouse="<FS_WAREHOUSE>",
    producer_role="<FS_PRODUCER_ROLE>",
    consumer_role="<FS_CONSUMER_ROLE>")
    