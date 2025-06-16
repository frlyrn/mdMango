from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import os
import io
from PIL import Image

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

MODEL_PATH = 'app/mango_classifier_model.h5'
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")

model = tf.keras.models.load_model(MODEL_PATH)

MODEL_INPUT_SHAPE = model.input_shape[1:]  
print(f"Model input shape: {MODEL_INPUT_SHAPE}")

CLASS_LABELS = ['Mature: ready to eat', 'Immature: wait for a few days']

@app.route('/')
def home():
    return "Fruit Maturity Detection API is running!"

@app.route('/predict', methods=['POST'])
def detect():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files['file']

        image = Image.open(io.BytesIO(file.read()))
        image = image.resize(MODEL_INPUT_SHAPE[:2])  
        image = np.array(image)  

        if image.shape[-1] != 3:
            return jsonify({"error": "Image must have 3 channels (RGB)."}), 400

        image = image.astype("float32")  
        image = np.expand_dims(image, axis=0)  
        image = image / 255.0  

        predictions = model.predict(image)
        print("Raw model output:", predictions)  # Debugging output

        if predictions.shape[-1] == 1:  # Model Sigmoid (0-1)
            maturity_score = float(predictions[0][0])
        else:  # Model Softmax (2 output)
            maturity_score = float(predictions[0][0])  # Gunakan indeks yang benar!

        # Menentukan status dan perkiraan hari panen
        if maturity_score > 0.5:
            result = "Mentah"
            suggestion = "Mangga ini belum matang, tunggu beberapa hari."
        else:
            result = "Matang"
            suggestion = "Mangga sudah matang, siap untuk dimakan."
            estimated_harvest_days = 0  # Sudah matang, siap panen

        return jsonify({
            "maturity_score": "{:.15e}".format(maturity_score),
            "result": result,
            "suggestion": suggestion,
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
