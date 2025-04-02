import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"  # Disable oneDNN messages
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"   # Suppress TensorFlow INFO & WARNING logs
from tensorflow import keras
from tensorflow.keras import layers

def SleepDisorderANN(input_size, output_size):
    model = keras.Sequential([
        layers.Dense(64, activation="relu", input_shape=(input_size,)),
        layers.BatchNormalization(),
        layers.Dropout(0.3),

        layers.Dense(32, activation="relu"),
        layers.BatchNormalization(),
        layers.Dropout(0.3),

        layers.Dense(output_size, activation="softmax")  
    ])
    
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )
    
    return model
