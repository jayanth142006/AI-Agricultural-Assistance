from flask import Blueprint, request, jsonify
import pandas as pd
import joblib
import requests

# Create a blueprint for fertilizer recommendation
fertilizer_recommendation_bp = Blueprint('fertilizer_recommendation', __name__)

# Load the saved fertilizer recommendation model
model_pipeline = joblib.load("models/fertilizer_recommendation_model.pkl")  # Ensure the path is correct

# Weatherstack API to fetch temperature and humidity
def get_weather_data(city_name):
    api_key = '0925556b7e84c9a8fc023b0927bd9f32'  # Replace with your API key
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

@fertilizer_recommendation_bp.route("/predict", methods=["POST"])
def predict_fertilizer():
    try:
        # Get input data from the request
        data = request.get_json()
        state = data['state']
        city = data['city']
        moisture = data['moisture']
        soil_type = data['soil_type']
        crop_type = data['crop_type']
        nitrogen = data['nitrogen']
        potassium = data['potassium']
        phosphorous = data['phosphorous']

        # Fetch weather data (temperature and humidity)
        temperature, humidity = get_weather_data(f"{city},{state}")

        if temperature is None or humidity is None:
            return jsonify({"error": "Failed to fetch weather data"}), 500

        # Prepare input data for prediction
        input_data = pd.DataFrame([[temperature, humidity, moisture, soil_type, crop_type, nitrogen, potassium, phosphorous]],
                                  columns=['Temperature', 'Humidity', 'Moisture', 'Soil Type', 'Crop Type', 
                                           'Nitrogen', 'Potassium', 'Phosphorous'])
        
        # Predict the fertilizer
        predicted_fertilizer = model_pipeline.predict(input_data)
        
        # Return the result as JSON
        return jsonify({
            "predicted_fertilizer": predicted_fertilizer[0],
            "temperature": temperature,
            "humidity": humidity
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
