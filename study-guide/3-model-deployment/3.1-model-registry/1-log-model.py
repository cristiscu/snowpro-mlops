mv = reg.log_model(
    catboost_model,
    model_name="diamond_catboost_explain_enabled",
    version_name="explain_v0",
    conda_dependencies=["snowflake-ml-python"],
    sample_input_data = xs,             # used as background data
    [signatures={
        "predict": predict_signature,
        "predict_proba": predict_proba_signature},]
    [options= {
        "enable_explainability": True,  # to pass both signatures+bk data)
        "relax_version": False }]       # avoid XGBoost err for earlier version

explanations = mv.run(input_data, function_name="explain")

# WITH mv AS MODEL m VERSION v
# SELECT * FROM ..., TABLE(mv!EXPLAIN(CUT, COLOR, ..., TABLE_PCT, X, Y, Z));
