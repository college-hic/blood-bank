import streamlit as st

# Set the page configuration
st.set_page_config(page_title="Karachi Blood Bank Finder", page_icon="💉", layout="centered")

# Link the CSS file to the app
st.markdown(
    """
    <style>
    @import url('css/style.css');
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit app content
st.title("💉 Karachi Blood Bank Finder")
st.write("Find the nearest blood bank in Karachi based on your location and required blood group.")

# Add a sidebar with information and contact
st.sidebar.header("About")
st.sidebar.write(
    """
    This app helps you find the nearest blood bank in Karachi based on your location and required blood group.
    Please contact the blood banks directly to confirm availability.
    """
)

st.sidebar.markdown("---")
st.sidebar.header("Contact Us")
st.sidebar.write("For inquiries, contact: support@bloodbankfinder.com")

# User input for location and blood group
st.subheader("Step 1: Select Your Location and Blood Group")
user_location = st.selectbox("Select your location", options=["Saddar", "Gulshan-e-Iqbal", "Korangi", "Clifton", "Nazimabad"])
required_blood_group = st.selectbox("Select the required blood group", options=["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])

# Simulate finding blood banks based on user input
if st.button("🔍 Find Blood Bank"):
    st.write("Displaying results for:", user_location, required_blood_group)

    # Dummy results
    st.write("### Nearby Blood Banks:")
    st.write("1. City Blood Bank\nLocation: Saddar\nAvailable Blood Groups: A+, B+, O+\nContact: 0301-1234567")
    st.write("2. LifeSaver Blood Center\nLocation: Gulshan-e-Iqbal\nAvailable Blood Groups: A+, AB-, O+\nContact: 0302-2345678")
else:
    st.info("Select your location and blood group, then click 'Find Blood Bank' to search.")
