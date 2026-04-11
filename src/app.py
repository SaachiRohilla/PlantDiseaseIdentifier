import io
from flask import Flask, render_template, request, jsonify
from PIL import Image
import base64
from model import run_model

app = Flask(__name__)

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
    #need to call model here 

    if "image" not in request.files:
        return TypeError
    
    file = request.files["image"]

    if file.filename not in allowed_ext(file.filename):
        return TypeError
    
    image = Image.open(file.stream)

    encoded_image = encoding(image)

    output = run_model(encoded_image) 
    #need to gte the model function and need to see what dtype is returned

    return render_template("index.html", image, output)


if __name__ == '__main__':
    app.run()