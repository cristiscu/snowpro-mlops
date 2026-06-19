CREATE API INTEGRATION git_api_integration
   API_PROVIDER = git_https_api
   API_ALLOWED_PREFIXES = ('https://github.com')
   ENABLED = TRUE;

CREATE GIT REPOSITORY snowflake_extensions
   ORIGIN = ' https://github.com/cristiscu/snowpro-mlops.git'
   API_INTEGRATION = git_api_integration
   [GIT_CREDENTIALS = git_secret];

ALTER GIT REPOSITORY snowflake_extensions FETCH;

ALTER GIT REPOSITORY snowflake_extensions SET TAG test1='1', test2='2';
ALTER GIT REPOSITORY snowflake_extensions UNSET TAG test1, test2;
