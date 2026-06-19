LIST 'snow://dataset/<dataset_name>/versions/<dataset_version>';
INFER_SCHEMA(
   LOCATION => 'snow://dataset/<dataset_name>/versions/<dataset_version>',
   FILE_FORMAT => '<file_format_name>')

CREATE FILE FORMAT my_parquet_format
   TYPE = PARQUET;
SELECT * FROM TABLE(INFER_SCHEMA(
   FILE_FORMAT => 'snow://dataset/MYDS/versions/v1',
   FILE_FORMAT => 'my_parquet_format'));

SELECT $1 FROM 'snow://dataset/foo/versions/V1' (
   FILE_FORMAT => 'my_parquet_format', 
   PATTERN => '.*data.*') t;
