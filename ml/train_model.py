import mysql.connector
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Function to connect to the MySQL database
def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="ananya",  # Change if needed
            database="lifelink"
        )
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Function to fetch data from the database
def fetch_data():
    conn = connect_db()
    if not conn:
        return pd.DataFrame()  # Return an empty DataFrame if connection fails

    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT 
        d.blood_type AS donor_blood_type,
        p.blood_type AS recip_blood_type,
        d.organ_type AS donor_organ_type,
        p.organ_needed AS recip_organ_type,
        d.age AS donor_age,
        p.age AS recip_age,
        p.urgency AS urgency_level,
        p.compatible AS `match`
    FROM 
        donors d
    JOIN 
        patients p 
    ON 
        d.organ_type = p.organ_needed
    WHERE 
        p.compatible IS NOT NULL
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return pd.DataFrame(rows)

# Function to train and save the model
def train_and_save_model():
    df = fetch_data()
    if df.empty:
        print("❌ No data found in the database.")
        return

    print(f"✅ Data loaded with {len(df)} records.")

    # Check for missing or invalid values in critical columns
    if df[['donor_blood_type', 'recip_blood_type', 'donor_organ_type', 'recip_organ_type']].isnull().any().any():
        print("❌ Missing values found in critical columns. Please check the data.")
        return

    # Fit blood type encoder on all possible blood types from both donor and recipient
    blood_encoder = LabelEncoder()
    all_blood = pd.concat([df['donor_blood_type'], df['recip_blood_type']], ignore_index=True)
    blood_encoder.fit(all_blood)

    df['donor_blood_encoded'] = blood_encoder.transform(df['donor_blood_type'])
    df['recip_blood_encoded'] = blood_encoder.transform(df['recip_blood_type'])

    # Fit organ type encoder on both donor and recipient organ types
    organ_encoder = LabelEncoder()
    all_organ = pd.concat([df['donor_organ_type'], df['recip_organ_type']], ignore_index=True)
    organ_encoder.fit(all_organ)

    df['donor_organ_encoded'] = organ_encoder.transform(df['donor_organ_type'])
    df['recip_organ_encoded'] = organ_encoder.transform(df['recip_organ_type'])

    # Prepare training data
    X = df[['donor_blood_encoded', 'recip_blood_encoded', 'donor_organ_encoded', 'recip_organ_encoded', 'donor_age', 'recip_age', 'urgency_level']]
    y = df['match']

    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = RandomForestClassifier(
    n_estimators=100,
    class_weight='balanced',  # Treats minority class (matches) more seriously
    max_depth=10,  # Optional: prevents overfitting
    random_state=42
    )
    model.fit(X_train, y_train)

    # Save the trained model and encoders
    with open("ml/model.pkl", "wb") as f:
        pickle.dump({
            "model": model,
            "blood_encoder": blood_encoder,
            "organ_encoder": organ_encoder
        }, f)

    print(f"✅ Model trained and saved as ml/model.pkl")

# Run the training function
if __name__ == "__main__":
    train_and_save_model()
