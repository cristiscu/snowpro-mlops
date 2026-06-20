# Experiment with single run [Template]
# https://docs.snowflake.com/en/developer-guide/snowflake-ml/experiments
# (you still need the training and test input datasets)

# ~CREATE EXPERIMENT exp
exp = ExperimentTracking(session=session)

experiment_date = datetime.now().strftime("%Y%m%d")
experiment_name = f"Wine_Quality_Classification_{experiment_date}"
exp.set_experiment(experiment_name)

# Train baseline model
# or with exp.end_run("run")
# ~ALTER EXPERIMENT exp ADD RUN run
with exp.start_run(run_name="run") as run:

    # ----------------------------------------------------
    # Define and log baseline parameters
    baseline_params = {
        'n_estimators': 100,
        'max_depth': 6,
        'learning_rate': 0.1,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'gamma': 0.1,
        'min_child_weight': 8,
        'random_state': 42 }
    exp.log_params(baseline_params)
    
    # ----------------------------------------------------
    # Train model and evaluate on validation set
    model = XGBClassifier(**baseline_params)
    model.fit(X_train_scaled, y_train)
    
    y_val_pred = model.predict(X_val_scaled)
    y_val_proba = model.predict_proba(X_val_scaled)[:, 1]
    
    # ----------------------------------------------------
    # Calculate and log evaluation metrics
    val_metrics = {
        'val_accuracy': metrics.accuracy_score(y_val, y_val_pred),
        'val_precision': metrics.precision_score(y_val, y_val_pred),
        'val_recall': metrics.recall_score(y_val, y_val_pred),
        'val_f1': metrics.f1_score(y_val, y_val_pred),
        'val_roc_auc': metrics.roc_auc_score(y_val, y_val_proba) }
    exp.log_metrics(val_metrics)
    
    print("Baseline Model Performance:")
    for metric, value in val_metrics.items():
        print(f"  {metric}: {value:.4f}")

    # ----------------------------------------------------
    # Log artifacts (from staged files)
    exp.log_artifact('/tmp/file.txt', artifact_path='artifacts')

    # ----------------------------------------------------
    # Register the model
    exp.log_model(
        model=model,
        model_name="my_model",
        options={"method_options": { "predict": { "case_sensitive": True } }})        

# ----------------------------------------------------
# Retrieve logged metric/parameters for a previous run
single_run_metrics = exp.list_metrics(run_name="run")

print("Baseline Model Performance:")
for metric, value in single_run_metrics.items():
    print(f"  {metric}: {value:.4f}")
