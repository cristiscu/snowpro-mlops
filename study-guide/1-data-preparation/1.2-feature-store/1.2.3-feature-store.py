from snowflake.snowpark import Session
from snowflake.ml.feature_store import FeatureStore, CreationMode, Entity, FeatureView

# -------------------------------------------------------
# 2. Initialize the Feature Store Connection

# Create your Snowpark session context
session = Session.builder.config("connection_name", "my_snowflake_conn").create()

# Initialize or connect to the feature store schema
fs = FeatureStore(
    name="prod_feature_store",
    session=session,
    database="ml_db",
    default_warehouse="compute_wh",
    [creation_mode=CreationMode.CREATE/FAIL_IF_NOT_EXIST])

# -------------------------------------------------------
# 3. Define Entities

# Register the primary subscriber entity 
user_entity = Entity(name="USER_ID", join_keys=["USER_ID"])
fs.register_entity(user_entity)

# -------------------------------------------------------
# 4. Create and Register Feature Views

# Define the transformation pipeline on raw event logs
raw_df = session.table("raw_data.user_events")
feature_df = raw_df.group_by("USER_ID").agg({
    "EVENT_TIMESTAMP": "max", 
    "CLICK": "sum"
}).select_expr(
    "USER_ID",
    "max(EVENT_TIMESTAMP) as LAST_ACTIVE_TIME",
    "sum(CLICK) as TOTAL_CLICKS")

# Bundle query logic into an explicitly versioned view
user_activity_fv = FeatureView(
    name="user_activity_features",
    entities=[user_entity],
    query=feature_df,
    timestamp_col="LAST_ACTIVE_TIME",
    refresh_freq="1h", # Automatically spins up an incremental Snowflake Dynamic Table
    version="v1")

# Save pipeline permanently into the repository
fs.register_feature_view(feature_view=user_activity_fv)

# -------------------------------------------------------
# 5. Generate Point-in-Time Training Data

# A baseline label dataset containing historical events
spine_df = session.table("ml_db.labels.user_conversions") 

# Read registered view back from the centralized catalog
fv = fs.get_feature_view(name="user_activity_features", version="v1")

# Snapshot training data safely with point-in-time exact matching
training_dataset = fs.generate_dataset(
    spine_df=spine_df,
    features=[fv],
    spine_timestamp_col="CONVERSION_TIME")

# -------------------------------------------------------
# 6. Transition to Low-Latency Online Serving

# Spin up online serving for real-time model inference
fs.create_online_store(
    online_store_name="prod_online_store",
    storage_type="snowflake_low_latency")

# Sync the specific view pipelines out to production infrastructure
fs.resume_online_store_sync(
    online_store_name="prod_online_store",
    feature_view_name="user_activity_features",
    version="v1")
