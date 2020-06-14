from app.ext import db
# from db import BaseModelMixin
from sqlalchemy import String,Integer,Boolean,Float,ForeignKey, Column, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

class Order_Article(db.Model):
    __tablename__='Order_Article'
    id= Column(Integer(), primary_key=True , nullable=False)
    order_id=Column(Integer, ForeignKey('Order.id'))
    article_id=Column(Integer, ForeignKey("Article.id"))
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
