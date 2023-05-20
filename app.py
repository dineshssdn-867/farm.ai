
import os
import cv2
import random
import string
import numpy as np
import urllib.request
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    url_for,
    render_template_string,
    send_file,
    jsonify,
)
from main_image import getPredictionWeeds, getPredictionDisease
from werkzeug.utils import secure_filename
from utils import html_js_file_weeds, html_js_file_disease, save_image_frame
from recommend_crop_predict import recommend_crop
from bot import get_response

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/weeds_detection_form", methods=["GET", "POST"])
def weeds_detection_form():
    return render_template("predict_weeds.html", predicted=False)

@app.route("/disease_detection_form", methods=["GET", "POST"])
def disease_detection_form():
    return render_template("predict_disease.html", predicted=False)

@app.route("/weeds_detect_camera", methods=["GET", "POST"])
def weeds_detect_camera():
    return render_template_string(html_js_file_weeds)

@app.route("/disease_detect_camera", methods=["GET", "POST"])
def disease_detect_camera():
    return render_template_string(html_js_file_disease)

@app.route("/crop_recommender_form", methods=["GET", "POST"])
def crop_recommender_form():
    return render_template('predict_crop_recommend.html', predicted=False)

@app.route("/weeds_detect_image", methods=["POST"])
def weeds_detect_image():
    if request.method == "POST":
        file = request.files.get("image")
        if file.filename != '':
            nparr = np.fromstring(request.files["image"].read(), np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            random_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
            filename = save_image_frame(img, "{}.jpg".format(random_name))
            res = getPredictionWeeds("{}.jpg".format(random_name))
            return render_template(
                "predict_weeds.html",
                predicted=True,
                filename=res
            )
        else:
            return render_template("predict_weeds.html", predicted=False)

@app.route("/disease_detect_image", methods=["POST"])
def disease_detect_image():
    if request.method == "POST":
        file = request.files.get("image")
        if file.filename != '':
            nparr = np.fromstring(request.files["image"].read(), np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            res = getPredictionDisease(img)
            return render_template(
                "predict_disease.html",
                predicted=True,
                class_predicted=res
            )
        else:
            return render_template("predict_disease.html", predicted=False)


@app.route('/recommend_crop_value',methods=['POST'])
def recommend_crop_value():
    N = request.form.get('N')
    P = request.form.get('P')
    K = request.form.get('K')
    temperature = request.form.get('temperature')
    humidity = request.form.get('humidity')
    rainfall = request.form.get('rainfall')
    ph = request.form.get('ph')
    crop_name = recommend_crop([[P, N, K, temperature, humidity, ph, rainfall]])
    return render_template("predict_crop_recommend.html", class_predicted=crop_name.capitalize(), predicted=True)


@app.route("/bot")
def bot():
    return render_template("chatbot.html")


@app.route("/chatbot_response", methods=["GET", "POST"])
def chatbot_response():
    msg = request.form["msg"]
    response = get_response(msg)
    return str(response)


if __name__ == "__main__":
  app.run(debug=True)
