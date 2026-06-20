# Using callbacks with ExperimentTracking [Template]
# https://docs.snowflake.com/en/developer-guide/snowflake-ml/experiments

# ----------------------------------------------------------
# LightGBM

from snowflake.ml.experiment.callback.lightgbm import SnowflakeLightgbmCallback
from snowflake.ml.model.model_signature import infer_signature
callback = SnowflakeLightgbmCallback(
    exp, model_name="name", model_signature=infer_signature(X, y))

from lightgbm import LGBMClassifier
model = LGBMClassifier()
with exp.start_run("my_run"):
    model.fit(X, y, eval_set=[(X, y)], callbacks=[callback])

# ----------------------------------------------------------
# Keras

from snowflake.ml.experiment.callback.keras import SnowflakeKerasCallback
from snowflake.ml.model.model_signature import infer_signature
callback = SnowflakeKerasCallback(
    exp, model_name="name", model_signature=infer_signature(X, y))

import keras
model = keras.Sequential()
model.add(keras.layers.Dense(1))
model.compile(
    optimizer=keras.optimizers.RMSprop(learning_rate=0.1),
    loss="mean_squared_error",
    metrics=["mean_absolute_error"])
with exp.start_run("my_run"):
    model.fit(X, y, validation_split=0.5, callbacks=[callback])
