# create task graph
CREATE TASK task_root SCHEDULE='1 MINUTE' AS SELECT 1;

CREATE TASK task_a AFTER task_root AS SELECT 1;
CREATE TASK task_b AFTER task_root AS SELECT 1;
CREATE TASK task_c AFTER task_a, task_b AS SELECT 1;

CREATE TASK task_finalizer FINALIZE=task_root AS SELECT 1;

# ------------------------------------------------------------
# show all dep tasks
select * from table(information_schema.task_dependents(
   task_name => 'db.sch.task_root', recursive => false));

# ------------------------------------------------------------
# reset all tasks manually
ALTER TASK task_a RESUME;
ALTER TASK task_b RESUME;
ALTER TASK task_c RESUME;
ALTER TASK task_finalizer RESUME;

SELECT SYSTEM$TASK_DEPENDENTS_ENABLE('db.sch.task_root');	-- alternative

# ------------------------------------------------------------
# execute task graph manually
EXECUTE TASK task_root;		            -- or ALTER TASK task_root RESUME;
ALTER TASK task_root SUSPEND;

EXECUTE TASK ... RETRY LAST;
EXECUTE TASK ... RETRY GRAPH RUN;
