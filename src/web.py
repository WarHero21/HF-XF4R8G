import os, io
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, make_response
from datetime import datetime
from PIL import Image

from db import Db
from alert import alert_admins
from data import Data

from ultralytics import YOLO
model = YOLO("src/yolov8s.pt") # load the model

app = Flask(__name__)
DB_NAME = "test"
UPLOAD_FOLDER = 'pictures'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'avif'}
ADMIN_LIST = ['admin','Obi-Wan Kenobi']
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

db = Db(DB_NAME)

if not os.path.exists(f"{UPLOAD_FOLDER}"):
    os.mkdir(f"{UPLOAD_FOLDER}")

### UTILS ###

def init_files(username):
    datas = db.download(username)

    for data in datas:
        save_image(data)

def save_image(data):
    if not os.path.exists(f"{UPLOAD_FOLDER}/{data.username}"):
        os.mkdir(f"{UPLOAD_FOLDER}/{data.username}")
    img = Image.open(io.BytesIO(data.image))
    filename = os.path.join(f"{UPLOAD_FOLDER}", data.username, data.filename)
    img.save(filename)

def read_cookies(cookies):
    datas = []
    for (key, value) in cookies.items():
        if key == 'username' or key == 'session' or key == 'admin_name':
            continue
        
        datas.append(Data.from_cookie(value))

    return datas

### PAGES ###

@app.route('/user')
def user():
    datas = read_cookies(request.cookies)
    username=request.cookies.get("username")
    return render_template('./user.html', datas=datas, username=username)

@app.route('/admin')
def admin():
    username=request.cookies.get("username")
    usernames= db.get_users()
    admin_name=request.cookies.get("admin_name")
    datas = db.download_all(username)
    return render_template('./admin.html', datas=datas, username=username, usernames=usernames, admin_name=admin_name)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        db.save_user(username)

        datas = db.download_all(username)
        
        template = '/admin' if username in ADMIN_LIST else '/user'
        
        response = make_response(redirect(template))
        response.set_cookie('username', username)
        if username in ADMIN_LIST:
            response.set_cookie("admin_name", username)
        
        for data in datas:
            response.set_cookie(f"{data.filename}", f"{data.to_cookie()}")

        return response
    return render_template('./login.html')

### UPLOAD ###

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    filename = file.filename
    if filename == '':
        return redirect(request.url)
    
    if '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        username = request.cookies.get("username")
        
        current_date = datetime.now()
        new_filename = f'{current_date.strftime("%Y%m%d%H%M%S")}_{filename}'
        filename_to_save = os.path.join(app.config['UPLOAD_FOLDER'],username, new_filename)
        if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'],username)):
            os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'],username))
        file.save(filename_to_save)
        
        results = model.predict(source=filename_to_save, classes=[2], save=True, project=os.path.join(app.config['UPLOAD_FOLDER'],username), show_labels=False, show_conf=False)
        number = len(results[0].boxes.data)
        
        date = current_date.strftime("%Y-%m-%d %H:%M:%S")
        description = request.form['description']

        image = Image.open(filename_to_save)
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='JPEG')

        data = Data(image_bytes.getvalue(),description,new_filename,number,username,date)

        ## DB

        data.id = db.upload(username, data)

        ## Cache
        
        template = '/admin' if username in ADMIN_LIST else '/user'
        datas = read_cookies(request.cookies)
        datas.append(data)

        response = make_response(redirect(template))
        response.set_cookie(f'{data.filename}', f'{data.to_cookie()}')

        ## Alert

        alert_admins(data)

        return response

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    username = request.cookies.get("username")
    
    if not os.path.exists(f"{UPLOAD_FOLDER}/{username}/{filename}"):
        data = db.download(username, filename)
        save_image(data)

    response = make_response(send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], username), filename))
    response.headers['Cache-Control'] = 'max-age=604800' # 1 week
    return response

@app.route('/choose_user', methods=['POST'])
def choose_user():
    response = make_response(redirect('/admin'))
    response.set_cookie('username', request.form.get('username'))
    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)