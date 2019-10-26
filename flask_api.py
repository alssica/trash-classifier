from flask import Flask, render_template, request
from skimage.io import imread
import cv2
import numpy as np
from keras.models import load_model


app = Flask(__name__)

categories = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']
cat_dict = dict(zip(categories, range(len(categories))))
cat_code_dict = dict(zip(range(len(categories)), categories))
img_w = 384//8
img_h = 512//8

def make_pred(model, img_file, img_w, img_h):

    npimg = np.fromfile(request.files['image'], np.uint8)
    # convert numpy array to image
    pic = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # pic = imread(img_file)

    pic = cv2.resize(pic, (img_w, img_h))
    
    # ensure the same orientation
    dim1 = len(pic)
    dim2 = len(pic[0])
    if dim1 > dim2:
        pic = np.rot90(pic)
        
    pic = np.expand_dims(pic, axis=0)
    #   y_class = model.predict_classes(pic)
    y_pred = model.predict(pic) 
    y_class_index = y_pred.argmax(axis=-1)[0]
    return cat_code_dict[y_class_index]

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # get uploaded image
        file = request.files['image']
        if not file: 
            return render_template('index.html', label="No file")
        

        # make prediction
        y_pred = make_pred(model, file, img_w, img_h)
        
        return render_template('index.html', user_image = file, label=y_pred)



if __name__ == "__main__":
    model = load_model('model/vgg19_5.h5')
    app.run(threaded=False)