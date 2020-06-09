                                                                        # APP:
# for init app                                                                        
from flask import Flask, request, jsonify

# serializator 
from flask_marshmallow import Marshmallow
# from marshmallow import fields, Schema, post_load

# models:
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String,Integer,Boolean,Float,ForeignKey, Column, DateTime
from sqlalchemy.orm import relationship, load_only
from werkzeug.security import generate_password_hash, check_password_hash

#api
from flask_rest_jsonapi import ResourceDetail, ResourceList ,ResourceRelationship,Api
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound
from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship,Schema
import os
import datetime

import json


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="mysql+pymysql://msb:qwe@localhost/db_7?charset=utf8mb4"
app.config["SECRET_KEY"]="SECRET_KEY_RIGHT_NOW"
app.config["debug"]=True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

db=SQLAlchemy(app)
# mongo_driver = PyMongo(app)

# db_users = mongo_driver.db.users

ma= Marshmallow(app)

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

@app.route("/<id>",methods=["GET","POST"])
def hello_request(id):
    print(request.json)
    print(request.args)
    print(request.values)
    print(request.url)

    return jsonify(request.json)



# MODELS
class Order_Article(db.Model):
    __tablename__='Order_Article'
    id= Column(Integer(), primary_key=True , nullable=False)
    order_id=Column(Integer, db.ForeignKey('Order.id'))
    article_id=Column(Integer, db.ForeignKey("Article.id"))
    item_able=Column(Integer, nullable=False)
    order=relationship("Order", back_populates="article_association")
    article_able=relationship("Article", back_populates="order_association")

    @property
    def items(self):
        return self.item_able
   
    @items.setter
    def items(self,quantity):
        if self.article is not None:
            if quantity < self.article_able.stock:#pendiente por arreglar en orderaritcle
                self.item_able = quantity
            else:
                raise AttributeError("item´s Quantity can´t be more than stock article")
        else:
            self.item_able=quantity
   
    @property
    def article(self):
        return self.article_able

    @article.setter
    def article(self,obj):
        if self.items is not None:
            if obj.stock > self.items:
                self.article_able=obj
            else:
                raise AttributeError("item´s Quantity can´t be more than stock article")
        else:
            self.article_able=obj
        
class Order(db.Model):
    __tablename__="Order"
    id= Column(Integer(), primary_key=True , nullable=False)
    status=Column(String(10),nullable=False, default="pendent")
    description=Column(String(100), default="")
    date=Column(DateTime, nullable=False, default=datetime.datetime.utcnow())
    article_association=relationship("Order_Article",back_populates="order")
    user_id=Column(Integer, ForeignKey("user.id"))
    user = relationship("User", lazy=True , backref="Order")
    
class Category(db.Model):
    # name que se debe poner, sino genera conflictos al importarlo
    __tablename__='Category'
    #Primary key como atributo
    id=Column(Integer, primary_key=True, nullable=False)
    name=Column(String(100), nullable=False, unique=True)# COLOCAR UNIQUE=TRUE

class Article(db.Model):
    __tablename__="Article"
    id=Column(Integer,nullable=False, primary_key=True)
    name=Column(String(50),nullable=False)
    price=Column(Float,nullable=False)
    iva=Column(Integer,default=21)
    description=Column(String(255))
    image=Column(String(255))
    stock=Column(Integer,default=0)
    CategoryId = Column(Integer, ForeignKey('Category.id'))
    #padre= object class Category
    category=relationship("Category",backref="article",lazy=True)
    order_association=relationship("Order_Article",back_populates="article_able")
    
    def price_with_iva(self):
        final.price= self.price*((self.iva/100)+1)
        return pricefinal

    def discount(self,quantity):
        if self.stock > quantity:
            self.stock-=quantity
        else:
            raise Exception("Quantity can´t be more than stock")
        
roles_users= db.Table('roles_users',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)    
class User(db.Model):
    id=Column(Integer,nullable=False, primary_key=True)
    username=Column(String(50),unique=True,nullable=False)
    password_hash=Column(String(255),unique=True,nullable=False)
    name=Column(String(50),nullable=False)
    email=Column(String(50),nullable=False)
    admin=Column(Boolean(),default=False)
    role=relationship("Role",backref="user",secondary=roles_users, lazy="subquery")

    @property
    def password(self):
        raise AttributeError("not allowed to read attribute password")
    
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash,password)
    
    # #Requisito en el modelo usuario para integrar con Flask-Login
    # @property
    # def is_authenticated(self):
    #     return True 
    # @property
    # def is_anonymous(self):
    #     return False
    # @property
    # def is_active(self):
    #     return True
    # #metodo requisito
    # def get_id(self):
    #     return self.id
    # #extra, NO requisito para Flask login
    # def is_admin(self):
    #     return self.admin

class Role(db.Model):
    id=Column(Integer, nullable=False, primary_key=True)
    name=Column(String(10), nullable=False, unique=True)

#SCHEMAS DEFINITIONS
class RoleSchema(Schema):
    class Meta:
        type_="role"
        self_view = "role_detail"
        self_view_kwargs={"id":"<id>"}
        self_view_many="role_list"
    id=fields.Integer(as_string=True, dump_only=True)
    name=fields.String()
    user=Relationship(
        related_view="user_list",
        related_view_kwargs={"role_id":"<id>"},
        self_view="role_users",
        self_view_kwargs={"id":"<id>"},
        many=True,
        schema="UserSchema",
        type_="user"
    )
    
class UserSchema(Schema):
    class Meta:
        type_="user"
        self_view = "user_detail"
        self_view_kwargs={"id":"<id>"}
        self_view_many="user_list"
    id=fields.Integer(as_string=True, dump_only=True)
    name=fields.String()
    username=fields.String()
    password=fields.String(load_only=True
    )
    email= fields.Email()
    admin=fields.Boolean()
    role=Relationship(
        attribute="role",
        related_view="role_list",
        related_view_kwargs={"user_id":"<id>"},
        # endpoint relationship CUIDADO POR AQUI
        self_view="user_roles" ,
        self_view_kwargs={"id":"<id>"},
        many=True,
        schema="RoleSchema",
        type_="role"
    )

    order=Relationship(
        attribute="Order",
        related_view="order_list",
        related_view_kwargs={"user_id":"<id>"},
        # endpoint relationship CUIDADO POR AQUI
        self_view="user_order" ,
        self_view_kwargs={"id":"<id>"},
        many=True,
        schema="OrderSchema",
        type_="order"
    )

class CategorySchema(Schema):
    class Meta:
        type_="category"
        self_view = "category_detail"
        self_view_kwargs={"id":"<id>"}
        self_view_many="category_list"
    id=fields.Integer(as_string=True, dump_only=True)
    name=fields.String()
    article=Relationship(
        related_view="article_list",
        related_view_kwargs={"category_id":"<id>"},
        self_view="category_articles",
        self_view_kwargs={"id":"<id>"},
        many=True,
        schema="ArticleSchema",
        type_="article"
    )

class ArticleSchema(Schema):
    class Meta:
        type_="article" 
        self_view="article_detail"
        self_view_kwargs={"id":"<id>"}
        self_viwe_many="article_list"
    id=fields.Integer(as_string=True, dump_only=True)
    name=fields.String()
    price=fields.Float()
    iva=fields.Float()
    description=fields.String()
    image=fields.String()
    stock=fields.Integer()
    CategoryId=fields.Integer(load_only=True)
    category=Relationship(
        related_view="category_detail",
        related_view_kwargs={"article_id":"<id>"},
        self_view="article_category",
        self_view_kwargs={"id":"<id>"},
        schema="CategorySchema",
        type_="category"
    )
        
#RESOURCES DEFINITIONS => data: diccionario para crear(POST) objeto de clase User/Role
# viewkwargs :diccionario que contiene todos los argumentos a ser ejecutados(GET) por view

#user
class UserDetail(ResourceDetail):
    def after_get(self,result):
        return jsonify(result)

    schema=UserSchema
    data_layer={
        "session":db.session,
        "model":User,
        "methods":{"after_get":after_get}
    }

class UserList(ResourceList):
    def query(self,view_kwargs):
        query_=self.session.query(User)
        if view_kwargs.get("role_id") is not None:
            try:
                # verificamos que exista el role con ese role_id
                self.session.query(Role).filter_by(id=view_kwargs.get["role_id"])
            except NoResultFound :
                raise ObjectNotFound({'parameter': 'id'}, "Role:{} not found".format(view_kwargs.get("role_id")))
            else:
                query_=query_.join(roles_users).join(Role).filter(Role.id==view_kwargs.get("role_id"))
                # lista de usuarios relaciondos con dicho Role
        return query_
    # para crear un usuario en el rol especificado
    # def before_create_object(self,data,view_kwargs):
    #     if view_kwargs.get("role_id") is not None:
    #         # obtenemos el objeto del role
    #         role_=self.session.query(Role).filter_by(id=view_kwargs["role_id"]).one()
    #         print(data)
    #         # diccionario a deserializar en una instancia de User.
    #         data["role_id"]=role_.id
    def before_get(*args,**kwargs):
        print(f"KWARGS:{kwargs},ARGS:{args}")
        print(args[0].__dict__)
    def after_get(self,result):
            return jsonify(result)
    get_schema_kwargs={"only":["name","email","password_hash"]}
    schema=UserSchema
    data_layer={
    "session":db.session,
    "model":User,
    "methods":{
        "query":query,
        # "before_create_object":before_create_object,
        "after_get":after_get
        }
    }
    
class UserRelationship(ResourceRelationship):

    def after_get(self, result):
        return jsonify(result)

    schema=UserSchema
    data_layer={
        "session":db.session,
        "model":User,
        "after_get":after_get
    }

#Role
class RoleDetail(ResourceDetail):
    def after_get(self,result):
        return jsonify(result)

    schema=RoleSchema
    data_layer={
        "session":db.session,
        "model":Role,
        "methods":{"after_get":after_get}
    }

class RoleList(ResourceList):
    def query(self,view_kwargs):
        query_=self.session.query(Role)
        if view_kwargs.get("user_id") is not None:
            try:
                # verificamos que exista el User con ese role_id
                self.session.query(User).filter_by(id=view_kwargs["user_id"])
            except NoResultFound :
                raise ObjectNotFound({'parameter': 'id'}, "User:{} not found".format(view_kwargs.get("user_id")))
            else:
                query_=query_.join(roles_users).join(User).filter(User.id==view_kwargs.get("user_id"))
        return query_
    # para crear un usuario en el rol especificado
    def before_create_object(self,data,view_kwargs):
        if view_kwargs.get("user_id") is not None:
            # obtenemos el objeto del role
            role_=self.session.query(User).filter(id=view_kwargs.get("user_id")).one()
            data["user_id"]=user_.id

    def after_get(self,result):
            return jsonify(result)

    schema=RoleSchema
    data_layer={
    "session":db.session,
    "model":Role,
    "methods":{
        "query":query,
        "before_create_object":before_create_object,
        "after_get":after_get
        }
    }
    
class RoleRelationship(ResourceRelationship):

    def after_get(self, result):
        return jsonify(result)

    schema=RoleSchema
    data_layer={
        "session":db.session,
        "model":Role,
        "after_get":after_get
    }

# Category
class CategoryDetail(ResourceDetail):
    def before_get_object(self,view_kwargs):
        if view_kwargs.get("article_id") is not None:
            try:
                art=self.session.query(Article).filter_by(id=view_kwargs["article_id"]).one()
            except NoResultFound :
                ObjectNotFound({"parameter":"article_id"},"Article {} not found".format(view_kwargs.get("article_id")))
            else:
                if art.category is not None:
                    view_kwargs["id"]=art.category.id
                else:
                    view_kwargs["id"]=None

    def after_get(self,result):
        return jsonify(result)

    schema=CategorySchema
    data_layer={
        "session":db.session,
        "model":Category,
        "methods":{
                "after_get":after_get,
                "before_get_object":before_get_object,
                }
    }

class CategoryList(ResourceList):

    def after_get(self,result):
            return jsonify(result)

    schema=CategorySchema
    data_layer={
    "session":db.session,
    "model":Category,
    "methods":{
        "after_get":after_get
        }
    }
    
class CategoryRelationship(ResourceRelationship):

    def after_get(self, result):
        return jsonify(result)

    schema=CategorySchema
    data_layer={
        "session":db.session,
        "model":Category,
        "after_get":after_get
    }

# Articles
class ArticleDetail(ResourceDetail):

    def after_get(self,result):
        return jsonify(result)

    schema=ArticleSchema
    data_layer={
        "session":db.session,
        "model":Article,
        "methods":{"after_get":after_get}
    }

class ArticleList(ResourceList):
    def query(self,view_kwargs):
        query_=self.session.query(Article)
        if view_kwargs.get("category_id") is not None:
            try:
                self.session.query(Category).filter_by(id=view_kwargs["category_id"]).one()
            except NoResultFound:
                raise ObjectNotFound({'parameter': 'id'}, "Category:{} not found".format(view_kwargs.get("category_id")))
            else:
                query_=query_.filter(Article.CategoryId == view_kwargs.get("category_id"))
                # retornando query de los usuarios relcionados con el rol especifiado por el id
        return query_
    def before_create_object(self,data, view_kwargs):
        if view_kwargs.get("category_id") is not None:
            print(f"CATEGORY CREATED DATA: {data}, VIEW_KWARGS:{view_kwargs}")
            try:
                category_=self.session.query(Category).filter_by(id=view_kwargs["category_id"]).one() 
                data["CategoryId"]=category_.id
            except NoResultFound:
                raise ObjectNotFound({'parameter': 'id'}, "Category:{} not found".format(view_kwargs.get("category_id")))

    def after_get(self,result):
            return jsonify(result)

    schema=ArticleSchema
    data_layer={
        "session":db.session,
        "model":Article,
        "methods":{
        "query":query,
        "before_create_object":before_create_object,
        "after_get":after_get
        }
    }
    
class ArticleRelationship(ResourceRelationship):

    def after_get(self, result):
        return jsonify(result)

    schema=ArticleSchema
    data_layer={
        "session":db.session,
        "model":Article,
        "after_get":after_get
    }



#ROUTES DEFINITIONS
api=Api(app)
# user
api.route(UserDetail,"user_detail","/user/<int:id>","order/<int:order_id>/user")#1
api.route(UserList,"user_list","/user", "/role/<int:role_id>/user")#
api.route(UserRelationship,"user_roles","/user/<int:id>/relationship/role")
# role
api.route(RoleDetail,"role_detail", "/role/<int:id>")
api.route(RoleList,"role_list", "/role" ,"/user/<int:user_id>/role")#
api.route(RoleRelationship,"role_users","/role/<int:id>/relationship/user")
# category
api.route(CategoryDetail,"category_detail","/category/<int:id>", "/article/<int:article_id>/category" )#
api.route(CategoryList, "category_list", "/category")
api.route(CategoryRelationship, "category_articles", "/category/<int:id>/relationship/article")

# articles
api.route(ArticleDetail,"article_detail","/article/<int:id>")
api.route(ArticleList, "article_list", "/article", "/category/<int:category_id>/article", "/order/<int:order_id>/article")#1
api.route(ArticleRelationship, "article_category", "/article/<int:id>/relationship/category")

class OrderSchema(Schema):
    class Meta:
        type_="order"
        self_view="order_detail"
        self_view_kwargs={'id':'<id>'}
        self_view_many="order_list"
    
    id=fields.Integer(as_string=True, dump_only=True)
    status=fields.String()
    description=fields.String()
    date=fields.DateTime()
    # lista de asociaciones
    article_association = Relationship(
        related_view="order_article_list",
        related_view_kwargs={"order_id":"<id>"},
        self_view="order_assc",
        self_view_kwargs={"id":"<id>"},
        many=True,
        schema="OrderArticleSchema",
        type_="order&article"
    )
    articles = Relationship(
        related_view="article_list",
        related_view_kwargs={"order_id":"<id>"},
        self_view="order_article",
        self_view_kwargs={"id":"<id>"},
        many=True,
        schema="ArticleSchema",
        type_="article"

    )
    # detalle de usuario
    user=Relationship(
        related_view="user_detail",
        related_view_kwargs={"order_id":"<id>"},
        self_view="order_user",
        self_view_kwargs={"id":"<id>"},
        schema="UserSchema",
        type_="user"
    )

    
    


# Order(1)
api.route(OrderDetail,"order_detail","/order/<int:id>")#  se podria añadir detalle de orden desde asociacion con dos ids 
api.route(OrderList, "order_list", "/order", "/user/<int:user_id>/order", "article/<int:article_id>/order")# P 
api.route(OrderAsscArticleRelationship, "order_assc", "/order/<int:id>/relationship/order&article")# 
api.route(OrderUserRelationship, "order_user", "/order/<int:id>/relationship/user")# 
api.route(OrderAsscArticleRelationship, "order_article", "/order/<int:id>/relationship/article")# trae lista de relaciones con articulos



class OrderArticleSchema(Schema):
    class Meta:
        self_view_many="order_article_list"

    order_id=Column(Integer, db.ForeignKey('Order.id'), primary_key=True, nullable=False)
    article_id=Column(Integer, db.ForeignKey("Article.id"), primary_key=True , nullable= False)
    item_able=Column(Integer, nullable=False)
    order=relationship("Order", back_populates="article_association")
    article_able=relationship("Article", back_populates="order_association")
    







# Order_Article:
# api.route(OrderArticleDetail,"order_article_detail","/order&article/<int:id>")# trae detalle de orden con relaciones con articulos y relacion con usuario
api.route(OrderArticleList, "order_article_list", "/order&article", "/order/<int:order_id>/order&article", "article/<int:article_id>/order&article")# trae lista de ordenes existentes / lista de ordenes relacionadas con un usuario 
# api.route(OrderArticleRelationship, "order_article_article", "/order&article/<int:id>/relationship/article")# trae lista de relaciones con articulos
# api.route(OrderUserRelationship, "order_article_order", "/order&article/<int:id>/relationship/user")# trae lista de relaciones con usuarios


if __name__ == "__main__":
    app.run(debug=True)
