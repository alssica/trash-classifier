import os
import cv2
import numpy as np
import base64

from keras.models import load_model
from keras.applications.imagenet_utils import preprocess_input
import keras

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# to be replaced by variables imported directly from the CNN script, once it's converted from nb to python file
categories = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']
cat_dict = dict(zip(categories, range(len(categories))))
cat_code_dict = dict(zip(range(len(categories)), categories))
img_w = 384//8
img_h = 512//8

# paths
# MODEL_PATH = 'model/vgg_8.h5'
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model/vgg_8.h5')
UPLOAD_PATH = 'uploads'

app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = "uploads"

def make_pred(model, img_file):

    # pic = cv2.imread(img_path, cv2.IMREAD_COLOR)
    # pic = cv2.resize(pic, (img_w, img_h))

    npimg = np.fromfile(img_file, np.uint8)
    pic = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    pic = cv2.resize(pic, (img_w, img_h))
    
    # ensure the same orientation
    dim1 = len(pic)
    dim2 = len(pic[0])
    if dim1 > dim2:
        pic = np.rot90(pic)
        
    pic_arr = np.expand_dims(pic, axis=0)
    x = preprocess_input(pic_arr, mode='caffe')  # necessary to turn single image into model required format

    y_pred = model.predict(x) 
    y_class_index = y_pred.argmax(axis=-1)[0]
    y_cat = cat_code_dict[y_class_index]
    y_prob = "{0:.1%}".format(y_pred[0][y_class_index])
    print(y_cat, y_prob)
    return "{},{}".format(y_cat, y_prob)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # get uploaded image
        file = request.files['image']
        
        # save to ./uploads
        # file_name = secure_filename(file.filename)
        # file_path = os.path.join(UPLOAD_PATH, file_name)
        # file.save(file_path)
        
        # make prediction
        result = make_pred(model, file)
        return result
        # return render_template('index.html', label=y_pred)

if __name__ == "__main__":
    model = load_model(MODEL_PATH)
    print("INFO: model is loaded.")
    
    app.run(threaded=False)
    # server = WSGIServer(('0.0.0.0', 5000), app)
    # server.serve_forever()