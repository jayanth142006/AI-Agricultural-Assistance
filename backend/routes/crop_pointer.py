from flask import Blueprint, request, jsonify
import pandas as pd
import joblib

# Blueprint for Crop Pointer
crop_pointer_bp = Blueprint("crop_pointer", __name__)

# Load the pre-trained model
model = joblib.load("models/pointer_crop_model.pkl")

@crop_pointer_bp.route("/predict", methods=["POST"])
def predict_crop():
    try:
        # Get input data from the request
        data = request.get_json()
        latitude = data["latitude"]
        longitude = data["longitude"]
        season = data["season"]
        year = data["year"]

        # Prepare input data
        input_data = pd.DataFrame([[latitude, longitude, season, year]],
                                  columns=["Latitude", "Longitude", "Season", "Year"])

        # Predict crop probabilities
        crop_probabilities = model.predict_proba(input_data)[0]

        # Get the crop names (you should have them in the same order as the model's classes)
        crops = model.classes_

        # Create a dictionary of crop names and their respective probabilities
        crop_prob_dict = dict(zip(crops, crop_probabilities))

        # Find the predicted crop with the highest probability
        predicted_crop = crops[crop_probabilities.argmax()]

        return jsonify({"predicted_crop": predicted_crop, "crop_probabilities": crop_prob_dict})

    except Exception as e:
        return jsonify({"error": str(e)})
