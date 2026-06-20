# Logging a PyCaret Model (pycaret_model.pkl) [Template]
# https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/bring-your-own-model-types#example-logging-a-pycaret-model

# create custom model class + instance
from pycaret.classification import load_model, predict_model

class PyCaretModel(custom_model.CustomModel):
    def __init__(self, context: custom_model.ModelContext) -> None:
        super().__init__(context)
        model_dir = self.context["model_file"][:-4]  # Remove '.pkl' suffix
        self.model = load_model(model_dir, verbose=False)
        self.model.memory = '/tmp/'  # Update memory directory

    @custom_model.inference_api
    def predict(self, X: pd.DataFrame) -> pd.DataFrame:
        model_output = predict_model(self.model, data=X)
        return pd.DataFrame({
            "prediction_label": model_output['prediction_label'],
            "prediction_score": model_output['prediction_score']})

my_pycaret_model = PyCaretModel(
    custom_model.ModelContext(model_file='pycaret_model.pkl'))

# --------------------------------------------------
# make predictions w/ the local model

test_data = [[1, 237, 1, 1.75, 1.99, 0.00, 0.00, 0, 0, 0.5, 1.99, 1.75, 0.24, 'No', 0.0, 0.0, 0.24, 1], ...]
col_names = [
    'Id', 'WeekofPurchase', 'StoreID', 'PriceCH', 'PriceMM', 'DiscCH', 'DiscMM',
    'SpecialCH', 'SpecialMM', 'LoyalCH', 'SalePriceMM', 'SalePriceCH',
    'PriceDiff', 'Store7', 'PctDiscMM', 'PctDiscCH', 'ListPriceDiff', 'STORE']
test_df = pd.DataFrame(test_data, columns=col_names)
output_df = my_pycaret_model.predict(test_df)

# --------------------------------------------------
# log the model (w/ a model signature) + predict again

predict_signature = model_signature.infer_signature(
    input_data=test_df,
    output_data=output_df)

snowml_registry = Registry(session)
custom_mv = snowml_registry.log_model(
    my_pycaret_model,
    model_name="my_pycaret_model",
    version_name="version_1",
    conda_dependencies=["pycaret==3.0.2", "scipy==1.11.4", "joblib==1.2.0"],
    options={"relax_version": False},
    signatures={"predict": predict_signature},
    comment = 'My PyCaret classification experiment using the CustomModel API')

snowml_registry.show_models()

snowpark_df = session.create_dataframe(test_data, schema=col_nms)
custom_mv.run(snowpark_df).show()

# SQL predictions:
# ---------------
# SELECT my_pycaret_model!predict(*) AS predict_dict,
#    predict_dict['prediction_label']::text AS prediction_label,
#    predict_dict['prediction_score']::double AS prediction_score
# from pycaret_input_data;