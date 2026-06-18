# run all these in a worksheet in your default personal workspace
CREATE DATABASE IF NOT EXISTS TEST;

CREATE OR REPLACE API INTEGRATION git_api_integration
  API_PROVIDER = git_https_api
  API_ALLOWED_PREFIXES = ('https://github.com')
  ENABLED = TRUE;

# create new GIT workspace with:
# Repository URL: https://github.com/cristiscu/snowpro-mlops.git
# Workspace name: snowpro-mlops
# API integration: git_api_integration
# Public repository