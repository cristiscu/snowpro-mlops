from snowflake.ml.modeling import tune

# configure the tunner
tuner_config = tune.TunerConfig(
   metric="accuracy",
   mode="max",
   search_alg=search.GridSearch(),   # alt: BayesOpt() / RandomSearch()
   num_trials=5,
   max_concurrent_trials=1)

# get the HPs and training metrics from each training job
def train_func():
   tuner_context = get_tuner_context()
   config = tuner_context.get_hyper_params()
   dm = tuner_context.get_dataset_map()
   ...
   tuner_context.report(metrics={"accuracy": accuracy}, model=model)

# init job training (w/ search space)
tuner = tune.Tuner(
   train_func, 
   { "n_estimators": tune.uniform(50, 200),    # tune.loguniform/randint/choice
      "max_depth": tune.uniform(3, 10),
      "learning_rate": tune.uniform(0.01, 0.3)}, 
   tuner_config)

# ingest the data
tuner_results = tuner.run(
   dataset_map={
      "train": DataConnector.from_dataframe(session.create_dataframe(X_train)),
      "test": DataConnector.from_dataframe(session.create_dataframe(X_test)))})

# get training job results
print(tuner_results.results)
print(tuner_results.best_model)
print(tuner_results.best_result)
