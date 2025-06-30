import numpy as np
import tensorflow as tf
from flask import Flask, request
from flask_cors import CORS

from errors import AppError
from utils import preprocess_image, read_json, send_response

app = Flask(__name__)
CORS(app)

# Load model
model = tf.keras.models.load_model("traffic_classifier.keras")
gtsrb_labels = read_json("gtsrb-labels.json")

@app.route("/api/v1/image/classify", methods=["POST"])
def classify_traffic_sign():
    try:
        if "image" not in request.files:
            raise AppError(code=400, message="No image uploaded.")

        img_file = request.files["image"]
        if img_file.filename == "":
            raise AppError(code=400, message="No image name found.")

        if img_file and not img_file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            raise AppError(code=400, message="Accepted formats: .png, .jpg or .jpeg.")

        # Process image
        img_bytes = img_file.read()
        processed_img = preprocess_image(img_bytes)
        
        # Predict image class
        predictions = model.predict(processed_img)
        predicted_class, confidence = int(np.argmax(predictions[0])), float(np.max(predictions[0]))
        
        if predicted_class is None or confidence is None:
            raise AppError(code=500, message="Prediction failed")

        predicted_label = gtsrb_labels.get(str(predicted_class))
        confidence = round(confidence, 3)
        return send_response("success", {
            "imageName" : img_file.filename, 
            "predictedLabel" : predicted_label, 
            "confidence" : confidence
            }
        )
    
    except AppError as e:
        return send_response("error", {"message" : e.message}), e.code
    except Exception as e:
        return send_response("error", {"message" : "Something went wrong! please try again later."}), 500



if __name__ == "__main__":
    app.run(debug=True, port=8080)
