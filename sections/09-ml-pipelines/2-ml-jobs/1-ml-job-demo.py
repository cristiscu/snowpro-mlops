from snowflake.snowpark import Session
from snowflake.ml.jobs import list_jobs, remote, submit_file, MLJobDefinition

session = Session.builder.getOrCreate() 	    # from ~/.snowflake/config.toml
ls = list_jobs([session=session]) 		        # current session implied

@remote(                                        # creates a MLJobDefinition instance!
   "MY_COMPUTE_POOL", 
   stage_name="payload_stage", 
   session=session.
   [runtime_environment="2.3.0"],
   [pip_requirements=["custom-package"]],
   [external_access_integrations=["PYPI_EAI"]])
def train_model([session: Session], data_table: str):
   [session = Session.builder.getOrCreate()]    # if not passed as param
   print(session.sql("SELECT CURRENT_VERSION()").collect())
   # ...
   return model

job = train_model("my_training_data") 	        # async call!
model = job.result() 				            # blocks here!

job1 = submit_file( 				            # can create from file/dir/stage
   "train.py",
   "MY_COMPUTE_POOL",
   stage_name="payload_stage",
   args=["--data-table", "my_training_data"],
   session=session,
   [imports=[("src/utils/", "utils")]])

job_definition1 = MLJobDefinition.register(     # from a stage directory
   entrypoint ='@tmp_stage/my_project/xgb.py',
   source = '@tmp_stage/my_project',
   stage_name = "payload_stage",
   compute_pool = compute_pool)

# train_model is a job definition created by the @remote decorator
train_model_task = DAGTask("TRAIN_MODEL", definition=train_model)

# copy and paste this url in browser to log in then to see the ray dashboard
ray_dashboard_url = job.get_ray_dashboard_url()

job = get_job("<job_id>")

print(job.status) 				                # PENDING/RUNNING/FAILED/DONE
print(job.get_logs())

delete_job(job)
