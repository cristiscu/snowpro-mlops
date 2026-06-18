from snowflake.ml.modeling import tune
from snowflake.ml.modeling.tune.search import BayesOpt, RandomSearch, GridSearch

# (1) ingest the data
dataset_map = {
   "train": DataConnector.from_dataframe(session.create_dataframe(X_train)),
   "test": DataConnector.from_dataframe(session.create_dataframe(X_test)))}

# (2) define search algorithm: GridSearch() / BayesOpt() / RandomSearch()
search_alg = GridSearch()

# (3) define sampling: tune.uniform/loguniform/randint/choice
search_space = {
   "n_estimators": tune.uniform(50, 200),
   "max_depth": tune.uniform(3, 10),
   "learning_rate": tune.uniform(0.01, 0.3)}

# (4) configure the tunner
tuner_config = tune.TunerConfig(
   metric="accuracy",
   mode="max",
   search_alg=search_algorithm.BayesOpt(
      utility_kwargs={"kind": "ucb", "kappa": 2.5, "xi": 0.0}),
   num_trials=5,
   max_concurrent_trials=1)

# (5) get the HPs and training metrics from each training job
def train_func():
   tuner_context = get_tuner_context()
   config = tuner_context.get_hyper_params()
   dm = tuner_context.get_dataset_map()
   ...
   tuner_context.report(metrics={"accuracy": accuracy}, model=model)

# (6) init job training
tuner = tune.Tuner(train_func, search_space, tuner_config)
tuner_results = tuner.run(dataset_map=dataset_map)

# (7) get training job results
print(tuner_results.results)
print(tuner_results.best_model)
print(tuner_results.best_result)
