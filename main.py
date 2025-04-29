import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from modules.donor import register_donor, view_donors, update_donor, delete_donor, search_donor, plot_donor_data
from modules.recipient import register_recipient, view_recipients, update_recipient, delete_recipient, search_recipient
from Live_tracker.tracker import update_tracker
from ml.predict import predict_match  # ML model


def set_sidebar_style():
    st.markdown("""
    <style>
    /* Sidebar background and border */
    [data-testid="stSidebar"] {
        background: linear-gradient(to bottom, #f8edeb, #fcd5ce, #fae1dd);
        border-right: 2px solid #6a0572;
        padding-top: 0rem !important;
        margin-top: 0rem !important;
    }
    /* Fix the internal content's margin */
    [data-testid="stSidebarContent"] {
        padding-top: 0rem !important;
        margin-top: 0rem !important;
    }
    /* Title and paragraph margin */
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] p {
        color: #6a0572;
        margin-bottom: 0.2rem;
        margin-top: 0rem;
    }
    /* Radio buttons design */
    div[data-baseweb="radio"] > div {
        background-color: #ffe6f0;
        padding: 10px;
        border-radius: 10px;
        margin-top: 0px;
    }
    label[data-testid="stMarkdownContainer"] > div {
        background-color: #ffc8dd;
        padding: 8px;
        border-radius: 8px;
        margin-bottom: 5px;
        cursor: pointer;
    }
    label[data-testid="stMarkdownContainer"] > div:hover {
        background-color: #ffafcc;
        color: white;
    }
    input:checked + div {
        background-color: #ff70a6 !important;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)


def sidebar_menu():
    with st.sidebar:
        st.markdown(
            "<h1 style='margin-bottom: 0.2rem; margin-top: 0rem;'>Lifelink Navigation 🚀</h1>", unsafe_allow_html=True)
        st.markdown("<hr style='margin: 0.2rem 0;'>", unsafe_allow_html=True)
        st.markdown(
            "<p style='font-weight:bold; font-size: 16px; margin-bottom: 0.2rem;'>Choose an option:</p>", unsafe_allow_html=True)

        menu_options = [
            "🏠 Home",
            "💉 Register Donor",
            "🩺 Register Recipient",
            "📊 Live Tracker",
            "🧪 Match Donor & Recipient",
            "🤲 Register for Pledge",
            "❓ FAQ",
            "ℹ️ About Us"
        ]
        selected = st.radio("", menu_options)

        st.markdown("<br>", unsafe_allow_html=True)

        st.image("download.gif", caption="Give the Gift of Life ❤️",
                 use_container_width=True)

        st.markdown("""
        <div style='background: linear-gradient(to right, #ffafbd, #ffc3a0); padding: 10px; border-radius: 10px; text-align: center; margin-top: 5px;'>
            <p style='color: #5a189a; font-size:16px;'>Together, We Can Save Lives 🌟</p>
        </div>
        """, unsafe_allow_html=True)

    return selected


def home_page():
    st.markdown("""
        <style>
            /* Apply dark purple background to the entire page */
            body, .reportview-container, .block-container, .stApp {
                background-color: #013220;  !important;
            }

            /* Ensure text is white for visibility */
            .stText, .stMarkdown, .stSubheader, .stWrite, .stCode {
                color: white !important;
            }
        </style>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div style="background: linear-gradient(to right, #003366, #00bcd4); padding: 15px; border-radius: 10px; margin-bottom: 15px;">
        <h1 style="text-align: center; color: white;">❤️ Lifelink - Saving Lives, One Organ at a Time</h1>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div style='background-color: background: linear-gradient(to right, #ffffff, #f5f5dc); padding: 20px; border-radius: 10px; margin-top: 10px;'>
        <h2 style='color: #f5f5dc;'>Welcome to Lifelink!</h2>
        <p style='font-size:18px; color:  #FFDAB9;'>
            At Lifelink, we bridge the gap between organ donors and patients in urgent need. 
            Using technology and AI, we ensure faster, smarter matches. Together, we can give the gift of life. 💖
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.image("organ_donation.gif", use_container_width=True,
             caption="Give the Gift of Life - Donate Organs")

    st.markdown("## 📊 Success Stories of organ transplant Recipients")

    st.image("image.png", width=700,
             caption="A new beginning, thanks to the gift of life")
    st.image("s2.jpg", width=700,  caption="Where hope meets healing")
    st.image("s3.jpg", width=700,
             caption="One donor, one miracle-countless tomorrows")
    st.image("s4.jpg", width=700,  caption="Heroes are'nt born they are made")
    st.image("s5.jpg", width=700,  caption="Donate Life")


def donor_section():
    # Set the background color and title section
    st.markdown("""
    <div style="background: linear-gradient(to right, #1b5e20, #8bc34a); padding: 15px; border-radius: 10px; margin-bottom: 15px;">
        <h1 style="text-align: center; color: white;">❤️ Lifelink - Saving Lives, One Organ at a Time</h1>
    </div>
""", unsafe_allow_html=True)

    # Create two columns for the options and the image
    col1, col2 = st.columns([1, 3])  # Adjust the column ratio as needed

    # Column 1: Donor options
    with col1:
        st.subheader("Donor Actions")
        task = st.radio("Select Action", [
                        "Register Donor", "View Donors", "Search Donor", "Update Donor", "Delete Donor"])

        # Don't call the donor functions inside the columns, call them after
        # These will be rendered outside the column context
        if task == "Register Donor":
            st.session_state.donor_action = "register"
        elif task == "View Donors":
            st.session_state.donor_action = "view"
        elif task == "Search Donor":
            st.session_state.donor_action = "search"
        elif task == "Update Donor":
            st.session_state.donor_action = "update"
        elif task == "Delete Donor":
            st.session_state.donor_action = "delete"

    # Column 2: Image (Replace 'donor.jpg' with the actual path to your image)
    with col2:
        with col2:
            st.image("donor.jpg", width=440,  caption="Donate Life")

    # Close the columns section explicitly so that content below takes full width
    # Force a break after the columns
    st.markdown("<br>", unsafe_allow_html=True)

    # Now, handle the donor action below the columns
    if 'donor_action' in st.session_state:
        action = st.session_state.donor_action

        if action == "register":
            register_donor()  # This is where the register donor function is called
        elif action == "view":
            view_donors()
        elif action == "search":
            search_donor()
        elif action == "update":
            update_donor()
        elif action == "delete":
            delete_donor()


def recipient_section():
    st.markdown("""
    <div style="background: linear-gradient(to right, #008080, #4682B4); padding: 15px; border-radius: 10px; margin-bottom: 15px;">
        <h1 style="text-align: center; color: white;">❤️ Lifelink - Saving Lives, One Organ at a Time</h1>
    </div>
""", unsafe_allow_html=True)
    # Set the background color and title section

    # Create two columns for the options and the image
    col1, col2 = st.columns([1, 3])  # Adjusted column ratio

    # Column 1: Recipient options
    with col1:
        st.subheader("Recipient Actions")
        task = st.radio("Select Action", ["Register Recipient", "View Recipients",
                        "Search Recipient", "Update Recipient", "Delete Recipient"])

    # Column 2: Image (this can be any image related to the recipient)
    with col2:
        st.image("organ3.jpg", width=450, caption="Recipient Life")

    # Clear the columns so that the content below occupies full width
    st.empty()

    # Now call the function based on the task selected
    if task == "Register Recipient":
        register_recipient()
    elif task == "View Recipients":
        view_recipients()
    elif task == "Search Recipient":
        search_recipient()
    elif task == "Update Recipient":
        update_recipient()
    elif task == "Delete Recipient":
        delete_recipient()
 # Reset the layout so content will span full width


def live_tracker_section():
    st.markdown("""
        <style>
            /* Apply dark olive green background to the entire page */
            body, .reportview-container, .block-container, .stApp {
                background-color: #013220 !important;
            }

            /* Ensure text is white for visibility */
            .stText, .stMarkdown, .stSubheader, .stWrite, .stCode {
                color: white !important;
            }

            

        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background: linear-gradient(to right, #1b5e20, #8bc34a); padding: 15px; border-radius: 10px; margin-bottom: 15px;">
        <h1 style="text-align: center; color: white;">❤️ Lifelink - Saving Lives, One Organ at a Time</h1>
    </div>
""", unsafe_allow_html=True)

    #st.subheader("Live Tracker")
    try:
        update_tracker()
    except Exception as e:
        st.error(f"An error occurred while fetching live tracker data: {e}")
    st.image("track.webp", caption="Life-saving Connection",
             use_container_width=True)


def match_donor_recipient():
    import pickle
    import pandas as pd

    st.markdown("""
        <style>
            body, .reportview-container, .block-container, .stApp {
                background-color: #3E2723 !important;
            }
            .stText, .stMarkdown, .stSubheader, .stWrite, .stCode {
                color: white !important;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background: linear-gradient(to right, #b08d57, #6a4e23); padding: 15px; border-radius: 10px; margin-bottom: 15px;">
        <h1 style="text-align: center; color: white;">❤️ Lifelink - Saving Lives, One Organ at a Time</h1>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("🧪 Donor-Recipient Matching (ML Powered)")

    with st.form("match_form"):
        st.write("### Enter Recipient Info")

        recip_blood = st.selectbox("Recipient Blood Type", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        recip_organ = st.selectbox("Organ Needed", ["Kidney", "Liver", "Heart", "Lungs"])
        recip_age = st.slider("Recipient Age", 1, 100, 30)
        urgency = st.slider("Urgency Level (1 = Low, 10 = High)", 1, 10, 5)

        submit = st.form_submit_button("Check Compatibility")

    if submit:
        recipient_info = {
            "blood_type": recip_blood,
            "organ_type": recip_organ,
            "age": recip_age,
            "urgency": urgency
        }

        result = predict_match(recipient_info)
        print(f"Result from predict_match: {result}")

        if "error" in result:
            st.error(f"⚠️ Error: {result['error']}")
        elif result["match"]:
            st.success(f"✅ Match Found! {result['message']}")
            st.write("🔍 Donor Info:")
            st.write(result["donor"])
            st.write(f"📈 Confidence: {result['confidence']}%")
        else:
            st.warning("❌ No compatible match found. Please try again.")

    # Add an image at the end
    st.image("match.jpg", caption="Life-saving Connection", use_container_width=True)

def donor_data_visualization_section():
    st.markdown("""
    <div style="background: linear-gradient(to right, #ff6b6b, #f06595, #cc5de8); padding: 15px; border-radius: 10px; margin-bottom: 15px;">
        <h1 style="text-align: center; color: white;">❤️ Lifelink - Saving Lives, One Organ at a Time</h1>
    </div>
    """, unsafe_allow_html=True)
    st.subheader("📊 Donor Data Visualization")
    df = pd.read_csv('donor_data.csv')  # Load donor data here
    plot_choice = st.selectbox("Visualize Donor Data By", [
                               "Age", "Blood Group", "Organ Type"])
    plot_donor_data(df, plot_choice)


def register():
    # Set the title and introductory heading
    st.markdown("""
    <div style="background-color: #2C6B3D; padding: 20px; border-radius: 10px; text-align: center;">
        <h1 style="color: white;">Save Lives Today - Organ Donation Pledge</h1>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Display an impactful image related to organ donation
    st.image("pledge.jpg", use_container_width=True)

    # Add an introductory paragraph about organ donation
    st.markdown("""
        Organ donation saves lives. By registering, you can help someone in need of an organ transplant and offer them a second chance at life. 
        The process is simple, and your decision to donate can make a huge impact. Join thousands of others in this noble cause. 🤲
    """)

    # Add a clear call to action
    st.markdown("""
        **Please Register for the Organ Donation Pledge by clicking the link below.**
    """)

    # Provide the URL for the registration (e.g., link to a Google Form or dedicated registration page)
    st.markdown("""
        [Register for Organ Donation Pledge](https://notto.abdm.gov.in/)
    """)

    # Add a message encouraging people to pledge
    st.markdown("""
        By clicking the link and filling out the form, you're committing to giving the gift of life. Your action today could save someone’s tomorrow.
    """)

    # Optionally, add a few impact statistics or quotes
    st.markdown("""
        ## Impact of Your Pledge
        - Over 120,000 people are waiting for organ transplants in the United States alone.
        - One organ donor can save up to 8 lives.
        - Your pledge today can make a difference tomorrow.
    """)

    # Provide a thank-you message after the registration
    if st.button("I Have Registered"):
        st.success("Thank you for your pledge! You are now part of a life-saving movement. 💖")

    st.image("state.jpg", caption="State wise Demographics", use_container_width=True)
    st.image("chart.jpg", caption="Pie charts depicting actual scenario", use_container_width=True)

# Call the register function at the appropriate place in your script









def play_video_with_speed():
    # Path to the locally stored video file
    video_path = "video.mp4"  # Update with your actual file path

 
    
    
    # Render the video in Streamlit using HTML
    st.video(video_path)

# Call the function to display the video with autoplay



# Cal


# Call the function to display the video with the specified speed




# Call the function to display the video with the specified speed



# Call the function to display the video


# Call the function to display the video with the specified speed


def about_us():
    st.markdown("""
    <div style="background: linear-gradient(to right, #2f3b52, #5f6d84); padding: 15px; border-radius: 10px; margin-bottom: 15px;">
        <h1 style="text-align: center; color: white;">❤️ Life Link</h1>
    </div>
""", unsafe_allow_html=True)
    # Set the background color for the entire page and adjust text color for readability
    st.markdown("""
    <style>
            /* Apply dark olive green background to the entire page */
            body, .reportview-container, .block-container, .stApp {
                background-color:#353839 !important;
            }

    h2, h3, h4 {
        color: #ffffff;  /* White color for headers */
    }

    p {
        color: #dcdcdc;  /* Slightly darker grey for paragraph text */
    }
    
    .main {
        padding: 20px;
        border-radius: 10px;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='main'>", unsafe_allow_html=True)  # Apply the background to the main content

    # Mission, Vision, and Strategy
    st.markdown("<h2>Our Mission, Vision & Strategy 🌟</h2>", unsafe_allow_html=True)
    st.markdown("""
    <p>
    <strong>Mission:</strong> Our mission is to create a world where no life is lost due to a lack of organ donation awareness and action. We aim to educate individuals and encourage them to contribute to saving lives through organ donation.
    </p>
    <p>
    <strong>Vision:</strong> Our vision is to make organ donation a common practice and ensure that every eligible person pledges to donate. We strive for a future where organ transplants are accessible to everyone in need.
    </p>
    <p>
    <strong>Strategy:</strong> We aim to raise awareness through campaigns, conduct educational workshops, collaborate with medical professionals, and create a community of people committed to organ donation. Our strategy includes both online and offline efforts to engage people effectively.
    </p>
    """, unsafe_allow_html=True)

    # Team Photo
    st.markdown("<h3>Meet Our Team 👥</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])  # Left, Center, Right

    with col2:
        st.image("AboutUs.jpg", caption="Our Dedicated Team", width=400)
    # Emotional Quote or Poem
    st.markdown("<h4>An Emotional Quote 💖</h4>", unsafe_allow_html=True)
    st.markdown("""
    <p style='text-align: center; font-style: italic;'>
    "The greatest gift you can give someone is the gift of life. Through organ donation, we become part of something bigger than ourselves. We leave behind not just memories but a legacy of hope." 🌈
    </p>
    """, unsafe_allow_html=True)
    play_video_with_speed()

    # Events and Activities
    st.markdown("<h3>Our Events & Activities 📅</h3>", unsafe_allow_html=True)

    st.markdown("""
    <h4>1. Online Meet for Organ Donation Awareness 🩺</h4>
    <p>We conducted an online meet to raise awareness about organ donation. The event included informative sessions on the importance of organ donation, the process, and real-life success stories. We had a panel of doctors, social workers, and organ recipients sharing their experiences.</p>
    """, unsafe_allow_html=True)
    st.image("a2.jpg", use_container_width=True)
    st.markdown("""
    <h4>2. Pledge for Organ Donation in College 📝</h4>
    <p>The second event focused on encouraging students to take the pledge for organ donation. We had a pledge-taking ceremony in our college, where we educated students about the significance of organ donation and how their commitment could save lives. This event helped in spreading the message of hope and selflessness.</p>
    """, unsafe_allow_html=True)
    st.image("a3.jpg", caption="Pledge for Organ Donation in College", use_container_width=True)

    # Close the content div
    st.markdown("</div>", unsafe_allow_html=True)




def faq_section():
    st.markdown("""
        <style>
            /* Apply dark olive green background to the entire page */
            body, .reportview-container, .block-container, .stApp {
                background-color: #333333 !important;
            }

            /* Ensure text is white for visibility */
            .stText, .stMarkdown, .stSubheader, .stWrite, .stCode {
                color: white !important;
            }

            

        </style>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div style="background: linear-gradient(to right, #2f3b52, #5f6d84); padding: 15px; border-radius: 10px; margin-bottom: 15px;">
        <h1 style="text-align: center; color: white;">❤️ Organ Donation FAQ</h1>
    </div>
""", unsafe_allow_html=True)

    st.image("faq.png", caption="Life-saving Connection",
             use_container_width=True)

    # Define the questions and answers
    faq_data = [
        ("What is organ and tissue donation?",
         "Organ donation means that a person during his/her lifetime pledges that after his/her death, organs from his/her body can be used for transplant to save or improve the life of someone in need. This can include organs like kidneys, heart, liver, lungs, etc."),

        ("How can I become an organ donor?",
         "You can become an organ donor by registering with your local or national organ registry or by expressing your intent to your family so they can make the decision for you when needed."),

        ("What organs can be donated?",
         "Organs that can be donated include kidneys, liver, heart, lungs, pancreas, and intestines. Additionally, tissues like corneas, skin, and bone marrow can also be donated."),

        ("Are there any age restrictions for organ donation?",
         "There is no specific age limit for organ donation. The suitability of organs for donation depends on the organ's health and condition, not the donor's age."),

        ("Can I donate an organ while I'm still alive?",
         "Yes, living people can donate certain organs such as a kidney or part of their liver. This can be done if they are in good health and meet the criteria set by medical professionals."),

        ("How long does it take to match a donor with a recipient?",
         "The matching process varies depending on factors like blood type, organ size, medical condition, and geographic location. The process can take anywhere from a few days to several months."),

        ("Is organ donation free of cost for the donor's family?",
         "Yes, organ donation is free of cost for the donor’s family. The costs of the organ recovery process are covered by the transplant center or the recipient's insurance."),

        ("What happens if I die in an accident and am an organ donor?",
         "If you die in an accident and are registered as an organ donor, your organs will be evaluated to see which ones are viable for transplant. The decision to donate will be made by medical professionals."),

        ("How can I revoke my organ donation decision?",
         "You can revoke your organ donation decision by contacting your local organ donation registry or informing your family about your new decision. It is essential to update your preferences if you change your mind."),

        ("Is there any medical risk for organ donors?",
         "Living organ donors face some medical risks, including complications from surgery. However, a thorough medical evaluation is performed before donation to ensure the risks are minimal and the donor’s health is protected."),

        # Additional unique questions
        ("Can I donate organs if I have a medical condition?",
         "Certain medical conditions may affect your eligibility to donate. Each case is evaluated individually based on the health of the organs and the donor's medical history."),

        ("How is organ donation different from organ transplantation?",
         "Organ donation refers to giving organs for transplantation, while organ transplantation is the medical procedure of moving the donated organ into a recipient’s body."),

        ("Can I donate organs if I have recently been vaccinated?",
         "In most cases, recent vaccination does not affect organ donation eligibility. However, it's always best to consult with medical professionals regarding your specific situation."),

        ("What is the process for organ recovery after death?",
         "Once a person is declared brain-dead, medical professionals begin the process of organ recovery, which involves surgically removing the organs for transplantation while maintaining the donor's body functions."),

        ("How is organ donation regulated?",
         "Organ donation is regulated by national and international laws and organizations that ensure fairness, transparency, and ethical practices in the donation and transplantation process."),

        ("Are there any religious considerations regarding organ donation?",
         "Many religions support organ donation as an act of kindness and saving lives, though individual beliefs may vary. It’s important to consult with religious leaders if you have concerns."),

        ("How can I support organ donation awareness?",
         "You can support organ donation awareness by spreading information, registering as a donor, participating in campaigns, and encouraging others to register."),

        ("Can I donate organs if I have a family history of certain diseases?",
         "It depends on the disease and its impact on the organs. Medical evaluations are performed to determine if the organs are suitable for donation."),

        ("What happens if a recipient rejects an organ?",
         "If a recipient's body rejects an organ, they may need further medical treatments, such as immunosuppressive drugs, to prevent the rejection. In severe cases, another transplant may be required."),

        ("How are organ donors' families supported?",
         "Many organ donation programs offer counseling and support to the families of donors, helping them cope with the emotional aspects of the donation process.")
    ]

    # Create columns for two boxes per row
    num_columns = 2
    columns = st.columns(num_columns)

    # Loop through each FAQ and display it in a separate box
    for index, (question, answer) in enumerate(faq_data):
        col_index = index % num_columns  # Alternate between the two columns

        with columns[col_index]:
            st.markdown(f"""
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <h3 style="color: #e83e8c; font-size: 20px; font-weight: bold;">{question}</h3>
                <p style="font-size: 14px; color: #555555;">{answer}</p>
            </div>
            """, unsafe_allow_html=True)

        # Add a small space between the boxes when switching to the next row
        if col_index == num_columns - 1:
            st.markdown("<br>", unsafe_allow_html=True)

# faq_section()


def main():
    set_sidebar_style()
    selected = sidebar_menu()

    if selected == "🏠 Home":
        home_page()
    elif selected == "💉 Register Donor":
        donor_section()
    elif selected == "🩺 Register Recipient":
        recipient_section()
    elif selected == "📊 Live Tracker":
        live_tracker_section()
    elif selected == "🧪 Match Donor & Recipient":
        match_donor_recipient()
    elif selected == "❓ FAQ":
        faq_section()
    elif selected == "🤲 Register for Pledge":
        register()
    elif selected == "ℹ️ About Us":
        about_us()

    # Call the new section for donor data visualization


if __name__ == "__main__":
    main()
