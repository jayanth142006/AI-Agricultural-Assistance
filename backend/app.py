from flask import Flask, render_template
from routes.crop_recommendation import crop_recommendation_bp
from routes.crop_yield_prediction import crop_yield_prediction_bp
from routes.fertilizer_recommendation import fertilizer_recommendation_bp  # Import the fertilizer recommendation blueprint
from routes.crop_pointer import crop_pointer_bp
from routes.crop_image_classification import crop_image_classification_bp  # Import the image classification blueprint

# Initialize the Flask app
app = Flask(__name__, template_folder="../frontend/templates")  # Ensure the correct path

# Register blueprints for APIs
app.register_blueprint(crop_recommendation_bp, url_prefix="/api/crop_recommendation")
app.register_blueprint(crop_yield_prediction_bp, url_prefix="/api/crop_yield_prediction")
app.register_blueprint(fertilizer_recommendation_bp, url_prefix="/api/fertilizer_recommendation")
app.register_blueprint(crop_pointer_bp, url_prefix="/api/crop_pointer")
app.register_blueprint(crop_image_classification_bp, url_prefix="/api/crop_image_classification")  # Register the new blueprint

# Home route (index page)
@app.route("/")
def home():
    return render_template("index.html")  # Ensure index.html exists in frontend/templates

# Route for Crop Recommendation Page
@app.route("/crop-recommendation")
def crop_recommendation_page():
    return render_template("crop_recommendation.html")  # Ensure the file exists in frontend/templates

# Route for Crop Yield Prediction Page
@app.route("/crop-yield-prediction")
def crop_yield_prediction_page():
    return render_template("crop_yield_prediction.html")  # Ensure this file exists in frontend/templates

# Route for Fertilizer Recommendation Page
@app.route("/fertilizer-recommendation")
def fertilizer_recommendation_page():
    return render_template("fertilizer_recommendation.html")  # Ensure this file exists in frontend/templates

@app.route("/crop-pointer")
def crop_pointer_page():
    return render_template("crop_pointer.html")  # Ensure crop_pointer.html exists in frontend/templates

# Route for Crop Image Classification Page
@app.route("/crop-image-classification")
def crop_image_classification_page():
    return render_template("crop_image_classification.html")  # Ensure crop_image_classification.html exists in frontend/templates

if __name__ == "__main__":
    app.run(debug=True)




