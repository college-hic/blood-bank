import streamlit as st
import pandas as pd
from geopy.distance import geodesic

# Set the page config as the first command
st.set_page_config(page_title="Karachi Blood Bank Finder", page_icon="💉", layout="centered")

# Apply custom CSS for enhanced UI
st.markdown("""
    <style>
        /* Set background image */
        body {
            background-image: url('assets/background.jpg');
            background-size: cover;
            background-position: center;
            font-family: 'Arial', sans-serif;
        }

        /* Header styles */
        h1, h2, h3 {
            color: #ffffff;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }

        /* Button Styles */
        .stButton button {
            background-color: #FF4081;
            color: white;
            font-size: 18px;
            border-radius: 10px;
            padding: 10px 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }

        .stButton button:hover {
            background-color: #f50057;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
        }

        /* Styling the input boxes */
        .stSelectbox select, .stButton button, .stTextInput input {
            border: 2px solid #ffffff;
            border-radius: 8px;
            padding: 8px;
            font-size: 16px;
        }

        .stSelectbox select:focus, .stButton button:focus, .stTextInput input:focus {
            border-color: #FF4081;
        }

        .stSelectbox select {
            background-color: rgba(255, 255, 255, 0.7);
        }

        .stTextInput input {
            background-color: rgba(255, 255, 255, 0.7);
        }

        /* Box for displaying the nearest blood banks */
        .blood-bank-box {
            background-color: rgba(255, 255, 255, 0.8);
            border-radius: 10px;
            padding: 15px;
            margin: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        }

        .blood-bank-box h4 {
            margin-top: 0;
        }
    </style>
""", unsafe_allow_html=True)

# Blood banks data with locations, contact info, available blood groups, and coordinates
blood_banks = [
    {"name": "City Blood Bank", "location": "Saddar", "contact": "0301-1234567", "email": "citybloodbank@gmail.com", "available_blood_groups": ["A+", "A-", "B+", "O+", "O-", "AB+"], "coordinates": (24.8607, 67.0011)},
    {"name": "LifeSaver Blood Center", "location": "Gulshan-e-Iqbal", "contact": "0302-2345678", "email": "lifesaverbb@gmail.com", "available_blood_groups": ["A+", "B+", "O+", "AB+", "B-", "AB-"], "coordinates": (24.9262, 67.0927)},
    {"name": "Karachi Central Blood Bank", "location": "North Nazimabad", "contact": "0303-3456789", "email": "kcentralbb@gmail.com", "available_blood_groups": ["A-", "B-", "O-", "AB+", "AB-", "O+"], "coordinates": (24.9424, 67.0652)},
    {"name": "Fatima Blood Bank", "location": "Korangi", "contact": "0304-4567890", "email": "fatimabb@gmail.com", "available_blood_groups": ["A+", "O+", "AB+", "O-"], "coordinates": (24.8467, 67.1077)},
    {"name": "Edhi Blood Bank", "location": "Clifton", "contact": "0305-5678901", "email": "edhibb@gmail.com", "available_blood_groups": ["A+", "A-", "B+", "O+"], "coordinates": (24.8090, 67.0333)},
    {"name": "Al-Mustafa Blood Bank", "location": "Gulistan-e-Johar", "contact": "0306-6789012", "email": "almustafabb@gmail.com", "available_blood_groups": ["B+", "O-", "AB-", "AB+"], "coordinates": (24.9113, 67.1171)},
    {"name": "Indus Hospital Blood Center", "location": "Korangi", "contact": "0307-7890123", "email": "indushospital@gmail.com", "available_blood_groups": ["A-", "B-", "O+", "O-"], "coordinates": (24.8415, 67.1341)},
    {"name": "Hussaini Blood Bank", "location": "Malir", "contact": "0308-8901234", "email": "hussainibb@gmail.com", "available_blood_groups": ["A+", "B+", "AB+", "O-"], "coordinates": (24.8932, 67.1888)},
    {"name": "Pakistan Red Crescent", "location": "Gulshan-e-Iqbal", "contact": "0309-9012345", "email": "redcrescentbb@gmail.com", "available_blood_groups": ["A-", "B-", "O+", "AB+"], "coordinates": (24.9362, 67.0831)},
    {"name": "Saylani Blood Bank", "location": "Nazimabad", "contact": "0310-1234568", "email": "saylanibb@gmail.com", "available_blood_groups": ["O+", "AB-", "A+", "B+"], "coordinates": (24.9312, 67.0226)},
    {"name": "Liaquat National Blood Bank", "location": "Stadium Road", "contact": "0311-2345678", "email": "liaquatnationalbb@gmail.com", "available_blood_groups": ["A+", "A-", "O+", "B+", "B-"], "coordinates": (24.8984, 67.0811)},
    {"name": "Jinnah Hospital Blood Bank", "location": "Jamshed Town", "contact": "0312-3456789", "email": "jinnahhospitalbb@gmail.com", "available_blood_groups": ["O+", "O-", "A+", "AB+"], "coordinates": (24.8946, 67.0742)},
]

# Karachi areas with sample coordinates
locations = {
    "Saddar": (24.8556, 67.0226), "Gulshan-e-Iqbal": (24.9333, 67.0921), "North Nazimabad": (24.9551, 67.0349),
    "Korangi": (24.8450, 67.1396), "Clifton": (24.8138, 67.0328), "Gulistan-e-Johar": (24.9284, 67.1281),
    "Malir": (24.9000, 67.1855), "Nazimabad": (24.9129, 67.0363), "Stadium Road": (24.8984, 67.0811),
    "Jamshed Town": (24.8785, 67.0431),
}

blood_groups = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]

# Streamlit app UI
st.title("💉 Karachi Blood Bank Finder")
st.write("Find the nearest blood bank in Karachi based on your location and required blood group.")

# User input for location and blood group
st.subheader("Step 1: Select Your Location and Blood Group")
user_location = st.selectbox("Select your location", options=sorted(locations.keys()))
required_blood_group = st.selectbox("Select the required blood group", options=blood_groups)

# Search button to find nearby blood banks
if st.button("🔍 Find Blood Bank"):
    user_coords = locations[user_location]
    nearby_blood_banks = []

    for bank in blood_banks:
        # Check if the blood bank has the required blood group
        if required_blood_group in bank["available_blood_groups"]:
            # Calculate the distance from the user
            distance = geodesic(user_coords, bank["coordinates"]).kilometers
            nearby_blood_banks.append({**bank, "distance": distance})

    # Sort blood banks by distance
    nearby_blood_banks = sorted(nearby_blood_banks, key=lambda x: x["distance"])

    # Display results with colorful box and information
    if nearby_blood_banks:
        st.success("Nearest Blood Banks Found:")
        for bank in nearby_blood_banks:
            st.markdown(f"""
                <div class="blood-bank-box">
                    <h4>{bank['name']}</h4>
                    <p>📍 <strong>Location:</strong> {bank['location']}</p>
                    <p>📞 <strong>Contact:</strong> {bank['contact']}</p>
                    <p>📧 <strong>Email:</strong> {bank['email']}</p>
                    <p>💉 <strong>Available Blood Groups:</strong> {', '.join(bank['available_blood_groups'])}</p>
                    <p>🚗 <strong>Distance:</strong> {bank['distance']:.2f} km</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.error("No blood banks available with the required blood group in nearby areas.")
else:
    st.info("Select your location and blood group, then click 'Find Blood Bank' to search.")
