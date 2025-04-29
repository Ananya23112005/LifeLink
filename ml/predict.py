import pickle
import mysql.connector
import pandas as pd

# Load the model and encoders (without urgency_encoder)
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
        # Make sure to encode the 'urgency' value properly using the same encoder
        #urgency = urgency_encoder.transform([recipient['urgency']])[0]


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
        #print(f"Checking blood compatibility: {donor['blood_type']} with {recipient['blood_type']}")

        # Check each donor with the model
        best_match = None
        best_confidence = 0

        for donor in donor_rows:
            print(f"Checking blood compatibility: {donor['blood_type']} with {recipient['blood_type']}")
            # Skip if donor blood type not in encoder
            if donor['blood_type'] not in blood_encoder.classes_:
                #print(f"Skipping donor {donor['donor_id']} due to invalid blood type.")
                continue

            # 🛑 Blood group compatibility check
            if not is_blood_compatible(donor['blood_type'], recipient['blood_type']):
                
                continue

            donor_blood = blood_encoder.transform([donor['blood_type']])[0]
            donor_organ = organ_encoder.transform([donor['organ_type']])[0]
            donor_age = donor['age']


            # Create a DataFrame for prediction with proper feature names
            features_df = pd.DataFrame([{
                'donor_blood_encoded': donor_blood,
                'recip_blood_encoded': recip_blood,
                'donor_organ_encoded': donor_organ,
                'recip_organ_encoded': recip_organ,
                'donor_age': donor_age,
                'recip_age': recip_age,
                'urgency_level':urgency
                
                
            }])
            print("Features DataFrame for prediction:")
            print(features_df)


            # Make prediction and calculate confidence
            prediction = model.predict(features_df)[0]
            confidence = model.predict_proba(features_df)[0][1]
            print(f"Prediction: {prediction}, Confidence: {confidence}")


            if  confidence > best_confidence:
                best_confidence = confidence
                best_match = donor

        if best_match:
            # Include contact_info in the final response
            return {
                "match": True,
                "message": f"🎉 Found a match with donor ID: {best_match['donor_id']}!",
                "confidence": round(best_confidence * 100, 2),
                "donor": {
                    "id": best_match['donor_id'],
                    "name": best_match['name'],
                    "blood_type": best_match['blood_type'],
                    "organ_type": best_match['organ_type'],
                    "age": best_match['age'],
                    "contact_info": best_match['contact_info']  # Include contact_info
                }
            }
        else:
            return {"match": False, "message": "No compatible match found."}

    except Exception as e:
        return {"error": str(e)}
