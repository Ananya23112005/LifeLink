import pickle
import mysql.connector
import pandas as pd

# Load the model and encoders
with open("ml/model.pkl", "rb") as f:
    data = pickle.load(f)
    model = data['model']
    blood_encoder = data['blood_encoder']
    organ_encoder = data['organ_encoder']

# Connect to DB
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="ananya",
        database="lifelink"
    )

# Check blood group compatibility
def is_blood_compatible(donor_blood, recipient_blood):
    compatibility = {
        'O-': ['O-', 'O+', 'A-', 'A+', 'B-', 'B+', 'AB-', 'AB+'],
        'O+': ['O+', 'A+', 'B+', 'AB+'],
        'A-': ['A-', 'A+', 'AB-', 'AB+'],
        'A+': ['A+', 'AB+'],
        'B-': ['B-', 'B+', 'AB-', 'AB+'],
        'B+': ['B+', 'AB+'],
        'AB-': ['AB-', 'AB+'],
        'AB+': ['AB+']
    }
    return recipient_blood in compatibility.get(donor_blood, [])

def predict_match(recipient):
    """
    recipient: dict with keys 'blood_type', 'organ_type', 'age','urgency'
    """
    try:
        # Encode recipient inputs
        if recipient['blood_type'] not in blood_encoder.classes_:
            raise ValueError("Invalid recipient blood type.")
        if recipient['organ_type'] not in organ_encoder.classes_:
            raise ValueError("Invalid recipient organ type.")

        # Encoding categorical variables
        recip_blood = blood_encoder.transform([recipient['blood_type']])[0]
        recip_organ = organ_encoder.transform([recipient['organ_type']])[0]
        recip_age = recipient['age']
        urgency = recipient['urgency']

        # Connect and fetch possible donors for the same organ
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM donors
            WHERE organ_type = %s
        """, (recipient['organ_type'],))
        donor_rows = cursor.fetchall()
        cursor.close()
        conn.close()

        if not donor_rows:
            return {"match": False, "message": "No donors available for this organ type."}

        compatible_matches = []

        for donor in donor_rows:
            if donor['blood_type'] not in blood_encoder.classes_:
                continue

            if not is_blood_compatible(donor['blood_type'], recipient['blood_type']):
                continue

            donor_blood = blood_encoder.transform([donor['blood_type']])[0]
            donor_organ = organ_encoder.transform([donor['organ_type']])[0]
            donor_age = donor['age']

            features_df = pd.DataFrame([{
                'donor_blood_encoded': donor_blood,
                'recip_blood_encoded': recip_blood,
                'donor_organ_encoded': donor_organ,
                'recip_organ_encoded': recip_organ,
                'donor_age': donor_age,
                'recip_age': recip_age,
                'urgency_level': urgency
            }])
            print("Feature vector:\n",(features_df))

            #prediction = model.predict(features_df)[0]
            #confidence = model.predict_proba(features_df)[0][1]
            proba = model.predict_proba(features_df)[0][1]
            prediction = 1 if proba >= 0.3 else 0

            print(f"Donor ID: {donor['donor_id']}, Prediction: {prediction}")


            if  prediction==1 :
                compatible_matches.append({
                    "Donor ID": donor['donor_id'],
                    "Name": donor['name'],
                    "Blood Type": donor['blood_type'],
                    "Organ Type": donor['organ_type'],
                    "Age": donor['age'],
                    #"Confidence (%)": round(confidence * 100, 2),
                    "Contact Info": donor['contact_info']
                })

        if compatible_matches:
            # Create a DataFrame and display as table
            df = pd.DataFrame(compatible_matches)
            print("\n✅ Compatible Matches Found:\n")
            print(df.to_string(index=False))
            print("Total donors checked:", len(donor_rows))
            print("Valid compatible matches:", len(compatible_matches))

            return {
                "match": True,
                "message": f"Found {len(compatible_matches)} compatible donor(s)!",
                "matches": compatible_matches
            }
        else:
            return {"match": False, "message": "No compatible match found."}

    except Exception as e:
        return {"match": False, "message": f"Error occurred: {str(e)}", "matches": []}
