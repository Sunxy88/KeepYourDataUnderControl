import os
import os.path
from datetime import datetime
import json

from flask import (
    abort,
    Blueprint,
    jsonify,
    request,
    Response,
)
from werkzeug.utils import secure_filename

from model import db, TextResource, ImageResource
from config import BASE_HOST, UPLOAD_FOLDER

api = Blueprint('api', __name__, url_prefix="")


@api.route('/', methods=['GET'])
def index():
    return "hello,world"

@api.route('/', methods=['POST'])
def upload_resource():
    if 'file' not in request.files:
        abort(Response("Missing file", 400))
    
    file = request.files['file']
    if file.filename == '':
        abort(Response("Empty filename", 400))

    filename = secure_filename(file.filename)
    # temporarily save file
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)
    extension = os.path.splitext(filename)[-1]
    if extension == '.txt':
        with open(file_path) as file:
            text = file.read()
            print(text)
            res = save_text(text)
            if res != -1:
                res = BASE_HOST + "/text/" + str(res)
                res = jsonify(url=res)
                return res
            else:
                return ""
    if extension == '.jpg':
        with open(file_path, 'rb') as file:
            img = file.read()
            res = save_image(img)
            if res != -1:
                res = BASE_HOST + "/image/" + str(res)
                return jsonify(url=res)
            else:
                return ""
    return ""

@api.route('/image/<int:id>', methods=['GET'])
def get_image(id):
    image = ImageResource.query.get(id)
    resp = Response(image.resource, mimetype="image/jpeg")
    return resp

@api.route('/text/<int:id>', methods=['GET'])
def get_text(id):
    text = TextResource.query.get(id)
    print(text.to_dict())

    return jsonify(text.resource)

@api.route('/text', methods=['POST'])
def create_text(): 
    res = -1

    if request.content_type.startswith("application/json"):
        content = request.json
        text = content.get('text')
        res = save_text(text)

    if res != -1:
        res = BASE_HOST + "/text/" + str(res)
        return jsonify(res)
    else:
        return ""

def save_text(text):
    text_resource = TextResource(resource=text)
    db.session.add(text_resource)
    db.session.commit()
    db.session.refresh(text_resource)
    res = text_resource.id
    return res

def save_image(image):
    image_resource = ImageResource(resource=image)
    db.session.add(image_resource)
    db.session.commit()
    db.session.refresh(image_resource)
    return image_resource.id