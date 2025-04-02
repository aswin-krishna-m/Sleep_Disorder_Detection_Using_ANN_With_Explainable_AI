import shap
import joblib
import numpy as np
import pandas as pd
from doctor.ml_model.model import SleepDisorderANN
from doctor.ml_model.preprocessing import preprocess_data
from doctor.ml_model.paths import model_path,scaler_path,label_encoder_path

# Load trained components
scaler = joblib.load(scaler_path)
label_encoders = joblib.load(label_encoder_path)

# Load trained TensorFlow model
input_size = len(scaler.mean_)
output_size = len(label_encoders["Sleep Disorder"].classes_)
model = SleepDisorderANN(input_size, output_size)
model.load_weights(model_path)

# Initialize SHAP Explainer
background_data = np.zeros((1, input_size))  # SHAP needs background data
explainer = shap.Explainer(model, background_data)

def predict_with_explanation(data_dict):
    df = pd.DataFrame([data_dict])  
    X, _, _, _ = preprocess_data(df, scaler, label_encoders)  
    X_numpy = np.array(X)  

    # Get model prediction
    probabilities = model.predict(X_numpy)
    prediction_idx = np.argmax(probabilities, axis=1)[0]
    confidence = probabilities[0][prediction_idx]

    predicted_label = label_encoders["Sleep Disorder"].inverse_transform([prediction_idx])[0]

    # Compute SHAP values
    # Compute SHAP values
    shap_values = explainer(X_numpy)

    # Extract SHAP values as an array
    shap_values_array = shap_values.values

    # Convert SHAP values to a dictionary for feature importance
    feature_importance = {
        feature: shap_values_array[0, i].sum() for i, feature in enumerate([
            "Age", "Gender", "Occupation", "Sleep Duration", "Quality of Sleep",
            "Physical Activity Level", "Stress Level", "BMI Category",
            "Systolic", "Diastolic", "Heart Rate", "Daily Steps"
        ])
    }

    feature_importance = {key: "{:.1e}".format(value) for key, value in feature_importance.items()}
    return {
        "PredictedDisorder": predicted_label,
        "Confidence": f"{confidence * 100:.2f}%",
        "FeatureImportance": feature_importance
    }

if __name__ == "__main__":
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
    
    result = predict_with_explanation(sample_input)
    print(result)
