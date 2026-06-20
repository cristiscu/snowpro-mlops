-- Create a Notification Integration
-- configure the integration that allows Snowflake to send automated emails.

CREATE OR REPLACE NOTIFICATION INTEGRATION model_alert_email
    TYPE = EMAIL
    ENABLED = TRUE
    ALLOWED_RECIPIENTS = ('your-team@domain.com');

-- ----------------------------------------------------------
-- Write Your Performance Degradation Logic
-- SQL condition that checks your event logs, ML registry views, or data metric functions. 
-- Assume you log model performance scores into a table named MODEL_PERFORMANCE_LOG.

SELECT CASE WHEN AVG(accuracy) < 0.85 THEN TRUE 
    ELSE FALSE END AS degradation_flag
FROM MODEL_PERFORMANCE_LOG
WHERE evaluation_timestamp >= DATEADD(day, -7, CURRENT_TIMESTAMP());

-- ----------------------------------------------------------
-- Define and Start the Alert
-- Combine your logic with an alert that fires on a set schedule
-- and sends an email via your configured integration.

CREATE OR REPLACE ALERT model_drift_alert
    WAREHOUSE = your_compute_wh
    SCHEDULE = '7 DAY'                  -- Adjust evaluation cadence
    IF (EXISTS(
        SELECT 1 
        FROM MODEL_PERFORMANCE_LOG
        WHERE accuracy < 0.85 
            AND evaluation_timestamp >= DATEADD(day, -7, CURRENT_TIMESTAMP())))
    THEN CALL SYSTEM$SEND_EMAIL(
        'model_alert_email',
        'your-team@domain.com',
        'Model Degradation Alert',
        'Warning: Model accuracy has dropped below the 0.85 threshold in the last 7 days.');

ALTER ALERT model_drift_alert RESUME;
