import numpy as np
import joblib
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from model import SleepDisorderANN  # Import TensorFlow model
from preprocessing import preprocess_data  # Import preprocessing function
# from paths import data_path,model_path,scaler_path,label_encoder_path

# Paths
data_path = "data.csv"
model_path = "best_sleep_disorder_model.keras"
scaler_path = "scaler.pkl"
label_encoder_path = "label_encoders.pkl"

# Load scaler and label encoders
scaler = joblib.load(scaler_path)
label_encoders = joblib.load(label_encoder_path)

# Preprocess test data
X, y, _, _ = preprocess_data(data_path, scaler, label_encoders)

# Convert to NumPy arrays
X = np.array(X)
y = np.array(y)

# Load trained model
input_size = X.shape[1]
output_size = len(label_encoders["Sleep Disorder"].classes_)
model = SleepDisorderANN(input_size, output_size)
model.load_weights(model_path)

# Model evaluation
y_pred_prob = model.predict(X)
y_pred = np.argmax(y_pred_prob, axis=1)

accuracy = accuracy_score(y, y_pred)
precision = precision_score(y, y_pred, average="weighted")
recall = recall_score(y, y_pred, average="weighted")
f1 = f1_score(y, y_pred, average="weighted")

print(f"Test Accuracy: {accuracy * 100:.2f}%")
print(f"Test F1 Score: {f1 * 100:.2f}%")
print(f"Test Recall: {recall * 100:.2f}%")
print(f"Test Precision: {precision * 100:.2f}%")

# Optional: Confusion matrix visualization
# import matplotlib.pyplot as plt
# import seaborn as sns
# cm = confusion_matrix(y, y_pred)
# plt.figure(figsize=(8, 6))
# sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
#             xticklabels=label_encoders["Sleep Disorder"].classes_,
#             yticklabels=label_encoders["Sleep Disorder"].classes_)
# plt.xlabel("Predicted Label")
# plt.ylabel("True Label")
# plt.title("Confusion Matrix")
# plt.show()
