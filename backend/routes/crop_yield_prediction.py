from flask import Blueprint, request, jsonify
import pandas as pd
import joblib

crop_yield_prediction_bp = Blueprint('crop_yield_prediction', __name__)

# Load the saved crop yield prediction model
model_pipeline = joblib.load("models/crop_yield_prediction1.pkl")

@crop_yield_prediction_bp.route("/predict", methods=["POST"])
def predict_yield():
    try:
        # Get input data from the request
        data = request.get_json()
        crop = data['crop']
        state = data['state']
        annual_rainfall = data['annual_rainfall']
        fertilizer = data['fertilizer']
        pesticide = data['pesticide']
        
        # Prepare input data for prediction
        input_data = pd.DataFrame([[crop, state, annual_rainfall, fertilizer, pesticide]],
                                  columns=['Crop', 'State', 'Annual_Rainfall', 'Fertilizer', 'Pesticide'])
        
        # Predict the crop yield
        predicted_yield = model_pipeline.predict(input_data)
        
        return jsonify({"predicted_yield": predicted_yield[0]})
    except Exception as e:
        return jsonify({"error": str(e)})
