import argparse
from ml_pipeline.utils.config_loader import load_config
from ml_pipeline.data.ingestion import load_raw_data
from ml_pipeline.data.validation import validate_data_quality
from ml_pipeline.features.transformers import create_features
from ml_pipeline.models.training import train_model
from ml_pipeline.models.evaluation import evaluate_model
from ml_pipeline.models.registry import register_model

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Config file path")
    parser.add_argument("--env", default="dev", help="Environment (dev/prod)")
    args = parser.parse_args()

    config = load_config(args.config, args.env)

    raw_data = load_raw_data(config.data.source_table)
    validate_data_quality(raw_data, config.data.quality_checks)
    features = create_features(raw_data, config.features.transformations)
    model = train_model(features, config.model.hyperparameters)
    metrics = evaluate_model(model, features, config.model.eval_metrics)
    register_model(model, metrics, config.model.registry_name)

if __name__ == "__main__":
    main()
