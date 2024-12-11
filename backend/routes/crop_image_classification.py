from flask import Blueprint, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import load_img, img_to_array
import numpy as np
import os

# Blueprint for Crop Image Classification
crop_image_classification_bp = Blueprint("crop_image_classification", __name__)

# Load the pre-trained model (VGG16)
model = load_model(os.path.join(os.getcwd(), "models", "vgg16(2).h5"))

# Set the target size for the model's input
TARGET_SIZE = (224, 224)

# Class names (you should match these to the classes used during training)
class_names = ['Potato__Early_blight','Potato__Late_blight','Potato__Healthy']

# Route for image classification
@crop_image_classification_bp.route("/predict", methods=["POST"])
def predict_crop_image():
    try:
        # Ensure uploads directory exists
        if not os.path.exists("uploads"):
            os.makedirs("uploads")

        # Check if an image file is part of the request
        if "file" not in request.files:
            return jsonify({"error": "No file part"})

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No selected file"})

        # Save the file temporarily
        img_path = os.path.join("uploads", file.filename)
        file.save(img_path)

        try:
            # Load and preprocess the image
            img = load_img(img_path, target_size=TARGET_SIZE)
            img_array = img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
            img_array /= 255.0  # Rescale image to [0, 1]

            # Predict the class
            predictions = model.predict(img_array)
            predicted_class_index = np.argmax(predictions, axis=1)
            predicted_class = class_names[predicted_class_index[0]]
            predicted_prob = predictions[0][predicted_class_index[0]]

            return jsonify({
                "predicted_class": predicted_class,
                "predicted_probability": float(predicted_prob)
            })
        finally:
            # Clean up the temporary file
            if os.path.exists(img_path):
                os.remove(img_path)
    except Exception as e:
        return jsonify({"error": str(e)})
