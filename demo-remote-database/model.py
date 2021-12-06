import uuid

from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import event
# from werkzeug.utils import secure_filename

# import config

db = SQLAlchemy()

class SerializableModelMixin:

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items() if isinstance(value, (int, str))}

class TextResource(db.Model, SerializableModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    resource = db.Column(db.String())

class ImageResource(db.Model, SerializableModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    resource = db.Column(db.LargeBinary(length=(2**32)-1))
