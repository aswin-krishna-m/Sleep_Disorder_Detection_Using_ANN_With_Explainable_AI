import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # Disable GPU for SHAP KernelExplainer

import shap
import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from doctor.ml_model.model import SleepDisorderANN
from doctor.ml_model.preprocessing import preprocess_data
from doctor.ml_model.paths import model_path, scaler_path, label_encoder_path,data_path

scaler = joblib.load(scaler_path)
label_encoders = joblib.load(label_encoder_path)

def explain_model(data_df):
    X_sample, _, _, _ = preprocess_data(data_df, scaler, label_encoders)

    df_full = pd.read_csv(data_path)
    X_background, _, _, _ = preprocess_data(df_full, scaler, label_encoders)

    feature_names = list(X_sample.columns) if isinstance(X_sample, pd.DataFrame) else [f'feature_{i}' for i in range(X_sample.shape[1])]

    input_size = X_sample.shape[1]
    output_size = len(label_encoders["Sleep Disorder"].classes_)
    model = SleepDisorderANN(input_size, output_size)
    model.load_weights(model_path)

    explainer = shap.KernelExplainer(model.predict, X_background[:100])

    shap_values = explainer(X_sample)
    feature_names = [
        "Gender", "Age", "Occupation", "Sleep Duration", "Quality of Sleep",
        "Physical Activity Level", "Stress Level", "BMI Category",
        "Systolic", "Diastolic", "Heart Rate", "Daily Steps"
    ]
    X_sample_df = pd.DataFrame(X_sample, columns=feature_names)
    # print(X_sample_df.shape)
    # print(np.array(shap_values).shape)
    # print(f"Features in X_sample: {X_sample_df.columns}")
    # print("SHAP values shape:", [np.array(s).shape for s in shap_values])
    pred = model.predict(X_sample)
    predicted_class = np.argmax(pred, axis=1)[0]

    class_names = list(label_encoders["Sleep Disorder"].classes_)
    class_names = ["Normal" if pd.isna(c) else c for c in class_names]
    predicted_label = label_encoders["Sleep Disorder"].inverse_transform([predicted_class])[0]
    # print("Predicted Sleep Disorder Class:", predicted_label)
    # shap_values_for_class = shap_values[predicted_class][0]  # (12,)
    # shap.plots.waterfall(shap_values, max_display=14)
    shap.summary_plot(shap_values, features=X_sample_df, feature_names=X_sample_df.columns,class_names=class_names)
    plt.savefig("static/graph.png", format="png")
    

# Sample input
# input_data = {
#     "Gender": "Male",
#     "Age": 27,
#     "Occupation": "Software Engineer",
#     "Sleep Duration": 6.5,
#     "Quality of Sleep": 4,
#     "Physical Activity Level": 32,
#     "Stress Level": 6,
#     "BMI Category": "Overweight",
#     "Systolic": 126,
#     "Diastolic": 83,
#     "Heart Rate": 77,
#     "Daily Steps": 2200
# }