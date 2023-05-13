import string
import os
import cv2
from tensorflow import keras
import random
import numpy as np
from roboflow import Roboflow

rf = Roboflow(api_key="bF5YYYVrAfwch116an6u")
project = rf.workspace().project("weeds-public")
model = project.version(1).model
disease_types = ['Pepper__bell___Bacterial_spot','Pepper__bell___healthy','Potato___Early_blight','Potato___Late_blight','Potato___healthy','Tomato_Bacterial_spot','Tomato_Early_blight','Tomato_Late_blight','Tomato_Leaf_Mold','Tomato_Septoria_leaf_spot','Tomato_Spider_mites_Two_spotted_spider_mite','Tomato__Target_Spot','Tomato__Tomato_YellowLeaf__Curl_Virus','Tomato__Tomato_mosaic_virus','Tomato_healthy']
model_image = keras.models.load_model('model.h5')

def getPredictionWeeds(name):
    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
    result = model.predict(name, confidence=40, overlap=30)
    os.chdir('/workspace/farm.ai/static/predicted_images')
    result.save("{}.jpg".format(res))
    os.chdir('/workspace/farm.ai')
    return "{}.jpg".format(res)


def getPredictionDisease(img):
    img = cv2.resize(img, (64, 64))
    img = np.reshape(img, (1, 64, 64, 3))
    prediction = model_image.predict(img)
    return disease_types[np.argmax(prediction)]

