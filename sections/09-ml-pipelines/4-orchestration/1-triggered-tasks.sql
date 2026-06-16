CREATE TASK my_triggered_task
   SCHEDULE='15 MINUTES'                        -- remove!
   TARGET_COMPLETION_INTERVAL='15 MINUTES'
   WHEN SYSTEM$STREAM_HAS_DATA('my_order_stream')
   [WAREHOUSE=...]                              -- skip for serverless
AS
   INSERT INTO customer_activity
   SELECT customer_id, order_total, order_date, 'order'
   FROM my_order_stream;

# ------------------------------------------------------------
ALTER TASK task SUSPEND;

ALTER TASK task UNSET SCHEDULE;				    -- from scheduled
ALTER TASK task UNSET WAREHOUSE;				-- to serverless
ALTER TASK task MODIFY TARGET_COMPLETION_INTERVAL '15 minutes'
ALTER TASK task MODIFY WHEN SYSTEM$STREAM_HAS_DATA('my_return_stream');

ALTER TASK task RESUME;
