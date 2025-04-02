from tensorflow import keras
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from preprocessing import preprocess_data
from model import SleepDisorderANN
# from paths import data_path,model_path,scaler_path,label_encoder_path

# Paths
data_path = "data.csv"
model_path = "best_sleep_disorder_model.keras"
scaler_path = "scaler.pkl"
label_encoder_path = "label_encoders.pkl"

# Load and preprocess data
X, y, label_encoders, scaler = preprocess_data(data_path)

# Save label encoders and scaler for future use
joblib.dump(scaler, scaler_path)
joblib.dump(label_encoders, label_encoder_path)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Apply SMOTE to balance the dataset
smote = SMOTE()
X_train, y_train = smote.fit_resample(X_train, y_train)

# Model initialization
input_size = X_train.shape[1]
output_size = len(np.unique(y))

model = SleepDisorderANN(input_size, output_size)
model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.001),
              loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

# Training loop with early stopping
callback = keras.callbacks.EarlyStopping(monitor='val_loss', patience=20, restore_best_weights=True)

model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=200, batch_size=32, callbacks=[callback])

# Save trained model
model.save(model_path)
print("Model training completed and saved.")
