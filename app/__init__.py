                                                                        # APP:
# for init app                                                                        

# serializator 
# from flask_marshmallow import Marshmallow
# from marshmallow import fields, Schema, post_load

# models:
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import String,Integer,Boolean,Float,ForeignKey, Column, DateTime
# from sqlalchemy.orm import relationship, load_only
# from werkzeug.security import generate_password_hash, check_password_hash

#api
# from flask_rest_jsonapi import ResourceDetail, ResourceList ,ResourceRelationship,Api
# from flask_rest_jsonapi.exceptions import ObjectNotFound
# from sqlalchemy.orm.exc import NoResultFound
# from marshmallow_jsonapi import fields
# from marshmallow_jsonapi.flask import Relationship,Schema

def create_app(configfile):
    
    from flask import Flask
    app = Flask(__name__)
    # app.config["DEBUG"]=True
    # app.config["SECRET_KEY"]="aDSDASDASDASDASFREE"
    # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
    # app.config["SQLALCHEMY_DATABASE_URI"]="mysql+pymysql://msb:qwe@localhost/db_8?charset=utf8mb4"
    # app.config["ENV"]="development"
    app.config.from_object(configfile)


    from .api_data_layer.api_v1 import api_v1
    app.register_blueprint(api_v1)

    from .ext import api,db,ma,migrate
    db.init_app(app)
    ma.init_app(app)
    api.init_app(app,api_v1)
    migrate.init_app(app,db)

    return app





    


# mongo_driver = PyMongo(app)

# db_users = mongo_driver.db.users


# TABLES MODELS DEFINITION 
# articles_orders= db.Table('articles_orders',
#     db.Column('article_id', db.Integer, db.ForeignKey('Article.id'), primary_key=True),
#     db.Column('order_id', db.Integer, db.ForeignKey('Order.id'), primary_key=True),
#     db.Column('items',db.Integer, nullable=False)
# )

# relationship Order => Order_Article <= Article ? trabajarlo con query
# relationship Order => Order_Article   ||  Order_Article <= Article
# Order ==> Order_Article ResourceRelationship/
# Article ==> Order_Article ResourceRelationship


# MODELS

#SCHEMAS   


#RESOURCES DEFINITIONS => data: diccionario para crear(POST) objeto de clase User/Role
# viewkwargs :diccionario que contiene todos los argumentos a ser ejecutados(GET) por view



#ROUTES DEFINITIONS
