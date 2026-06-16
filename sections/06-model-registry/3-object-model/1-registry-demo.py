from snowflake.ml.registry import Registry
from snowflake.ml.model import task, type_hints

reg = Registry(
   session=sp_session, 
   database_name="ML", 
   schema_name="REGISTRY")

mv = reg.log_model(clf,
   model_name="my_model",
   version_name="v1",
   conda_dependencies=["scikit-learn"],
   comment="My awesome ML model",
   metrics={"score": 96},
   sample_input_data=train_features,
   task=task.Task.TABULAR_BINARY_CLASSIFICATION)

# LIST 'snow://model/my_model/versions/V3/';
session.file.get(
   'snow://model/my_model/versions/V3/MANIFEST.yml',
   'model_artifacts')

model_df = reg.show_models()
model_list = reg.models()

reg.delete_model("mymodel")

# -----------------------------------------------------------
m = reg.get_model("MyModel")

print(m.comment)
m.comment = "A better description than the one I provided originally"

print(m.show_tags())
m.set_tag("live_version", "v1")
m.get_tag("live_version")
m.unset_tag("live_version")
m.rename("MY_MODEL_TOO")

version_list = m.versions()
version_df = m.show_versions()
m.delete_version("rc1")

default_version = m.default
m.default = "v2"

mv = m.version("v1")
mv = m.default

print(mv.comment)
print(mv.description)

mv.comment = "A model version comment"
mv.description = "Same as setting the comment"

# -----------------------------------------------------------
remote_prediction = mv.run(
   test_features, 
   function_name="predict")
remote_prediction.show()
