from flask import Blueprint, request, jsonify, render_template
import pandas as pd
import joblib

# Define the blueprint
yr_yield_prediction_bp = Blueprint('yr_yield_prediction', __name__)

# Load Prophet models from the "models/prophet_models" folder
import os
from prophet import Prophet

models = {}
models_folder = "models/prophet_models"

for model_file in os.listdir(models_folder):
    if model_file.endswith(".pkl"):
        crop_name = model_file.replace(".pkl", "")
        models[crop_name] = joblib.load(os.path.join(models_folder, model_file))

@yr_yield_prediction_bp.route("/predict", methods=["POST"])
def predict_yield():
    try:
        # Get input data from the request
        data = request.get_json()
        crop_name = data.get('crop_name')
        year = data.get('year')

        if crop_name not in models:
            return jsonify({"error": f"Model for crop '{crop_name}' not found!"}), 400

        # Get the Prophet model for the crop
        model = models[crop_name]

        # Create a DataFrame for the prediction year
        future_data = pd.DataFrame({'ds': [pd.to_datetime(f"{year}-01-01")]})
        
        # Predict yield
        forecast = model.predict(future_data)
        predicted_yield = forecast['yhat'].iloc[0]

        return jsonify({
            "crop_name": crop_name,
            "year": year,
            "predicted_yield": round(predicted_yield, 2)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@yr_yield_prediction_bp.route("/", methods=["GET"])
def yr_yield_prediction_page():
    return render_template("yr_yield_prediction.html")

