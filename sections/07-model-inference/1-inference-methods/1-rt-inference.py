from snowflake.ml.registry import Registry

reg = Registry(session=session, database_name=DB, schema_name=SCH)
mv = reg.get_model('mymodel').version('myversion')  	# returns ModelVersion

# --------------------------------------------------------
mv.create_service(
   service_name="myservice",
   service_compute_pool="mycp",
   ingress_enabled=True,
   gpu_requests=None)

mv.list_services()
