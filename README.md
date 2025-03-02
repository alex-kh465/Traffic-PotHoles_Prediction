# 🚦 Traffic & Pothole Detection System 🛣️  

![Traffic & Pothole Detection](https://images.unsplash.com/photo-1510915228340-29c85a43dcfe)  

## 📌 Project Overview  

This project integrates **traffic prediction** and **pothole detection** using a Flask-based backend and a Streamlit-based frontend.  

### **🔹 Features**  
✅ **Traffic Prediction** – Uses an LSTM model to forecast traffic congestion.  
✅ **Pothole Detection** – Identifies potholes using a YOLO-based deep learning model.  
✅ **Google Maps API Integration** – Displays routes and pothole locations on an interactive map.  
✅ **Dynamic Rerouting** – Suggests alternative routes in case of heavy traffic.  

## 📜 Table of Contents  

- [🚀 Setup Instructions](#-setup-instructions)  
- [🖥 Running the Backend (Flask API)](#-running-the-backend-flask-api)  
- [💻 Running the Frontend (Streamlit App)](#-running-the-frontend-streamlit-app)  
- [🕵️‍♂️ Testing Pothole Detection](#-testing-pothole-detection)  
- [🚗 Testing Traffic Prediction](#-testing-traffic-prediction)  
- [📂 Folder Structure](#-folder-structure)  
- [⚠️ Troubleshooting](#-troubleshooting)  
- [🚀 Future Enhancements](#-future-enhancements)  

## 🚀 Setup Instructions  

### **1️⃣ Install Prerequisites**  

Ensure you have the following installed:  
✔ **Python 3.8+**  
✔ **Conda** (for virtual environment)  
✔ **Google Maps API key**  

### **2️⃣ Create & Activate a Conda Environment**  
```bash
conda create --name traffic_pothole python=3.8
conda activate traffic_pothole
```
### **3️⃣ Install Required Dependencies**  
```bash
pip install -r requirements.txt
```

## 🖥 Running the Backend (Flask API)  

```bash
cd Code_Files/backend 
python app.py
```
Backend will be running at:  
```
http://127.0.0.1:5000/
```

## 💻 Running the Frontend (Streamlit App)  

```bash
cd Code_Files/frontend
streamlit run main.py
```
Open the displayed **localhost URL** in your browser.  

## 🕵️‍♂️ Testing Pothole Detection  

1. Go to **Pothole Detection** in the Streamlit app.  
2. Upload an image of a road with potholes.  
3. The system will return an **annotated image** with detected potholes.  

## 🚗 Testing Traffic Prediction  

1. Select a **junction** and **destination** in the Streamlit app.  
2. Choose a **date and time**.  
3. Click **"Predict Traffic"** to get congestion levels.  
4. The app will display:  
   - **Estimated traffic percentage**  
   - **Suggested alternative routes if traffic is high**  

## 📂 Folder Structure  

```
Code_Files/
│   requirements.txt   # Required Python packages
│
├───backend/          # Flask API and models
│   │   app.py        # Flask backend
│   │   detected_potholes.jpg  # Sample pothole output
│   │
│   └───models/
│           best.pt   # YOLO model for pothole detection
│           lstm_traffic_model.h5  # LSTM model for traffic prediction
│           scaler.pkl  # Scaler for traffic model normalization
│
├───frontend/        # Streamlit UI
│   │   bg_2.jpg  # Background image
│   │   config.py  # Configuration settings
│   │   main.py  # Streamlit frontend script
│
├───model_training/  # Model training scripts
│   ├───Pothole_Detection/
│   │       best.pt  # Trained YOLO model
│   │       Pothole.ipynb  # Jupyter Notebook for training YOLO
│   │
│   └───traffic_pred/
│           lstm_traffic_model.h5  # Trained LSTM model
│           model_train.ipynb  # Jupyter Notebook for training LSTM
│           scaler.pkl  # Scaler for traffic model
│           updated_traffic.csv  # Processed traffic dataset
```

## ⚠️ Troubleshooting  

### **Backend Issues**  
- If the Flask API **fails to start**, install Flask manually:  
  ```bash
  pip install Flask
  ```
- Ensure `best.pt` and `lstm_traffic_model.h5` exist in `backend/models/`.

### **Frontend Issues**  
- If the Streamlit app **fails to start**, install missing packages:  
  ```bash
  pip install streamlit folium requests
  ```
- Check your **Google Maps API Key** in `config.py` if maps don't load.

## 🚀 Future Enhancements  

✅ **Real-time traffic updates using live APIs**  
✅ **Mobile app integration**  
✅ **Improved pothole detection with semantic segmentation**  

📧 **Contact:** [alexkhundongbam260@gmail.com](mailto:alexkhundongbam260@gmail.com)  