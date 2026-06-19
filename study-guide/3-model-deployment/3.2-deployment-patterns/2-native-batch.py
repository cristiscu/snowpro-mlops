from snowflake.ml.registry import Registry

reg = Registry(session=session, database_name=DB, schema_name=SCH)
mv = reg.get_model('mymodel').version('myversion')  	# returns ModelVersion

# SHOW FUNCTION IN MODEL model VERSION version;
mv.show_functions()						# predict...

# --------------------------------------------------------
preds = mv.run(
   input_features, 
   function_name="predict", 
   [params={"temperature": 0.9, "max_tokens": 512}]  fct parameters
   [service_name="example_spcs_service"])  if on SPCS (else on a warehouse)

preds.show()

# --------------------------------------------------------
# run from a warehouse / service:

# SELECT MODEL(model, [v1/LAST])!predict(input_text, [0.9, [512]]) FROM my_table;
# SELECT service!predict(input_text => input_text, [max_tokens => 512]) FROM table;
