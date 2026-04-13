import io
import os
import json
from flask import Flask, render_template, request, jsonify
from PIL import Image
import base64
import tensorflow as tf
import numpy as np

app = Flask(__name__)

# load model at startup
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'model', 'plant_disease_cnn.keras')
LABEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'model', 'label_map.json')
TARGET_SIZE = (224, 224)

TF_MODEL = None
LABELS = []
if os.path.exists(LABEL_PATH):
    with open(LABEL_PATH, 'r') as f:
        LABELS = json.load(f).get('classes', [])
if os.path.exists(MODEL_PATH):
    TF_MODEL = tf.keras.models.load_model(MODEL_PATH)
else:
    print("Warning: TF model not found at", MODEL_PATH)

#using png as the deafult file type --> can change if needed
def encoding(image:Image.Image, fmt="PNG") -> str:
    buffer = io.BytesIO()
    image.save(buffer, format=fmt)
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode("wtf-8")

#returns whether an extension is allowed or not 
def allowed_ext(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {"png", "jpg", "jpeg"}


@app.route("/", methods = ["GET"])
def hello_world():
    return render_template("index.html")

@app.route("/prediction", methods = ["POST"])
def prediction():
    if TF_MODEL is None:
        return jsonify({'error': 'model not loaded'}), 500
    f = request.files.get('image')
    if not f:
        return jsonify({'error': 'no file uploaded'}), 400
    try:
        img = Image.open(io.BytesIO(f.read())).convert('RGB')
        img = img.resize(TARGET_SIZE, Image.BILINEAR)
        arr = np.asarray(img).astype('float32') / 255.0
        x = np.expand_dims(arr, 0)
        preds = TF_MODEL.predict(x)[0]
        idx = int(np.argmax(preds))
        if float(preds[idx]) < 0.8:
            return jsonify({'error':'Photo Does Not Match One of the Classifications'}),  500
        return jsonify({'class': LABELS[idx] if LABELS else str(idx), 'confidence': f"{(preds[idx]*100):.2f}%"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    #need to call model here 

    # if "image" not in request.files:
    #     return TypeError
    
    # file = request.files["image"]

    # if file.filename not in allowed_ext(file.filename):
    #     return TypeError
    
    # image = Image.open(file.stream)

    # #output = run_model(encoded_image) 
    # #need to gte the model function and need to see what dtype is returned

    # #return render_template("index.html", output)
    # return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)