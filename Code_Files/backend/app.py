from flask import Flask, request, jsonify,send_file
from PIL import Image
from keras.models import load_model 
from ultralytics import YOLO
import numpy as np
import pickle
import datetime
import os
from flask_cors import CORS
import io

app = Flask(__name__, static_folder="static")
CORS(app)
# Load models
traffic_model = load_model("models/lstm_traffic_model.h5")  # Keras Model
pothole_model = YOLO("models/best.pt")  # YOLO Model

# Load scaler
with open("models/scaler.pkl", "rb") as f:
    scaler = pickle.load(f)


def simulate_realistic_traffic():
    """Simulates past 24 hours of realistic traffic congestion values."""
    traffic_pattern = []
    now = datetime.datetime.now()

    for i in range(24):
        hour = (now - datetime.timedelta(hours=i)).hour

        if 7 <= hour <= 10:   # Morning Rush Hour
            traffic = np.random.uniform(80, 120)
        elif 11 <= hour <= 16:  # Afternoon Lower Traffic
            traffic = np.random.uniform(30, 60)
        elif 17 <= hour <= 20:  # Evening Rush Hour
            traffic = np.random.uniform(60, 90)
        else:  # Late Night / Early Morning (Low Traffic)
            traffic = np.random.uniform(30, 70)

        traffic_pattern.append(traffic)

    # Normalize using the same MinMaxScaler
    traffic_pattern = np.array(traffic_pattern).reshape(-1, 1)
    traffic_pattern = scaler.transform(traffic_pattern)  # Scale data
    return np.reshape(traffic_pattern, (1, 24, 1))  # Reshape for LSTM

@app.route("/predict_traffic", methods=["POST"])
def predict_traffic():
    """Predict traffic congestion using real-world traffic patterns."""
    data = request.json
    junction = data.get("junction")
    date_time = data.get("datetime")

    if not junction or not date_time:
        return jsonify({"error": "Missing junction or datetime"}), 400

    # Get realistic past 24-hour data
    X_input = simulate_realistic_traffic()

    # Predict using the LSTM model
    prediction = traffic_model.predict(X_input)
    predicted_traffic = float(scaler.inverse_transform([[prediction[0][0]]])[0][0])  # Convert back to real scale

    # Categorize traffic
    if predicted_traffic < 20:
        category = "Empty Road"
    elif predicted_traffic < 40:
        category = "Low"
    elif predicted_traffic < 60:
        category = "Moderate"
    elif predicted_traffic < 80:
        category = "High"
    else:
        category = "Severly High"



    return jsonify({
        "junction": junction,
        "datetime": date_time,
        "traffic": predicted_traffic,
        "category": category
    })
@app.route("/predict_pothole", methods=["POST"])
def predict_pothole():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Read image file into memory
    image = Image.open(file.stream)
    image = image.convert("RGB")  # Ensure correct format

    # Run YOLO inference
    results = pothole_model(image)

    # Draw bounding boxes on the image
    for result in results:
        result.save(filename="detected_potholes.jpg")  # Saves with bounding boxes

    # Convert image to bytes for returning
    img_io = io.BytesIO()
    with Image.open("detected_potholes.jpg") as img:
        img.save(img_io, "JPEG")
    img_io.seek(0)

    potholes_detected = len(results[0].boxes)

    return send_file(img_io, mimetype="image/jpeg", as_attachment=False)
if __name__ == "__main__":
    app.run(debug=True)
