import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd
import re

# List of blood groups
blood_groups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

# Database connection function
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="ananya",  # Update with your MySQL password
        database="lifelink"
    )

# Register a new recipient
def register_recipient():
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] {
            background-color:  #003153;
        }

        .title {
            font-size: 48px;
            font-weight: bold;
            text-align: center;
            color: white;
            background: linear-gradient(45deg, #ff5c8d, #872657);
            -webkit-background-clip: text;
            background-clip: text;
            padding: 20px;
            margin-bottom: 30px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.subheader("Register Recipient")

    name = st.text_input("Name:")
    age = st.number_input("Age:", min_value=0)
    blood_type = st.selectbox("Blood Group", blood_groups)
    organ_needed = st.selectbox("Organ Needed", ["Kidney", "Heart", "Liver","Lungs","Pancreas"])
    contact_info = st.text_input("Contact Info (Email/Phone):")
    urgency = st.slider("Urgency", min_value=1, max_value=10, value=5, step=1, help="Set urgency level from 1 to 10")
     


   
   

    if st.button("Register Recipient"):
        if not name or not blood_type or not organ_needed or not contact_info or not urgency:
            st.error("All fields must be filled.")
        else:
            # Validate contact_info
            is_phone = re.fullmatch(r"\d{10}", contact_info)
            is_email = re.fullmatch(r"[^@]+@[^@]+\.[^@]+", contact_info)

            if not (is_phone or is_email):
                st.error("Contact Info must be a valid 10-digit phone number or a valid email address.")
            else:
                try:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO patients (name, age, blood_type, organ_needed, contact_info, urgency) VALUES (%s, %s, %s, %s, %s, %s)",(name, age, blood_type, organ_needed, contact_info, urgency))
                    conn.commit()
                    st.success(f"{name} registered successfully!")
                except Error as e:
                    st.error(f"Database Error: {e}")
                finally:
                    if conn.is_connected():
                        cursor.close()
                        conn.close()

    # ===== After form: Show Organ Demand Chart =====
    st.subheader("Current Organ Demand Overview")

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT organ_needed, COUNT(*) FROM patients GROUP BY organ_needed")
        data = cursor.fetchall()

        if data:
            df = pd.DataFrame(data, columns=["Organ", "Count"])
            st.bar_chart(df.set_index("Organ"))
        else:
            st.info("No data available yet.")
    except Error as e:
        st.error(f"Database Error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


# View all recipients
def view_recipients():
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] {
            background-color: #003153;  /* Dark navy blue background */
        }

        .table-container {
            background-color: #f1f1f1;  /* Light background color for the table */
            padding: 20px;
            border-radius: 10px;
            border: 2px solid #003366;  /* Thick border around the table */
        }

        .table-container table {
            width: 100%;
            border-collapse: collapse;
        }

        .table-container th, .table-container td {
            padding: 10px;
            text-align: left;
            border: 1px solid #003366;
        }
       
        .table-container th {
            background-color: #003366;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.subheader("All Registered Recipients")
   
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients")
        data = cursor.fetchall()
        col_names = [desc[0] for desc in cursor.description]

        if data:
            df = pd.DataFrame(data, columns=col_names)
            # Display the table with custom styles
            st.markdown('<div class="table-container">', unsafe_allow_html=True)
            st.dataframe(df, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No recipients found.")
       
        cursor.close()
        conn.close()
   
    except Error as e:
        st.error(f"Database Error: {e}")
   
    # ===== After form: Show Organ Demand Chart =====
    st.subheader("Current Organ Demand Overview")
   
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT organ_needed, COUNT(*) FROM patients GROUP BY organ_needed")
        data = cursor.fetchall()

        if data:
            df = pd.DataFrame(data, columns=["Organ", "Count"])
            st.bar_chart(df.set_index("Organ"))
        else:
            st.info("No data available yet.")
    except Error as e:
        st.error(f"Database Error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Search recipient by ID
def search_recipient():
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] {
            background-color:  #003153;
        }

        .title {
            font-size: 48px;
            font-weight: bold;
            text-align: center;
            color: white;
            background: linear-gradient(45deg, #ff5c8d, #872657);
            -webkit-background-clip: text;
            background-clip: text;
            padding: 20px;
            margin-bottom: 30px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.subheader("Search Recipient")

    recipient_id = st.number_input("Enter Recipient ID", min_value=1)

    if st.button("Search"):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM patients WHERE patient_id = %s", (recipient_id,))
            data = cursor.fetchone()

            if data:
                df = pd.DataFrame([data], columns=["ID", "Name", "Age", "Blood Type", "Organ Needed", "Contact Info", "Urgency", "Compatible"])
                st.table(df)
            else:
                st.warning("Recipient not found.")
        except Error as e:
            st.error(f"Database Error: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    # ===== After form: Show Organ Demand Chart =====
    st.subheader("Current Organ Demand Overview")

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT organ_needed, COUNT(*) FROM patients GROUP BY organ_needed")
        data = cursor.fetchall()

        if data:
            df = pd.DataFrame(data, columns=["Organ", "Count"])
            st.bar_chart(df.set_index("Organ"))
        else:
            st.info("No data available yet.")
    except Error as e:
        st.error(f"Database Error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


# Update recipient details
def update_recipient():
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] {
            background-color:  #003366;
        }

        .title {
            font-size: 48px;
            font-weight: bold;
            text-align: center;
            color: white;
            background: linear-gradient(45deg, #ff5c8d, #872657);
            -webkit-background-clip: text;
            background-clip: text;
            padding: 20px;
            margin-bottom: 30px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.subheader("Update Recipient")

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT patient_id, name FROM patients")
        recipients = cursor.fetchall()

        if not recipients:
            st.warning("No recipients available to update.")
            return

        options = [f"{r[0]} - {r[1]}" for r in recipients]
        selected = st.selectbox("Choose Recipient", options)
        selected_id = int(selected.split(" - ")[0])

        cursor.execute("SELECT * FROM patients WHERE patient_id = %s", (selected_id,))
        data = cursor.fetchone()

        if data:
            name = st.text_input("Name", value=data[1])
            age = st.number_input("Age", min_value=1, value=data[2])
            blood_type = st.selectbox("Blood Type", blood_groups, index=blood_groups.index(data[3]))
            organ_needed = st.selectbox("Organ Needed", ["Kidney", "Heart", "Liver","Lungs","Pancreas"])
            contact_info = st.text_input("Contact Info", value=data[5])
            urgency = st.slider("Urgency", min_value=1, max_value=10, value=data[6], step=1, help="Set urgency level from 1 to 10")
           
            # Handle potential invalid data[7] value for compatibility
            #compatible_value = data[7]
            #if compatible_value not in ["Yes", "No"]:
                #compatible_value = "No"  # Default value if data[7] is invalid or not "Yes" / "No"
           
            #compatible = st.selectbox("Compatible", ["Yes", "No"], index=["Yes", "No"].index(compatible_value))

            if st.button("Update"):
                # Basic non-empty validation
                if not name or not blood_type or not organ_needed or not contact_info:
                    st.error("All fields must be filled.")
                else:
                    # Contact Info Validation
                    is_phone = re.fullmatch(r"\d{10}", contact_info)
                    is_email = re.fullmatch(r"[^@]+@[^@]+\.[^@]+", contact_info)

                    if not (is_phone or is_email):
                        st.error("Contact Info must be a valid 10-digit phone number or a valid email address.")
                    else:
                        # Optionally: restrict organ types
                        allowed_organs = ["Kidney", "Heart", "Liver", "Lungs", "Pancreas"]
                        if organ_needed.capitalize() not in allowed_organs:
                            st.error(f"Organ Needed must be one of: {', '.join(allowed_organs)}")
                        else:
                            update_query = """UPDATE patients SET name=%s, age=%s, blood_type=%s, organ_needed=%s, contact_info=%s, urgency=%s WHERE patient_id=%s"""
                            cursor.execute(update_query, (name, age, blood_type, organ_needed.capitalize(), contact_info, urgency, selected_id))
                            conn.commit()
                            st.success("Recipient updated successfully.")

        else:
            st.error("Selected recipient not found.")

    except Error as e:
        st.error("Error while updating.")
        st.exception(e)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

    # ===== After form: Show Organ Demand Chart =====
    st.subheader("Current Organ Demand Overview")

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT organ_needed, COUNT(*) FROM patients GROUP BY organ_needed")
        data = cursor.fetchall()

        if data:
            df = pd.DataFrame(data, columns=["Organ", "Count"])
            st.bar_chart(df.set_index("Organ"))
        else:
            st.info("No data available yet.")
    except Error as e:
        st.error(f"Database Error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def get_patient_data_by_id(patient_id):
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] {
            background-color:   #013220 ;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE patient_id = %s", (patient_id,))
    patient_data = cursor.fetchone()
    conn.close()

    if patient_data:
        return {
            "donor_id": patient_data[0],
            "name": patient_data[1],
            "age": patient_data[2],
            "blood_type": patient_data[3],
            "organ_type": patient_data[4],
            "contact_info": patient_data[5]
        }
    else:
        return None


# Delete a recipient
def delete_recipient():
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] {
            background-color: #003153;
        }

        .title {
            font-size: 48px;
            font-weight: bold;
            text-align: center;
            color: white;
            background: linear-gradient(45deg, #ff5c8d, #872657);
            -webkit-background-clip: text;
            background-clip: text;
            padding: 20px;
            margin-bottom: 30px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.subheader("Delete Recipient")
    recipient_id = st.number_input("Enter Recipient ID to Delete", min_value=1)

    if st.button("Delete"):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM patients WHERE patient_id = %s", (recipient_id,))
            conn.commit()

            if cursor.rowcount > 0:
                st.success(f"Recipient with ID {recipient_id} deleted.")
            else:
                st.warning("No such recipient found.")
        except Error as e:
            st.error(f"Database Error: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    # ===== After form: Show Organ Demand Chart =====
    st.subheader("Current Organ Demand Overview")

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT organ_needed, COUNT(*) FROM patients GROUP BY organ_needed")
        data = cursor.fetchall()

        if data:
            df = pd.DataFrame(data, columns=["Organ", "Count"])
            st.bar_chart(df.set_index("Organ"))
        else:
            st.info("No data available yet.")
    except Error as e:
        st.error(f"Database Error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


# Streamlit UI main layout
def main():
    st.title("Lifelink - Recipient Management")

    options = [
        "Register Recipient",
        "View All Recipients",
        "Search Recipient by ID",
        "Update Recipient Details",
        "Delete Recipient"
    ]
    choice = st.sidebar.selectbox("Select Action", options)

    if choice == "Register Recipient":
        register_recipient()
    elif choice == "View All Recipients":
        view_recipients()
    elif choice == "Search Recipient by ID":
        search_recipient()
    elif choice == "Update Recipient Details":
        update_recipient()
    elif choice == "Delete Recipient":
        delete_recipient()

if __name__ == "__main__":
    main()
