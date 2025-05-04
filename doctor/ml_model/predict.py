import joblib
import numpy as np
import pandas as pd
from doctor.ml_model.model import SleepDisorderANN
from doctor.ml_model.preprocessing import preprocess_data
from doctor.ml_model.paths import model_path, scaler_path, label_encoder_path
from doctor.ml_model.xai import explain_model
# Load trained components
scaler = joblib.load(scaler_path)
label_encoders = joblib.load(label_encoder_path)

# Load trained TensorFlow model
input_size = len(scaler.mean_)
output_size = len(label_encoders["Sleep Disorder"].classes_)
model = SleepDisorderANN(input_size, output_size)
model.load_weights(model_path)

def predict_sleep_disorder(data_dict):
    df = pd.DataFrame([data_dict])
    X, _, _, _ = preprocess_data(df, scaler, label_encoders)
    X_numpy = np.array(X)

    probabilities = model.predict(X_numpy)
    prediction_idx = np.argmax(probabilities, axis=1)[0]
    confidence = probabilities[0][prediction_idx]

    predicted_label = label_encoders["Sleep Disorder"].inverse_transform([prediction_idx])[0]
    explain_model(df)
    return {
        "PredictedDisorder": predicted_label,
        "Confidence": f"{confidence * 100:.2f}%",
    }

# if __name__ == "__main__":
#     sample_input = {
#         "Gender": "Male",
#         "Age": 27,
#         "Occupation": "Software Engineer",
#         "Sleep Duration": 6.5,
#         "Quality of Sleep": 4,
#         "Physical Activity Level": 32,
#         "Stress Level": 6,
#         "BMI Category": "Overweight",
#         "Systolic": 126,
#         "Diastolic": 83,
#         "Heart Rate": 77,
#         "Daily Steps": 2200
#     }

#     result = predict_sleep_disorder(sample_input)
#     print(result)
