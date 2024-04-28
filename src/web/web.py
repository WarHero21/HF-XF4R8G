from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os

from ultralytics import YOLO
model = YOLO("yolov8s.pt") # load the model

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
DETECT_FOLDER = 'detects'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DETECT_FOLDER'] = DETECT_FOLDER
app.config['FILE_UPLOADED'] = len(os.listdir(app.config['UPLOAD_FOLDER']))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    images = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('./index.html', images=images)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        app.config['FILE_UPLOADED'] += 1
        filename = file.filename
        description = request.form['description']
        
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],f"{app.config['FILE_UPLOADED']}_{filename}"))
        
        detect(os.path.join(app.config['UPLOAD_FOLDER'],f"{app.config['FILE_UPLOADED']}_{filename}"))
        # You can save the description and filename to a database here if you want
        return redirect(url_for('index'))

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/detects/<path:filename>')
def detected_file(filename):
    return send_from_directory(app.config['DETECT_FOLDER'], filename)

@app.route('/detect/<path:filename>')
def detect(filename):
    model.predict(filename, classes=[2], save=True, project=app.config['DETECT_FOLDER'], show_labels=False, show_conf=False)

if __name__ == '__main__':
    app.run(debug=True)