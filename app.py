import os
import uuid
from flask import Flask, flash, jsonify, make_response, request, redirect, url_for
from flask_cors import cross_origin
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

@app.route("/", methods=['GET', 'POST'])
@cross_origin()
def removebackapi():
    if request.method == "GET":
        return '<h1>Removeback API</h1>'

@app.route("/removeback", methods=['GET', 'POST'])
@cross_origin()
def upload_file():
    if request.method == 'POST':
        print(request.headers.get("X-RapidAPI-Proxy-Secret"))
        print(os.environ.get("X_RAPIDAPI_PROXY_SECRET"))
        print(request.headers.get("X-RapidAPI-Proxy-Secret") == os.environ.get("X_RAPIDAPI_PROXY_SECRET"))
              
        if request.headers.get("X-RapidAPI-Proxy-Secret") == os.environ.get("X_RAPIDAPI_PROXY_SECRET"):
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
        else:
            return make_response(jsonify({'error': 'Unauthorized access'}), 401)
        
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))