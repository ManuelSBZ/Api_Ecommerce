from flask_marshmallow import Marshmallow
from flask_rest_jsonapi import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db=SQLAlchemy()
ma= Marshmallow()
api=Api()
migrate=Migrate()