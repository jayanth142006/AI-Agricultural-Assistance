from flask import Blueprint, request, jsonify
import joblib
import pandas as pd
import requests

# Define a Flask Blueprint
crop_recommendation_bp = Blueprint("crop_recommendation", __name__)

# Load the pre-trained model
model_path = "models/crop_recommendation_model.pkl"
model = joblib.load(model_path)

# Weatherstack API to get temperature and humidity based on state/city
def get_weather_data(city_name):
    api_key = '0925556b7e84c9a8fc023b0927bd9f32'  # Replace with your actual API key
    base_url = "http://api.weatherstack.com/current?"
    
    complete_url = base_url + "access_key=" + api_key + "&query=" + city_name
    response = requests.get(complete_url)
    data = response.json()

    if data.get("current"):
        temperature = data["current"]["temperature"]
        humidity = data["current"]["humidity"]
        return temperature, humidity
    else:
        return None, None

@crop_recommendation_bp.route("/", methods=["POST"])
def recommend_crop():
    try:
        # Extract data from the POST request
        data = request.json
        N = data.get("N")
        P = data.get("P")
        K = data.get("K")
        ph = data.get("ph")  # Ensure pH is being passed
        rainfall = data.get("rainfall")  # Ensure rainfall is being passed
        state = data.get("state")
        city = data.get("city")

        # Validate that all fields are provided
        if not all([N, P, K, ph, rainfall, state, city]):
            return jsonify({"error": "Missing input data"}), 400

        # Fetch weather data (temperature and humidity)
        temperature, humidity = get_weather_data(f"{city},{state}")

        if temperature is None or humidity is None:
            return jsonify({"error": "Failed to fetch weather data"}), 500

        # Create a DataFrame for the input
        input_data = pd.DataFrame([[N, P, K, temperature, humidity, ph, rainfall]], 
                                  columns=["N", "P", "K", "temperature", "humidity", "ph", "rainfall"])

        # Debugging step to ensure pH and rainfall are in the input data
        print(f"Input data for prediction: {input_data}")

        # Predict the crop
        prediction = model.predict(input_data)
        crop = prediction[0]

        # Return the result as JSON
        return jsonify({
            "recommended_crop": crop,
            "temperature": temperature,
            "humidity": humidity
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


