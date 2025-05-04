import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

def preprocess_data(data, scaler=None, label_encoders=None):
    # Load dataset if `data` is a file path
    if isinstance(data, str):  
        df = pd.read_csv(data)
    else:  
        df = data.copy()  # If already a DataFrame, use it directly

    # Drop "Person ID" if it exists
    if "Person ID" in df.columns:
        df.drop(columns=["Person ID"], inplace=True)

    # Categorical Encoding
    categorical_columns = ["Gender", "Occupation", "BMI Category", "Sleep Disorder"]
    
    if label_encoders is None:
        label_encoders = {}
        for col in categorical_columns:
            if col in df.columns:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col])
                label_encoders[col] = le
    else:
        for col in categorical_columns:
            if col in df.columns:
                df[col] = label_encoders[col].transform(df[col])

    # Define Features & Target Variable
    X = df.drop(columns=["Sleep Disorder"]) if "Sleep Disorder" in df.columns else df
    y = df["Sleep Disorder"] if "Sleep Disorder" in df.columns else None

    # Normalize Data
    if scaler is None:
        scaler = StandardScaler()
        X = scaler.fit_transform(X)
    else:
        X = scaler.transform(X)

    return X, y, label_encoders, scaler

