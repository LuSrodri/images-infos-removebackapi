import os
import uuid
from flask import Flask, flash, jsonify, make_response, request, redirect, url_for
from werkzeug.utils import secure_filename
from rembg import remove
from PIL import Image
from google.cloud import storage
from dotenv import load_dotenv

load_dotenv()

UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

storage_client = storage.Client()
bucket_name = "imagesinfos"
bucket = storage_client.get_bucket(bucket_name)

@app.route("/removeback", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(str(uuid.uuid4()) + '.png')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            input = Image.open(filename)
            output = remove(input)
            output.save(filename)

            blob = bucket.blob(filename)
            blob.upload_from_filename(filename)

            os.unlink(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            return jsonify(publicUrl=("https://storage.googleapis.com/imagesinfos/" + filename))