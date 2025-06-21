from PIL import Image
import tensorflow as tf
import numpy as np
import cv2
import os# load and preprocess the image
from fastapi import Request
import requests
from flask import Flask, jsonify, render_template, request,redirect,session,url_for
import mysql.connector
import os
import numpy as np
import pandas
import sklearn
import pickle
# from tensorflow.keras.models import load_model
from keras.models import load_model

# from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from werkzeug.utils import secure_filename

import tensorflow as tf



from tensorflow import keras
from skimage import io
from tensorflow.keras.preprocessing import image


# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename


#####  importing model
model=pickle.load(open('model.pkl','rb'))

model2 =tf.keras.models.load_model('D:\shashikala\FarmAI\model\PlantDNet.h5',compile=False)
print('Model2 loaded. Check http://127.0.0.1:5000/')
app=Flask(__name__)

app.secret_key=os.urandom(24)
conn=mysql.connector.connect( host='localhost',
    user='root',
    password='shashikala',
    database='FarmAI')
cursor=conn.cursor()

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def about():
    return render_template('register.html')

@app.route('/')
def home():
    return render_template('home.html')

#########   Features 
@app.route('/features')
def feature():
    if 'user_id' in session:
        return render_template('features.html')
    else:
        return redirect('/')
########### About Section
@app.route('/aboutFeature')
def aboutFeature():
    return render_template('aboutFeature.html')    

#######     Pricing Section
@app.route('/pricing')
def pricing():
    return render_template('pricing.html')



@app.route('/login_validation',methods=['POST'])
def login_validation():
    email=request.form.get('email')
    password=request.form.get('password')

    cursor.execute("SELECT * FROM `user` WHERE `email` = %s AND `password` = %s", (email, password))
    users = cursor.fetchall()
    if len(users)>0:
        session['user_id']=users[0][0]
        return redirect('/features')
    else:
        return redirect('/')
    return users


@app.route('/add_user', methods=['POST'])
def add_user():
    name=request.form.get('uname')
    email=request.form.get('uemail')
    password=request.form.get('upassword')
    cursor.execute("INSERT INTO `user` (`user_id`, `sname`, `email`, `password`) VALUES (NULL, %s, %s, %s)",
                   (name, email, password))
    conn.commit()

    cursor.execute("""SELECT * FROM `user` WHERE `email` LIKE '{}'""".format(email))
    myuser=cursor.fetchall()
    session['user_id']=myuser[0][0]
    return redirect('/')
    # return "The email is {} and the password is {} ".format(email,password)
##############               Features     #########################
@app.route('/cropPrediction')
def cropprediction():
    return render_template('/cropPrediction.html')


@app.route("/predict", methods=['POST'])
def predict():
    try:
        N = int(request.form['Nitrogen']) if request.form['Nitrogen'] else 0
        P = int(request.form['Phosphorous']) if request.form['Phosphorous'] else 0
        K = int(request.form['Potassium']) if request.form['Potassium'] else 0
        temp = float(request.form['Temperature']) if request.form['Temperature'] else 0.0
        humidity = float(request.form['Humidity']) if request.form['Humidity'] else 0.0
        ph = float(request.form['pH']) if request.form['pH'] else 0.0
        rainfall = float(request.form['Rainfall']) if request.form['Rainfall'] else 0.0
    except ValueError:
        result = "Please enter valid numeric values for all inputs."
        return render_template('cropPrediction.html', result=result)

    feature_list = [N, P, K, temp, humidity, ph, rainfall]
    single_pred = np.array(feature_list).reshape(1, -1)
    prediction = model.predict(single_pred)

    crop_dict = {
        1: 'Rice', 2: 'Maize', 3: 'Jute', 4: 'Cotton', 5: 'Coconut', 6: 'Papaya', 7: 'Orange',
        8: 'Apple', 9: 'Muskmelon', 10: 'Watermelon', 11: 'Grapes', 12: 'Mango', 13: 'Banana',
        14: 'Pomegranate', 15: 'Lentil', 16: 'Blackgram', 17: 'Mungbean', 18: 'Mothbeans',
        19: 'Pigeonpeas', 20: 'Kidneybeans', 21: 'Chickpea', 22: 'Coffee'
    }

    crop = crop_dict.get(prediction[0], "Unknown")
    result = f"{crop} is the best crop to be cultivated right there" if crop != "Unknown" else "Prediction failed."

    return render_template('cropPrediction.html', prediction=result)

@app.route('/agroCart')
def agroCart():
    return render_template('agroCart.html')
@app.route('/fertilizers')
def fertilizers():
    return render_template('fertilizers.html')
@app.route('/pesticides')
def pesticides():
    return render_template('pesticides.html')
@app.route('/farmTools')
def farmTools():
    return render_template('farmTools.html')
@app.route('/soilKit')
def soilKit():
    return render_template('soilKit.html')
########        Disease Detection ###########

def model_predict(img_path, model2):
    img = image.load_img(img_path, grayscale=False, target_size=(64, 64))
    show_img = image.load_img(img_path, grayscale=False, target_size=(64, 64))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = np.array(x, 'float32')
    x /= 255
    preds = model2.predict(x)
    return preds

@app.route('/predictD', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model2)
        print(preds[0])

        # x = x.reshape([64, 64]);
        disease_class = ['Pepper__bell___Bacterial_spot', 'Pepper__bell___healthy', 'Potato___Early_blight',
                         'Potato___Late_blight', 'Potato___healthy', 'Tomato_Bacterial_spot', 'Tomato_Early_blight',
                         'Tomato_Late_blight', 'Tomato_Leaf_Mold', 'Tomato_Septoria_leaf_spot',
                         'Tomato_Spider_mites_Two_spotted_spider_mite', 'Tomato__Target_Spot',
                         'Tomato__Tomato_YellowLeaf__Curl_Virus', 'Tomato__Tomato_mosaic_virus', 'Tomato_healthy']
        a = preds[0]
        ind=np.argmax(a)
        print('Prediction:', disease_class[ind])
        result=disease_class[ind]
        return result
    return None

@app.route('/diseasePrediction', methods=['GET'])
def diseasePrediction():
    return render_template('diseasePrediction.html')

@app.route('/chatbot')
def chatbot():
    
    return render_template('/chatbot.html', image_url=url_for('static', filename='kisan.png'),ai_Url=url_for('static', filename='mira.png'),load_Url=url_for('static', filename='loading.webp'))
API_KEY="YOUR_API_KEY"
from flask import Flask, request, jsonify, render_template
import requests

# app = Flask(__name__)

# Flask backend: /generate
@app.route('/generate', methods=['POST'])
def generate():
    
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        image = data.get('image')
        API_KEY = "YOUR_API_KEY"

        headers = {"Content-Type": "application/json"}
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"



        parts = [{"text": prompt}]
        if image:
            parts.append({
                "inline_data": {
                    "mime_type": image["mime_type"],
                    "data": image["data"]
                }
            })

        payload = {
            "contents": [{
                "parts": parts
            }]
        }

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        output = response.json()
        generated_text = output["candidates"][0]["content"]["parts"][0]["text"]

        return jsonify({"response": generated_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#################### Logout ###########################
@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')
if __name__=='__main__':
    app.run(debug=True)



