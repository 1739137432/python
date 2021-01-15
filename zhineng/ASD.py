import os
import cv2
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__, template_folder='./html')

@app.route('/up_file', methods=['POST'])
def up_file(): 
    file = request.files['file']
    img = cv2.imread(file.filename,1)
    face_engine = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faces = face_engine.detectMultiScale(img,scaleFactor=1.3,minNeighbors=5)
    for (x,y,w,h) in faces:
        img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    cv.imwrite('upload/ing.png',img)

    img_stream = ''
    with open('upload/ing.png', 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream).decode()
    return render_template('index.html',img_stream=img_stream)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()