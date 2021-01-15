import cv2 as cv
import os
import base64
from flask import Flask, request,render_template
from werkzeug.utils import secure_filename   # 获取上传文件的文件名


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','doc'])   # 允许上传的文件类型
UPLOAD_FOLDER = r'upload'   # 上传路径
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):   # 验证上传的文件名是否符合要求，文件名必须带点并且符合允许上传的文件类型要求，两者都满足则返回 true
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':   # 如果是 POST 请求方式
        file = request.files['file']   # 获取上传的文件
        if file and allowed_file(file.filename):   # 如果文件存在并且符合要求则为 true\
            filename = secure_filename(file.filename)   # 获取上传文件的文件名
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))   # 保存文件
            img = cv.imread('upload/{}'.format(filename))
            face_engine = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
            faces = face_engine.detectMultiScale(img,scaleFactor=1.3,minNeighbors=5)
            for (x,y,w,h) in faces:
                img = cv.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            cv.imwrite('upload/ing.png',img)
            img_stream = ''
            with open('upload/ing.png', 'rb') as img_f:
                img_stream = img_f.read()
                img_stream = base64.b64encode(img_stream).decode()
            if len(faces) == 1:
                return render_template('picture.html',
                           img_stream=img_stream)
            else:
                return '<h1 style="text-align: center">改图无人脸！<h1>'
    return render_template('index.html')

if __name__ == "__main__":
    app.run()