from flask import Flask, render_template, request, Markup
import pandas as pd
from utils.fertilizer import fertilizer_dict
import os
import numpy as np
from keras.preprocessing import image
from keras.models import load_model
import pickle

classifier = load_model('Trained_model.h5')
classifier._make_predict_function()

classifier2 = load_model('Leaf_disease_Model.h5')
classifier2._make_predict_function()

classifier3 = load_model('tomato_Model.h5')
classifier3._make_predict_function()

crop_recommendation_model_path = 'Crop_Recommendation.pkl'
crop_recommendation_model = pickle.load(open(crop_recommendation_model_path, 'rb'))

app = Flask(__name__)

@ app.route('/fertilizer-predict', methods=['POST'])
def fertilizer_recommend():

    crop_name = str(request.form['cropname'])
    N_filled = int(request.form['nitrogen'])
    P_filled = int(request.form['phosphorous'])
    K_filled = int(request.form['potassium'])

    df = pd.read_csv('Data/Crop_NPK.csv')

    N_desired = df[df['Crop'] == crop_name]['N'].iloc[0]
    P_desired = df[df['Crop'] == crop_name]['P'].iloc[0]
    K_desired = df[df['Crop'] == crop_name]['K'].iloc[0]

    n = N_desired- N_filled
    p = P_desired - P_filled
    k = K_desired - K_filled

    if n < 0:
        key1 = "NHigh"
    elif n > 0:
        key1 = "Nlow"
    else:
        key1 = "NNo"

    if p < 0:
        key2 = "PHigh"
    elif p > 0:
        key2 = "Plow"
    else:
        key2 = "PNo"

    if k < 0:
        key3 = "KHigh"
    elif k > 0:
        key3 = "Klow"
    else:
        key3 = "KNo"

    abs_n = abs(n)
    abs_p = abs(p)
    abs_k = abs(k)

    response1 = Markup(str(fertilizer_dict[key1]))
    response2 = Markup(str(fertilizer_dict[key2]))
    response3 = Markup(str(fertilizer_dict[key3]))
    return render_template('Fertilizer-Result.html', recommendation1=response1,
                           recommendation2=response2, recommendation3=response3,
                           diff_n = abs_n, diff_p = abs_p, diff_k = abs_k)


def pred_pest(pest):
    try:
        test_image = image.load_img(pest, target_size=(64, 64))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        result = classifier.predict_classes(test_image)
        return result
    except:
        return 'x'

def pred_rice(rice):
    try:
        test_image = image.load_img(rice, target_size=(64, 64))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        result = classifier2.predict_classes(test_image)
        return result
    except:
        return 'x'

def pred_tomato(tomato):
    try:
        test_image = image.load_img(tomato, target_size=(256, 256))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        result = classifier3.predict_classes(test_image)
        return result
    except:
        return 'x'



@app.route("/")
@app.route("/index.html")
def index():
    return render_template("index.html")

@app.route("/CropRecommendation.html")
def crop():
    return render_template("CropRecommendation.html")

@app.route("/FertilizerRecommendation.html")
def fertilizer():
    return render_template("FertilizerRecommendation.html")

@app.route("/PesticideRecommendation.html")
def pesticide():
    return render_template("PesticideRecommendation.html")

@app.route("/DiseaseDetection.html")
def Disease():
    return render_template("DiseaseDetection.html")

@app.route("/TomatoDetection.html")
def Tomato():
    return render_template("TomatoDetection.html")


@app.route("/predict", methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        file = request.files['image']  # fetch input
        filename = file.filename

        file_path = os.path.join('static/user uploaded', filename)
        file.save(file_path)

        pred = pred_pest(pest=file_path)
        if pred == 'x':
            return render_template('unaptfile.html')
        if pred[0] == 0:
            pest_identified = 'aphids'
        elif pred[0] == 1:
            pest_identified = 'armyworm'
        elif pred[0] == 2:
            pest_identified = 'beetle'
        elif pred[0] == 3:
            pest_identified = 'bollworm'
        elif pred[0] == 4:
            pest_identified = 'earthworm'
        elif pred[0] == 5:
            pest_identified = 'grasshopper'
        elif pred[0] == 6:
            pest_identified = 'mites'
        elif pred[0] == 7:
            pest_identified = 'mosquito'
        elif pred[0] == 8:
            pest_identified = 'sawfly'
        elif pred[0] == 9:
            pest_identified = 'stem borer'

        return render_template(pest_identified + ".html",pred=pest_identified)

@app.route("/rice_predict", methods=['GET', 'POST'])
def rice_predict():

   
    if request.method == 'POST':
        file = request.files['image']  # fetch input
        filename = file.filename

        file_path = os.path.join('static/user uploaded', filename)
        file.save(file_path)

        disease = pred_rice(rice=file_path)
        if disease == 'x':
            return render_template('unaptfile.html')
        if disease[0] == 0:
            rice_identified = 'bacterial leaf blight'
        elif disease[0] == 1:
            rice_identified = 'brown spot'
        elif disease[0] == 2:
            rice_identified = 'leaf smut'

        return render_template(rice_identified + ".html",disease=rice_identified)


@app.route("/tomato_predict", methods=['GET', 'POST'])
def tomato_predict():
    if request.method == 'POST':
        file = request.files['image']  # fetch input
        filename = file.filename

        file_path = os.path.join('static/user uploaded', filename)
        file.save(file_path)

        vegetable = pred_tomato(tomato=file_path)
        if vegetable == 'x':
            return render_template('unaptfile.html')
        if vegetable[0] == 0:
            tomato_identified = 'Pepper__bell___Bacterial_spot'
        elif vegetable[0] == 1:
            tomato_identified = 'Pepper__bell___healthy'
        elif vegetable[0] == 2:
            tomato_identified = 'Potato___Early_blight'
        elif vegetable[0] == 3:
            tomato_identified = 'Potato___healthy'
        elif vegetable[0] == 4:
            tomato_identified = 'Potato___Late_blight'
        elif vegetable[0] == 5:
            tomato_identified = 'Tomato__Target_Spot'
        elif vegetable[0] == 6:
            tomato_identified = 'Tomato__Tomato_mosaic_virus'
        elif vegetable[0] == 7:
            tomato_identified = 'Tomato__Tomato_YellowLeaf__Curl_Virus'
        elif vegetable[0] == 8:
            tomato_identified = 'Tomato_Bacterial_spot'
        elif vegetable[0] == 9:
            tomato_identified = 'Tomato_Early_blight'
        elif vegetable[0] == 10:
            tomato_identified = 'Tomato_healthy'
        elif vegetable[0] == 11:
            tomato_identified = 'Tomato_Late_blight'
        elif vegetable[0] == 12:
            tomato_identified = 'Tomato_Leaf_Mold'
        elif vegetable[0] == 13:
            tomato_identified = 'Tomato_Septoria_leaf_spot'
        elif vegetable[0] == 14:
            tomato_identified = 'Tomato_Spider_mites_Two_spotted_spider_mite'
       
        return render_template(tomato_identified + ".html",vegetable=tomato_identified)




@ app.route('/crop_prediction', methods=['POST'])
def crop_prediction():
    if request.method == 'POST':
        N = int(request.form['nitrogen'])
        P = int(request.form['phosphorous'])
        K = int(request.form['potassium'])
        ph = float(request.form['ph'])
        rainfall = float(request.form['rainfall'])
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
        my_prediction = crop_recommendation_model.predict(data)
        final_prediction = my_prediction[0]
        return render_template('crop-result.html', prediction=final_prediction, pred='img/crop/'+final_prediction+'.jpg')

if __name__ == '__main__':
    app.run(debug=True)