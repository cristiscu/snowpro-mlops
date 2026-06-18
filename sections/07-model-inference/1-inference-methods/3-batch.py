from snowflake.ml.registry import Registry

reg = Registry(session=session, database_name=DB, schema_name=SCH)
mv = reg.get_model('mymodel').version('myversion')  	# returns ModelVersion

# --------------------------------------------------------
from snowflake.ml.model.batch import OutputSpec, InputSpec

job = mv.run_batch(
   X=session.table("my_table"),		# inference data
   compute_pool="my_compute_pool",
   [input_spec=InputSpec(params={"temperature":0.9, "max_tokens":512})],
   output_spec=OutputSpec(stage_location="@db.sch.stage/path/"))

job.wait() 						    # blocks until job finishes

# --------------------------------------------------------
from snowflake.ml.jobs import list_jobs, delete_job, get_job

job.get_logs()
job.cancel()
list_jobs().show()
job = get_job("db.sch.job_name")
delete_job(job)
