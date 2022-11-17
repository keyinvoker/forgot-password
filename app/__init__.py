from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

from app.config import Config
from app.blueprints import bp

app = Flask('Banana')
app.config.from_object(Config)

api = Api(bp)
db = SQLAlchemy(app)
ma = Marshmallow(app)

from app import routes
app.register_blueprint(bp)

CORS(app)