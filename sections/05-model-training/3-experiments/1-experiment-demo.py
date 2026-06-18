exp = ExperimentTracking(session=session)

experiment_date = datetime.now().strftime("%Y%m%d")
experiment_name = f"Wine_Quality_Classification_{experiment_date}"
exp.set_experiment(experiment_name)

# Train baseline model
with exp.start_run(run_name="baseline_xgboost") as run:
    # Define baseline parameters
    baseline_params = {
        'n_estimators': 100,
        'max_depth': 6,
        'learning_rate': 0.1,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'gamma': 0.1,
        'min_child_weight': 8,
        'random_state': 42,
    }
    
    # Log parameters
    exp.log_params(baseline_params)
    
    # Train model
    baseline_model = XGBClassifier(**baseline_params)
    baseline_model.fit(X_train_scaled, y_train)
    
    # Evaluate on validation set
    y_val_pred = baseline_model.predict(X_val_scaled)
    y_val_proba = baseline_model.predict_proba(X_val_scaled)[:, 1]
    
    # Calculate metrics
    val_metrics = {
        'val_accuracy': metrics.accuracy_score(y_val, y_val_pred),
        'val_precision': metrics.precision_score(y_val, y_val_pred),
        'val_recall': metrics.recall_score(y_val, y_val_pred),
        'val_f1': metrics.f1_score(y_val, y_val_pred),
        'val_roc_auc': metrics.roc_auc_score(y_val, y_val_proba)
    }
    
    # Log metrics
    exp.log_metrics(val_metrics)
    
    print("Baseline Model Performance:")
    for metric, value in val_metrics.items():
        print(f"  {metric}: {value:.4f}")
