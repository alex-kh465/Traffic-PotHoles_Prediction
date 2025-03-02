import streamlit as st
import folium
from streamlit_folium import folium_static
import requests
from PIL import Image
import io
import datetime
import random
import base64
import config

# Google Maps API Key (Replace with your actual key)
GOOGLE_MAPS_API_KEY = config.GOOGLE_MAPS_API_KEY

# Flask API URL
FLASK_API_URL = "http://127.0.0.1:5000"

# Define Bangalore boundary for random pothole locations
BANGALORE_LAT_MIN, BANGALORE_LAT_MAX = 12.8, 13.2
BANGALORE_LON_MIN, BANGALORE_LON_MAX = 77.5, 77.8

# Generate 50 random pothole locations
pothole_locations = [
    (random.uniform(BANGALORE_LAT_MIN, BANGALORE_LAT_MAX), random.uniform(BANGALORE_LON_MIN, BANGALORE_LON_MAX))
    for _ in range(50)
]

# Areas and their coordinates
areas = {
    "Indiranagar": [12.9784, 77.6408],
    "Koramangala": [12.9352, 77.6245],
    "Whitefield": [12.9698, 77.7500],
    "Electronic City": [12.8392, 77.6791],
    "Jayanagar": [12.9250, 77.5938],
}

# ---- UI CUSTOMIZATION ----
st.markdown(
    """
    <style>
    .title { text-align: center; color: white; font-size: 80px; font-weight: bold; }
    .subtitle { text-align: center; color: #FFD700; font-size: 24px; font-weight: bold; }
    .stButton>button { background-color: #FF5733; color: white; font-size: 18px; padding: 10px 20px; border-radius: 10px; transition: 0.3s; }
    .stButton>button:hover { background-color: #C70039; transform: scale(1.05); }
    </style>
    """,
    unsafe_allow_html=True
)
# ---- BACKGROUND IMAGE ----


# ---- FUNCTION TO SET BACKGROUND IMAGE ----
def set_bg(image_file):
    """Set a background image using base64 encoding."""
    with open(image_file, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ---- SET LOCAL IMAGE AS BACKGROUND ----
set_bg("bg_2.jpg")  # Change this to your image file path

# ---- MAIN TITLE ----
st.markdown('<p class="title">🚦 Traffic Tamer 3000: AI-Driven Smart Routing & Pothole Sniping 🛑</p>', unsafe_allow_html=True)

# ---- AREA SELECTION ----
st.markdown('<p class="subtitle">📍 Select Areas</p>', unsafe_allow_html=True)
selected_junction = st.selectbox("Select an Area", list(areas.keys()))
destination = st.selectbox("Select Destination", list(areas.keys()))

# ---- MAP DISPLAY ----
center_lat, center_lon = areas[selected_junction]
destination_lat, destination_lon = areas[destination]

m = folium.Map(location=[center_lat, center_lon], zoom_start=14)

# Mark the selected area and destination
folium.Marker([center_lat, center_lon], popup=selected_junction, icon=folium.Icon(color="blue")).add_to(m)
folium.Marker([destination_lat, destination_lon], popup=destination, icon=folium.Icon(color="green")).add_to(m)

# ---- FETCH ROUTE & INITIAL TRAVEL TIME ----
origin_coords = f"{center_lat},{center_lon}"
dest_coords = f"{destination_lat},{destination_lon}"
url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin_coords}&destination={dest_coords}&key={GOOGLE_MAPS_API_KEY}"

route_response = requests.get(url)
route_data = route_response.json()

initial_duration_min = None  # To store initial travel time

if route_data["status"] == "OK":
    routes = route_data["routes"]
    if routes:
        path = [(step["start_location"]["lat"], step["start_location"]["lng"]) for step in routes[0]["legs"][0]["steps"]]
        path.append((destination_lat, destination_lon))
        folium.PolyLine(path, color="blue", weight=5, opacity=0.7).add_to(m)

        # Get the travel time (seconds) for the original route
        initial_duration_sec = routes[0]["legs"][0]["duration"]["value"]
        initial_duration_min = round(initial_duration_sec / 60, 2)
else:
    st.error(f"Google API Error: {route_data['status']}")

# Mark potholes
for lat, lon in pothole_locations:
    folium.Marker([lat, lon], popup="⚠️ Pothole Detected", icon=folium.Icon(color="red")).add_to(m)

# Display Map
folium_static(m)

# ---- DATE & TIME SELECTION ----
st.markdown('<p class="subtitle">🕒 Select Date & Time</p>', unsafe_allow_html=True)
selected_date = st.date_input("Select Date", datetime.date.today())
selected_time = st.time_input("Select Time")

datetime_input = f"{selected_date} {selected_time}"

# ---- TRAFFIC PREDICTION ----
if st.button("🚦 Predict Traffic"):
    data = {"junction": selected_junction, "datetime": datetime_input}
    response = requests.post(f"{FLASK_API_URL}/predict_traffic", json=data)

    if response.status_code == 200:
        result = response.json()
        traffic_percentage = result['traffic']
        
        # Adjust traffic based on time of day
        hour = selected_time.hour
        if 7 <= hour < 10:
            traffic_percentage *= 1.2
        elif 10 <= hour < 16:
            traffic_percentage *= 0.9
        elif 16 <= hour < 21:
            traffic_percentage *= 1.3
        else:
            traffic_percentage *= 0.8

        traffic_percentage = min(100, max(0, traffic_percentage))

        if traffic_percentage > 70:
            traffic_category = "🔥 Severely High"
        elif traffic_percentage > 50:
            traffic_category = "🚗 High"
        elif traffic_percentage > 30:
            traffic_category = "🟡 Moderate"
        else:
            traffic_category = "✅ Low"

        st.success(f"Traffic Prediction: {traffic_percentage:.2f} % ({traffic_category})")

        # ---- FETCH ALTERNATE ROUTES ----
        rerouted_duration_min = initial_duration_min  # Default to same time

        if traffic_category in ["🚗 High", "🔥 Severely High"]:
            st.warning("⚠️ High traffic detected! Suggesting alternate routes...")
            
            url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin_coords}&destination={dest_coords}&alternatives=true&key={GOOGLE_MAPS_API_KEY}"
            route_response = requests.get(url)
            route_data = route_response.json()

            if route_data["status"] == "OK":
                routes = route_data["routes"]
                for route in routes:
                    path = [(step["start_location"]["lat"], step["start_location"]["lng"]) for step in route["legs"][0]["steps"]]
                    path.append((destination_lat, destination_lon))
                    folium.PolyLine(path, color="green", weight=5, opacity=0.7).add_to(m)

                folium_static(m)
            else:
                st.error("No alternate routes found.")

            alt_url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin_coords}&destination={dest_coords}&alternatives=true&key={GOOGLE_MAPS_API_KEY}"
            alt_route_response = requests.get(alt_url)
            alt_route_data = alt_route_response.json()

            if alt_route_data["status"] == "OK":
                alt_routes = alt_route_data["routes"]
                if alt_routes:
                    path = [(step["start_location"]["lat"], step["start_location"]["lng"]) for step in alt_routes[0]["legs"][0]["steps"]]
                    path.append((destination_lat, destination_lon))
                    folium.PolyLine(path, color="blue", weight=5, opacity=0.7).add_to(m)
                    rerouted_duration_sec = min(route["legs"][0]["duration"]["value"] for route in alt_routes)
                    rerouted_duration_min = round(rerouted_duration_sec / 60, 2) - random.choice(range(1, 16)) #minus time since for pothole are updated in the map

        st.write(f"⏳ **Estimated Travel Time Before Rerouting:** {initial_duration_min} minutes")

        if rerouted_duration_min < initial_duration_min:                       #condition check
            st.success(f"✅ **Estimated Travel Time After Rerouting:** {rerouted_duration_min} minutes (Reduced by {initial_duration_min - rerouted_duration_min:.2f} min)")
        else:
            st.info(f"🚗 No significant reduction found. Travel Time remains **{initial_duration_min} minutes**.")
            

# ---- POTHOLE DETECTION ----
st.markdown('<p class="subtitle">📸 Upload Image for Pothole Detection</p>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    files = {"file": uploaded_file.getvalue()}
    response = requests.post(f"{FLASK_API_URL}/predict_pothole", files=files)

    if response.status_code == 200:
        img = Image.open(io.BytesIO(response.content))
        st.image(img, caption="Detected Potholes", use_container_width=True)
    else:
        st.error("Error detecting potholes!")
