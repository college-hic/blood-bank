import streamlit as st
from geopy.distance import geodesic

# Blood banks data with locations, contact info, available blood groups, and coordinates
blood_banks = [
    {"name": "City Blood Bank", "location": "Saddar", "contact": "0301-1234567", "email": "citybloodbank@gmail.com", "available_blood_groups": ["A+", "A-", "B+", "O+", "O-", "AB+"], "coordinates": (24.8607, 67.0011)},
    {"name": "LifeSaver Blood Center", "location": "Gulshan-e-Iqbal", "contact": "0302-2345678", "email": "lifesaverbb@gmail.com", "available_blood_groups": ["A+", "B+", "O+", "AB+", "B-", "AB-"], "coordinates": (24.9262, 67.0927)},
    {"name": "Karachi Central Blood Bank", "location": "North Nazimabad", "contact": "0303-3456789", "email": "kcentralbb@gmail.com", "available_blood_groups": ["A-", "B-", "O-", "AB+", "AB-", "O+"], "coordinates": (24.9424, 67.0652)},
    # Add more blood banks as needed
]

# Karachi areas with sample coordinates
locations = {
    "Saddar": (24.8556, 67.0226), "Gulshan-e-Iqbal": (24.9333, 67.0921), "North Nazimabad": (24.9551, 67.0349),
    "Korangi": (24.8450, 67.1396), "Clifton": (24.8138, 67.0328), "Gulistan-e-Johar": (24.9284, 67.1281),
    "Malir": (24.9000, 67.1855), "Nazimabad": (24.9129, 67.0363), "Stadium Road": (24.8984, 67.0811),
    "Jamshed Town": (24.8785, 67.0431),
}

blood_groups = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]

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

# Sidebar with information and contact
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
user_location = st.selectbox("Select your location", options=sorted(locations.keys()))
required_blood_group = st.selectbox("Select the required blood group", options=blood_groups)

# Simulate finding blood banks based on user input
if st.button("🔍 Find Blood Bank"):
    user_coords = locations[user_location]
    nearby_blood_banks = []

    # Loop through blood banks to filter by available blood group and calculate distance
    for bank in blood_banks:
        if required_blood_group in bank["available_blood_groups"]:
            distance = geodesic(user_coords, bank["coordinates"]).kilometers
            nearby_blood_banks.append({**bank, "distance": distance})

    # Sort blood banks by distance
    nearby_blood_banks = sorted(nearby_blood_banks, key=lambda x: x["distance"])

    # Display results in interactive format
    if nearby_blood_banks:
        st.success("Nearest Blood Banks Found:")
        for bank in nearby_blood_banks:
            with st.container():
                st.markdown(f"""
                    <div class="blood-bank-card">
                        <h4>{bank['name']}</h4>
                        <p><strong>Location:</strong> {bank['location']}</p>
                        <p><strong>Available Blood Groups:</strong> {', '.join(bank['available_blood_groups'])}</p>
                        <p><strong>Contact:</strong> {bank['contact']}</p>
                        <p><strong>Email:</strong> {bank['email']}</p>
                        <p class="distance"><strong>Distance:</strong> {bank['distance']:.2f} km</p>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.error("No blood banks available with the required blood group in nearby areas.")
else:
    st.info("Select your location and blood group, then click 'Find Blood Bank' to search.")
