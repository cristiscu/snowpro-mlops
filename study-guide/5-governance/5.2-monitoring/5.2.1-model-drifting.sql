CREATE MODEL MONITOR [ IF NOT EXISTS ] <monitor_name> WITH
    MODEL = <model_name> VERSION = '<version_name>'
    FUNCTION = '<function_name>'
    SOURCE = <source_name>
    WAREHOUSE = <warehouse_name>
    REFRESH_INTERVAL = '<num> { seconds | minutes | hours | days }'
    AGGREGATION_WINDOW = '<num> days'
    TIMESTAMP_COLUMN = <timestamp_name>
    [ BASELINE = <baseline_name> ]
    [ ID_COLUMNS = <id_column_name_array> ]
    [ PREDICTION_CLASS_COLUMNS = <prediction_class_column_name_array> ]
    [ PREDICTION_SCORE_COLUMNS = <prediction_column-name_array> ]
    [ ACTUAL_CLASS_COLUMNS = <actual_class_column_name_array> ]
    [ ACTUAL_SCORE_COLUMNS = <actual_column_name_array> ]
    [ SEGMENT_COLUMNS = <segment_column_name_array> ]
    [ CUSTOM_METRIC_COLUMNS = <custom_metric_column_name_array> ]

# ----------------------------------------------------- 

CREATE MODEL MONITOR MORTGAGE_LENDING_BASE_MODEL_MONITOR WITH
    MODEL=MORTGAGE_LENDING_MLOPS_0 VERSION=XGB_BASE
    FUNCTION=predict
    SOURCE=DEMO_MORTGAGE_LENDING_TEST_0
    BASELINE=DEMO_MORTGAGE_LENDING_TRAIN_0
    TIMESTAMP_COLUMN=TIMESTAMP
    PREDICTION_CLASS_COLUMNS=(XGB_BASE_PREDICTION)  
    ACTUAL_CLASS_COLUMNS=(MORTGAGERESPONSE)
    ID_COLUMNS=(LOAN_ID)
    WAREHOUSE=E2E_SNOW_MLOPS_WH
    REFRESH_INTERVAL='1 hour'
    AGGREGATION_WINDOW='1 day';

CREATE MODEL MONITOR MORTGAGE_LENDING_OPTIMIZED_MODEL_MONITOR WITH
    MODEL=MORTGAGE_LENDING_MLOPS_0 VERSION=XGB_OPTIMIZED
    FUNCTION=predict
    SOURCE=DEMO_MORTGAGE_LENDING_TEST_0
    BASELINE=DEMO_MORTGAGE_LENDING_TRAIN_0
    TIMESTAMP_COLUMN=TIMESTAMP
    PREDICTION_CLASS_COLUMNS=(XGB_OPTIMIZED_PREDICTION)  
    ACTUAL_CLASS_COLUMNS=(MORTGAGERESPONSE)
    ID_COLUMNS=(LOAN_ID)
    WAREHOUSE=E2E_SNOW_MLOPS_WH
    REFRESH_INTERVAL='12 hours'
    AGGREGATION_WINDOW='1 day';

# ----------------------------------------------------- 
#	model monitor functions - query model drift metrics

SELECT * FROM TABLE(MODEL_MONITOR_DRIFT_METRIC(
    'MORTGAGE_LENDING_BASE_MODEL_MONITOR',
    'DIFFERENCE_OF_MEANS',
    'XGB_BASE_PREDICTION',
    '1 DAY',
    DATEADD(DAY, -90, CURRENT_DATE()),
    DATEADD(DAY, -60, CURRENT_DATE())))
