from flask import Blueprint, render_template, jsonify, request
from keras.models import load_model
from PIL import Image
from .utlis import prepare_image
import numpy as np
import io 
import os
import base64


home = Blueprint('home', __name__)

model = load_model(os.path.join(os.getcwd(), "clasifyIT/FINAL.h5"))

model._make_predict_function()

@home.route('/')
def index():
    return render_template('index.html')


@home.route("/predict", methods=["POST"])
def predict():
    message = request.get_json(force=True)
    encoded = message['image']
    decoded = base64.b64decode(encoded)
    image = Image.open(io.BytesIO(decoded))
    processed_image = prepare_image(image, target_size=(50,50))


    prediction = np.argmax(model.predict(processed_image).tolist())

    cancer_type = {
        0 : "Melanocytic_nevi",
        1 : "Melanoma",
        2 : "Benign_keratosis",
        3 : "Basal_cell_carcinoma",
        4 : "Actinic_keratoses",
        5 : "Vascular_lesions",
        6 : "Dermatofibroma"
    }
    
    print(cancer_type[prediction])

    response = {
        'prediction': {
            'result' : cancer_type[prediction]
        }
    }

    return jsonify(response)
