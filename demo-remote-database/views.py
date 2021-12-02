from datetime import datetime

from flask import (
    abort,
    Blueprint,
    jsonify,
    request,
    Response,
)

from model import Student, db, TextResource

api = Blueprint('api', __name__, url_prefix="")


@api.route('/')
def index():
    return "hello,world"

@api.route('/text/<int:id>', methods=['GET'])
def getText(id):
    text = TextResource.query.get(id)
    print(text.to_dict())

    return jsonify(text.resource)

@api.route('/text', methods=['POST'])
def createText(): 
    res = -1

    if request.content_type.startswith("application/json"):
        content = request.json
        text = content.get('text')
        textResource = TextResource(resource=text)
        db.session.add(textResource)
        db.session.commit()
        db.session.refresh(textResource)
        res = textResource.id

    if res != -1:
        res = "http://127.0.0.1:12345/text/" + str(res)
        return jsonify(res)
    else:
        return ""

@api.route('/student/<int:id>', methods=['GET'])
def testGet(id):
    students = Student.query.get(id)
    print(students.to_dict())

    return jsonify(students.to_dict())

@api.route('/student', methods=['POST'])
def testPost(): 
    res = -1

    if request.content_type.startswith("application/json"):
        content = request.json
        id = content.get('id')
        name = content.get('name')
        student = Student(id=id, name=name)
        db.session.add(student)
        db.session.commit()
        db.session.refresh(student)
        res = student.id

    return jsonify(res)