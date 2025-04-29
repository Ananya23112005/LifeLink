import pandas as pd
import streamlit as st
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns

# Function to connect to the database
def connect_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="ananya",  # Update this with your real password
        database="lifelink"
    )
    return conn

# Function to display a background image and style the page
def apply_styles():
    st.markdown("""
    <style>
    body {
        background-image: url('https://www.w3schools.com/w3images/forestbridge.jpg');
        background-size: cover;
        background-position: center;
        font-family: 'Arial', sans-serif;
    }
    .title {
        text-align: center;
        color: white;
        font-size: 36px;
        padding-top: 30px;
    }
    .info {
        background-color: rgba(255, 255, 255, 0.7);
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Function to visualize donor data
# Function to visualize donor data
def plot_donor_data(df, column):
    # Always start by creating a fresh figure
    plt.figure(figsize=(10, 6))
    
    # Check if the column exists
    if column == 'Blood Group':
        if 'blood_type' in df.columns:
            sns.countplot(data=df, x='blood_type', palette='coolwarm')
            plt.title('Distribution of Donors by Blood Group')
        else:
            st.error("Blood Type column is missing.")
    elif column == 'Age':
        if 'age' in df.columns:
            sns.histplot(df['age'], kde=True, bins=5, color='skyblue')
            plt.title('Age Distribution of Donors')
        else:
            st.error("Age column is missing.")
    elif column == 'Organ Type':
        if 'organ_type' in df.columns:
            organ_counts = df['organ_type'].value_counts()

            # Create a fresh figure for pie chart
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.pie(organ_counts, labels=organ_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("Set2", len(organ_counts)))
            ax.set_title('Distribution of Donors by Organ Type')
            ax.axis('equal')  # Keep it circular
            
            # Display the pie chart using Streamlit
            st.pyplot(fig)
            return  # Important: so that below st.pyplot(plt) doesn't run again
        else:
            st.error("Organ Type column is missing.")        
    
    # For Blood Group and Age charts
    st.pyplot(plt)

def register_donor():
    # Set the ENTIRE page background color
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] {
            background-color:  #013220 

;
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


    # Display options for donor registration (column 1) and content below
    st.subheader("Register New Donor")
    
    # Form for Donor Registration
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0)
    blood_type = st.text_input("Blood Type")
    organ_type = st.text_input("Organ Type")
    contact_info = st.text_input("Contact Info")

    if st.button("Register Donor"):
        if not name or not blood_type or not organ_type or not contact_info:
            st.error("All fields must be filled.")
        else:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(""" 
                INSERT INTO donors (name, age, blood_type, organ_type, contact_info)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, age, blood_type, organ_type, contact_info))
            conn.commit()
            st.success("Donor registered successfully!")
            cursor.close()
            conn.close()

    # Donor Data Visualization (optional)
    st.subheader("Donor Data Visualization")
    plot_choice = st.radio("Visualize Donor Data By", ['Age', 'Blood Group', 'Organ Type'])

    # Fetch donor data and display a plot
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM donors")
    data = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(data, columns=col_names)
    cursor.close()
    conn.close()

    # Plot the selected chart (using existing plot_donor_data function)
    plot_donor_data(df, plot_choice)



# 2. View All Donors
def view_donors():
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] {
            background-color: 	#013220 ;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.subheader("All Donors")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM donors")
    data = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(data, columns=col_names)
    st.dataframe(df, use_container_width=True)
    cursor.close()
    conn.close()
    st.subheader("Donor Data Visualization")
    plot_choice = st.radio("Visualize Donor Data By", ['Age', 'Blood Group', 'Organ Type'])

    # Fetch donor data and display a plot
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM donors")
    data = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(data, columns=col_names)
    cursor.close()
    conn.close()

    # Plot the selected chart (using existing plot_donor_data function)
    plot_donor_data(df, plot_choice)

# 3. Search Donor
def search_donor():
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] {
            background-color: 	#013220 ;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.subheader("Search Donor")
    query = st.text_input("Enter donor name or organ to search:")
    if st.button("Search"):
        if not query:
            st.warning("Please enter a value.")
        else:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM donors WHERE LOWER(name) LIKE LOWER(%s) OR LOWER(organ_type) LIKE LOWER(%s)",
                (f"%{query}%", f"%{query}%")
            )
            data = cursor.fetchall()
            col_names = [desc[0] for desc in cursor.description]
            if data:
                df = pd.DataFrame(data, columns=col_names)
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("No matching donors found.")
            cursor.close()
            conn.close()
            st.subheader("Donor Data Visualization")
    plot_choice = st.radio("Visualize Donor Data By", ['Age', 'Blood Group', 'Organ Type'])

    # Fetch donor data and display a plot
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM donors")
    data = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(data, columns=col_names)
    cursor.close()
    conn.close()

    # Plot the selected chart (using existing plot_donor_data function)
    plot_donor_data(df, plot_choice)

# 4. Update Donor
def update_donor():
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] {
            background-color: 	#013220 ;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.subheader("Update Donor")
    donor_id = st.text_input("Enter Donor ID to Update:")

    if donor_id:
        donor_data = get_donor_data_by_id(donor_id)

        if donor_data:
            new_name = st.text_input("Enter New Name:", value=donor_data["name"])
            new_age = st.number_input("Enter New Age:", value=donor_data["age"], min_value=18, max_value=120)
            new_blood_type = st.text_input("Enter New Blood Type:", value=donor_data["blood_type"])
            new_organ_type = st.text_input("Enter New Organ Type:", value=donor_data["organ_type"])
            new_contact_info = st.text_input("Enter New Contact Info:", value=donor_data["contact_info"])

            if st.button("Update Donor"):
                success = update_donor_data(donor_id, new_name, new_age, new_blood_type, new_organ_type, new_contact_info)

                if success:
                    st.success("Donor information updated successfully!")
                else:
                    st.error("Failed to update donor information. Please try again.")
        else:
            st.error("Donor ID not found. Please enter a valid donor ID.")
    else:
        st.warning("Please enter a donor ID to proceed.")
    st.subheader("Donor Data Visualization")
    plot_choice = st.radio("Visualize Donor Data By", ['Age', 'Blood Group', 'Organ Type'])

    # Fetch donor data and display a plot
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM donors")
    data = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(data, columns=col_names)
    cursor.close()
    conn.close()

    # Plot the selected chart (using existing plot_donor_data function)
    plot_donor_data(df, plot_choice)    

# Function to retrieve donor data from the MySQL database
def get_donor_data_by_id(donor_id):
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] {
            background-color: 	#013220 ;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM donors WHERE donor_id = %s", (donor_id,))
    donor_data = cursor.fetchone()
    conn.close()

    if donor_data:
        return {
            "donor_id": donor_data[0],
            "name": donor_data[1],
            "age": donor_data[2],
            "blood_type": donor_data[3],
            "organ_type": donor_data[4],
            "contact_info": donor_data[5]
        }
    else:
        return None

# Function to update donor data in the MySQL database
def update_donor_data(donor_id, name, age, blood_type, organ_type, contact_info):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(""" 
        UPDATE donors
        SET name = %s, age = %s, blood_type = %s, organ_type = %s, contact_info = %s
        WHERE donor_id = %s
    """, (name, age, blood_type, organ_type, contact_info, donor_id))

    conn.commit()
    if cursor.rowcount > 0:
        conn.close()
        return True
    else:
        conn.close()
        return False

# 5. Delete Donor
def delete_donor():
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] {
            background-color: 	#013220 ;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.subheader("Delete Donor")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT donor_id, name FROM donors")
    donors = cursor.fetchall()
    donor_dict = {f"{name} (ID: {id})": id for id, name in donors}
    cursor.close()
    conn.close()

    selected = st.selectbox("Select Donor to Delete", list(donor_dict.keys()))
    donor_id = donor_dict[selected]

    if st.button("Delete Donor"):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM donors WHERE donor_id = %s", (donor_id,))
        conn.commit()
        st.success(f"Donor with ID {donor_id} deleted.")
        cursor.close()
        conn.close()
    st.subheader("Donor Data Visualization")
    plot_choice = st.radio("Visualize Donor Data By", ['Age', 'Blood Group', 'Organ Type'])

    # Fetch donor data and display a plot
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM donors")
    data = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(data, columns=col_names)
    cursor.close()
    conn.close()

    # Plot the selected chart (using existing plot_donor_data function)
    plot_donor_data(df, plot_choice)    

# Main display function
def main():
    apply_styles()

    # Layout with image next to buttons
    col1, col2 = st.columns([3, 1])
    
    with col1:
        action = st.selectbox(
            "Choose an action",
            ["Register Donor", "View Donors", "Search Donor", "Update Donor", "Delete Donor"]
        )

    with col2:
        image_url = "donor.jpg"  # Replace with your image URL
        st.image(image_url, use_column_width=True)
    
    # Perform the action based on user choice
    if action == "Register Donor":
        register_donor()
        st.subheader("Donor Data Visualization")
        # Show Graph below registration form
        plot_choice = st.radio("Visualize Donor Data By", ['Age', 'Blood Group','Organ Type'])
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM donors")
        data = cursor.fetchall()
        col_names = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(data, columns=col_names)
        cursor.close()
        conn.close()
        plot_donor_data(df, plot_choice)

    elif action == "View Donors":
        view_donors()
    elif action == "Search Donor":
        search_donor()
    elif action == "Update Donor":
        update_donor()
    elif action == "Delete Donor":
        delete_donor()

if __name__ == "__main__":
    main()
