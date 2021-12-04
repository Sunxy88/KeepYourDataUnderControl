import os
from flask import Flask
from model import db
from views import api

def create_app() :

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = ''
    db.init_app(app)
    app.register_blueprint(api)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(port=int(os.environ.get('FLASK_PORT', 12345)))

