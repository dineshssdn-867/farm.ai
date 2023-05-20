import pickle
import sklearn

model = pickle.load(open('crop_recommendation_model.sav', 'rb'))

def recommend_crop(data):
    result = model.predict(data)
    return result[0]
