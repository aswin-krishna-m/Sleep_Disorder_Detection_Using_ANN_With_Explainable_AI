import os
from django.conf import settings
BASE_DIR = settings.BASE_DIR

# Define paths for ML-related files
data_path = os.path.join(BASE_DIR, "doctor", "ml_model", "data.csv")
model_path = os.path.join(BASE_DIR, "doctor", "ml_model", "best_sleep_disorder_model.keras")
scaler_path = os.path.join(BASE_DIR, "doctor", "ml_model", "scaler.pkl")
label_encoder_path = os.path.join(BASE_DIR, "doctor", "ml_model", "label_encoders.pkl")