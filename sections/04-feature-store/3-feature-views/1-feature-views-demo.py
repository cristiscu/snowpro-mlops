from snowflake.ml.feature_store import FeatureView

managed_fv = FeatureView(
    name="MY_MANAGED_FV",
    entities=[entity],
    feature_df=my_df, 			# DataFrame w/ feature transfs
    [timestamp_col="ts"], 		# col name in the dataframe
    refresh_freq="5 minutes",
    [desc="my managed feature view"])

external_fv = FeatureView(
    name="MY_EXTERNAL_FV",
    entities=[entity],
    feature_df=my_df, 			# DataFrame for feature table
    [timestamp_col="ts"], 		# col name in the dataframe
    refresh_freq=None, 			# None for external!
    [desc="my external feature view"])

external_fv = external_fv.attach_feature_desc({
    "SENDERID": "Sender account ID for the transaction",
    "RECEIVERID": "Receiver account ID for the transaction",
    "IBAN": "International Bank Identifier for the receiver bank",
    "AMOUNT": "Amount of the transaction"})

registered_fv: FeatureView = fs.register_feature_view(
    feature_view=managed/external_fv,
    version="1",
    block=True, 				# until init data available
    overwrite=False) 			# replace existing

retrieved_fv: FeatureView = fs.get_feature_view(
    name="MY_MANAGED_FV", version="1")

fs.list_feature_views(
    [entity_name="<entity_name>"],
    [feature_view_name="<feature_view_name>"]
).show()

fs.update_feature_view(name="<name>", version="<version>",
    [refresh_freq="<new_fresh_freq>"],
    [warehouse="<new_warehouse>"],
    [desc="<new_description>"])

fs.delete_feature_view(feature_view="<name>", version="<version>")
