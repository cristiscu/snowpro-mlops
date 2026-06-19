CREATE SERVICE echo_service
IN COMPUTE POOL tutorial_compute_pool
FROM SPECIFICATION $$
spec:
  containers:
  - name: echo
    image: /tutorial_db/data_schema/tutorial_repository/my_image:tutorial
    readinessProbe:
      port: 8000
      path: /healthcheck
  endpoints:
  - name: echoendpoint
    port: 8000
    public: true
$$;

CREATE SERVICE echo_service
  IN COMPUTE POOL tutorial_compute_pool
  FROM @tutorial_stage
  SPECIFICATION_FILE='echo_spec.yaml';

EXECUTE JOB SERVICE
IN COMPUTE POOL tutorial_compute_pool
FROM SPECIFICATION $$
spec:
  containers:
  - name: main
    image: /tutorial_db/data_schema/tutorial_repository/my_image:latest
    env:
      SNOWFLAKE_WAREHOUSE: tutorial_warehouse
    args:
    - "--query=select current_time() as time,'hello'"
    - "--result_table=results"
$$;

EXECUTE JOB SERVICE
IN COMPUTE POOL tutorial_compute_pool
NAME = example_job_service
ASYNC = TRUE
FROM SPECIFICATION $$ ... $$;
