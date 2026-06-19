-- 1. Configure Role-Based Access Control (RBAC)

-- Create a specialized role and grant warehouse access
CREATE ROLE feature_store_admin;
GRANT USAGE ON WAREHOUSE compute_wh TO ROLE feature_store_admin;

-- Grant permissions to create and manage the workspace
GRANT CREATE DATABASE ON ACCOUNT TO ROLE feature_store_admin;

-- Data scientists require specific schema execution grants
GRANT CREATE DYNAMIC TABLE, CREATE VIEW, CREATE TABLE 
ON SCHEMA ml_db.prod_feature_store TO ROLE feature_store_admin;
