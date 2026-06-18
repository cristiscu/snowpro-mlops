# grant usage to a prod role
GRANT USAGE ON MODEL my_model TO ROLE prod_role;

# promote model to production
ALTER MODEL my_model SET DEFAULT_VERSION = new_version;

# use model in prod
SELECT my_model!predict(...) ... ;

# dev and testing
SELECT MODEL(my_model, new_version)!predict(...) FROM ...;

# -------------------------------------------------------
# use aliases

ALTER MODEL my_model VERSION v1 SET ALIAS = production;
ALTER MODEL my_model VERSION v2 SET ALIAS = alpha;

ALTER MODEL my_model VERSION v2 UNSET ALIAS;
ALTER MODEL my_model VERSION v2 SET ALIAS = beta;

ALTER MODEL my_model VERSION v1 UNSET ALIAS;
ALTER MODEL my_model VERSION v2 UNSET ALIAS;
ALTER MODEL my_model VERSION v2 SET ALIAS = production;

# use model versions in prod and dev/testing
SELECT MODEL(my_model, production)!predict(...) FROM ...;
SELECT MODEL(my_model, alpha)!predict(...) FROM ...;