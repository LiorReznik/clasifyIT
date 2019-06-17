from flask import Blueprint, render_template, jsonify, request,make_response,send_file
from keras.models import load_model
from PIL import Image
from .utlis import prepare_image
import numpy as np
import io 
import os
import base64
from flask_login import login_user, logout_user, current_user
from ..email import sender
from email.mime.text import MIMEText
from ..encrypt import des_ofb,hash



home = Blueprint('home', __name__)

model = load_model(os.path.join(os.getcwd(), "clasifyIT/FINAL.h5"))

model._make_predict_function()


@home.route('/')
def index():
    
    return render_template('index.html')


@home.route('/search-doctor')
def search():
    return render_template('search.html')

    
@home.route('/contact')
def contact():
    return render_template('contact.html')

@home.route("/download-pdf",methods=["POST"])
def createPdf():
    from fpdf import FPDF
    message = request.get_json(force=True)
    print(message)
    pdf = FPDF()
    # compression is not yet supported in py3k version
    pdf.compress = True
    pdf.add_page()
    # Unicode is not yet supported in the py3k version; use windows-1252 standard font
    pdf.set_font('Arial', '', 14)  
    pdf.ln(10)
    pdf.write(5, message["prediction"])
    print(pdf.output('py3k.pdf', 'F'))
    pdf.close()
    from PyPDF2 import PdfFileReader, PdfFileWriter
    with open("py3k.pdf", "rb") as in_file:
        input_pdf = PdfFileReader(in_file)
        output_pdf = PdfFileWriter()
        output_pdf.appendPagesFromReader(input_pdf)
        email=des_ofb.ofb_decrypt(current_user.email,current_user.password_hash[:8],current_user.password_hash[24:32])  
        password=des_ofb.ofb_encrypt(current_user.username,current_user.password_hash[:8],current_user.password_hash[24:32])
        output_pdf.encrypt(password)
        out_file=open('encrypted_output.pdf', 'wb')
        out_file.seek(0)
        output_pdf.write(out_file)
        out_file.close()
        sender.SendMail().preapare_attatched_mail(email,"The password","Open the file to see the password for pdf",password)
        return send_file("../encrypted_output.pdf",mimetype='application/pdf',as_attachment=True)

@home.route("/predict", methods=["POST"])
def predict():
    """
    prediction function that gets an image from the user (frontend upload)
    and classifies it with a pre-trained model
    :return:
    """
    if current_user.is_authenticated:
        message = request.get_json(force=True)
        encoded = message['image']
        decoded = base64.b64decode(encoded)
        image = Image.open(io.BytesIO(decoded))
        processed_image = prepare_image(image, target_size=(50,50))#resizeing the image


        prediction = np.argmax(model.predict(processed_image).tolist())#getting the prediction

        cancer_type = { #translation dict
            0 : "Melanocytic_nevi",
            1 : "Melanoma",
            2 : "Benign_keratosis",
            3 : "Basal_cell_carcinoma",
            4 : "Actinic_keratoses",
            5 : "Vascular_lesions",
            6 : "Dermatofibroma"
        }
        
        email=des_ofb.ofb_decrypt(current_user.email,current_user.password_hash[:8],current_user.password_hash[24:32])  
        
        sender.SendMail().preapare_attatched_mail(email,"The Result","Open the file to see the result",cancer_type[prediction])
        response = {
            'prediction': {
                'result' : cancer_type[prediction]
            }
        }

        # sending the result to the front
        response = {'prediction': {'result' : cancer_type[prediction]}}
        return jsonify(response)
    else:
        return redirect(url_for('user.login')) #if not logged in redirecting to login page
