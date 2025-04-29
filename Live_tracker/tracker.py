# live_tracker/tracker.py

import streamlit as st
import mysql.connector
from mysql.connector import Error
import plotly.graph_objects as go

# IMPORTANT: set page config first
st.set_page_config(page_title="LifeLink Live Tracker", layout="wide")


def update_tracker():
    st.title("🩺 Live Tracker Dashboard")

    # Connect to MySQL database
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="ananya",
            database="lifelink"
        )
        cursor = conn.cursor(dictionary=True)
    except Error as e:
        st.error(f"Error connecting to MySQL: {e}")
        return

    # Fetch donor and recipient counts
    try:
        cursor.execute("SELECT COUNT(*) as count FROM donors")
        donor_count = cursor.fetchone()['count']
    except Error as e:
        st.error(f"Error fetching donor data: {e}")
        donor_count = 0

    try:
        cursor.execute("SELECT COUNT(*) as count FROM patients")
        recipient_count = cursor.fetchone()['count']
    except Error as e:
        st.error(f"Error fetching patient data: {e}")
        recipient_count = 0

    # Only this section inside blue box
    st.markdown(
        """
        <div style="background-color: #dbeafe; padding: 30px; border-radius: 12px; color: black; margin-bottom: 30px;">
        """,
        unsafe_allow_html=True,
    )

    st.subheader("📊 Live Counts")
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.metric(label="🩸 Total Donors", value=donor_count)
    with col2:
        st.metric(label="🏥 Total Recipients", value=recipient_count)

    st.markdown("</div>", unsafe_allow_html=True)
    # blue box closed ✅

    # Now normal content without blue box
    # Display Goal Progress
    st.subheader("🎯 Donation Goals Progress")

    target_donors = 300

    st.write("Goal: 300 Donors 🚀")
    st.progress(min(donor_count / target_donors, 1.0))

    # Draw pie chart
    st.subheader("🧬 Donors vs Recipients Distribution")

    labels = ['Donors', 'Recipients']
    values = [donor_count, recipient_count]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.4)])
    fig.update_layout(title_text='Donors vs Recipients')
    st.plotly_chart(fig, use_container_width=True)

    # Recently Registered Donors
    st.subheader("🆕 Recently Registered Donors")
    try:
        cursor.execute(
            "SELECT name, blood_type, organ_type FROM donors ORDER BY donor_id DESC LIMIT 5")
        recent_donors = cursor.fetchall()
        for donor in recent_donors:
            st.write(
                f"🩸 **{donor['name']}** ({donor['blood_type']}) - Organ: {donor['organ_type']}")
    except Error as e:
        st.error(f"Error fetching recent donors: {e}")

    # Recently Registered Recipients
    st.subheader("🆕 Recently Registered Recipients")
    try:
        cursor.execute(
            "SELECT name, blood_type, organ_needed FROM patients ORDER BY patient_id DESC LIMIT 5")
        recent_recipients = cursor.fetchall()
        for patient in recent_recipients:
            st.write(
                f"🏥 **{patient['name']}** ({patient['blood_type']}) - Needs: {patient['organ_needed']}")
    except Error as e:
        st.error(f"Error fetching recent recipients: {e}")

    # Close DB connection
    cursor.close()
    conn.close()

    st.success("✅ Live data updated successfully!")
