import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
import joblib


def predict_outbreaks(df):
    # Clean column names
    df.columns = df.columns.str.strip().str.lower()

    # Rename columns to standard format
    df.rename(columns={
        'detected_disease': 'disease',
        'timestamp': 'time',
        'probability': 'probability',
        'location': 'location',
        'source': 'source',
        's.no': 'id',
        'text': 'text'
    }, inplace=True)

    print("\U0001F9EA Columns after renaming:", df.columns.tolist())

    # Check for required columns
    required_cols = ['time', 'disease', 'location', 'source', 'probability']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"❌ Required column '{col}' is missing after renaming.")

    # Ensure datetime conversion
    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    df['hour'] = df['time'].dt.hour
    df['day'] = df['time'].dt.day
    df['month'] = df['time'].dt.month

    # Create group key and outbreak label
    df['group_key'] = df['location'] + "_" + df['disease']
    group_counts = df['group_key'].value_counts()
    df['outbreak_label'] = df.apply(
        lambda row: 1 if row['probability'] > 0.7 and group_counts[row['group_key']] >= 2 else 0,
        axis=1
    )

    # Encode categorical features
    le_loc = LabelEncoder()
    le_dis = LabelEncoder()
    le_src = LabelEncoder()
    df['location_encoded'] = le_loc.fit_transform(df['location'])
    df['disease_encoded'] = le_dis.fit_transform(df['disease'])
    df['source_encoded'] = le_src.fit_transform(df['source'])

    # Frequency-based features
    df['loc_freq'] = df.groupby('location')['location'].transform('count')
    df['dis_freq'] = df.groupby('disease')['disease'].transform('count')
    df['src_freq'] = df.groupby('source')['source'].transform('count')

    # Select features
    features = ['probability', 'hour', 'day', 'month',
                'loc_freq', 'dis_freq', 'src_freq',
                'location_encoded', 'disease_encoded', 'source_encoded']

    X = df[features]
    y = df['outbreak_label']

    # Train-test split for initial evaluation
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model_eval = RandomForestClassifier()
    model_eval.fit(X_train, y_train)
    y_pred_eval = model_eval.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred_eval)
    print(f"✅ Model Accuracy on Test Set: {accuracy * 100:.2f}%")

    # SMOTE for imbalance handling
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X, y)

    # Train final model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_resampled, y_resampled)
    joblib.dump(model, 'outbreak_rf_model.pkl')

    # Predict full dataset
    df['predicted_label'] = model.predict(X)

    # Apply custom threshold logic for final prediction
    df['outbreak_prediction'] = df.apply(
        lambda row: 'Outbreak' if row['probability'] > 0.7 else (
            'Outbreak' if row['predicted_label'] == 1 else 'Normal'
        ),
        axis=1
    )

    print(df[['probability', 'predicted_label', 'outbreak_prediction']].tail(100))

    # Ensure ID column exists for mapping back
    if 'id' not in df.columns:
        raise ValueError("❌ 'id' column is required to update the database but was not found.")

    return df


# -------------------------------
# FUNCTION 2: Single Text Prediction
# -------------------------------
def predict_single_outbreak(text):
    """
    Accepts a text string and returns a dummy disease & probability.
    Replace with NLP-based classification if needed.
    """
    text = text.lower()
    if "covid" in text:
        return "COVID", 0.91
    elif "dengue" in text:
        return "Dengue", 0.87
    elif "flu" in text:
        return "Flu", 0.83
    else:
        return "none", 0.0