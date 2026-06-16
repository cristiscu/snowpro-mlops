from snowflake.ml.feature_store import FeatureStore, CreationMode

fs = FeatureStore(
   session=session,
   database="MY_DB",
   name="MY_FEATURE_STORE",
   default_warehouse="MY_WH",
   [creation_mode=CreationMode.CREATE/FAIL_IF_NOT_EXIST])
