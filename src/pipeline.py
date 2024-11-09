from src.data.load_data import load_data
from src.data.preprocess import clean_data
from src.data.feature_engineering import engineer_features
from src.models.train import train_model
from src.models.evaluate import evaluate_model

def run_pipeline():
    data = load_data()
    clean_data(data)
    features = engineer_features(data)
    model = train_model(features)
    evaluate_model(model, features)

if __name__ == "__main__":
    run_pipeline()
