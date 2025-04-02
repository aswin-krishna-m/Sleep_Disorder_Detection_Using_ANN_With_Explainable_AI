import shap
import joblib
import numpy as np
import pandas as pd
import tensorflow as tf
from model import SleepDisorderANN
from preprocessing import preprocess_data

# Paths to model and preprocessing components
model_path = "best_sleep_disorder_model.keras"
scaler_path = "scaler.pkl"
label_encoder_path = "label_encoders.pkl"

# Load trained components
scaler = joblib.load(scaler_path)
label_encoders = joblib.load(label_encoder_path)

# Load trained TensorFlow model
input_size = len(scaler.mean_)
output_size = len(label_encoders["Sleep Disorder"].classes_)
model = SleepDisorderANN(input_size, output_size)
model.load_weights(model_path)

# Initialize SHAP Explainer with a sample background dataset
background_data = np.zeros((1, input_size))  # Using a dummy input for SHAP initialization
explainer = shap.Explainer(model, background_data)

def explain_prediction(data_dict):
    """
    Generates a prediction along with SHAP-based feature importance scores.
    
    Args:
        data_dict (dict): A dictionary containing patient data for prediction.
    
    Returns:
        dict: Prediction result including disorder classification, confidence, and feature importance.
    """
    df = pd.DataFrame([data_dict])  # Convert input dictionary to DataFrame
    X, _, _, _ = preprocess_data(df, scaler, label_encoders)  # Preprocess input
    X_numpy = np.array(X)  # Convert to NumPy array

    # Get model prediction
    probabilities = model.predict(X_numpy)
    prediction_idx = np.argmax(probabilities, axis=1)[0]
    confidence = probabilities[0][prediction_idx]
    predicted_label = label_encoders["Sleep Disorder"].inverse_transform([prediction_idx])[0]

    # Compute SHAP values
    shap_values = explainer(X_numpy)
    shap_values_array = shap_values.values  # Extract SHAP values as an array

    # Map feature importance scores to feature names
    feature_names = [
        "Age", "Gender", "Occupation", "Sleep Duration", "Quality of Sleep",
        "Physical Activity Level", "Stress Level", "BMI Category",
        "Systolic", "Diastolic", "Heart Rate", "Daily Steps"
    ]
    feature_importance = {feature: shap_values_array[0, i].sum() for i, feature in enumerate(feature_names)}

    # Convert SHAP values to scientific notation for better readability
    feature_importance = {key: "{:.1e}".format(value) for key, value in feature_importance.items()}

    return {
        "PredictedDisorder": predicted_label,
        "Confidence": f"{confidence * 100:.2f}%",
        "FeatureImportance": feature_importance
    }

if __name__ == "__main__":
    # Sample input for testing
    sample_input = {
        "Gender": "Male",
        "Age": 28,
        "Occupation": "Sales Representative",
        "Sleep Duration": 5.9,
        "Quality of Sleep": 4,
        "Physical Activity Level": 30,
        "Stress Level": 8,
        "BMI Category": "Obese",
        "Heart Rate": 85,
        "Daily Steps": 3000,
        "Systolic": 140,
        "Diastolic": 90
    }
    
    result = explain_prediction(sample_input)
    print(result)
