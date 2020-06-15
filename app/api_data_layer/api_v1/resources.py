from app.ext import db
from .schemas import UserSchema,OrderArticleSchema,OrderSchema,CategorySchema,ArticleSchema,RoleSchema
from ..models import Article,Category,Order,Role,roles_users,User,Order_Article
from flask_rest_jsonapi import ResourceDetail, ResourceList ,ResourceRelationship,Api
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound
from flask import jsonify,request


#user
class UserDetail(ResourceDetail):
    def before_get_object(self, view_kwargs):
        if view_kwargs.get("id") is not None:
            try:
                self.session.query(self.model).filter_by(id= view_kwargs.get("id")).one()
            except NoResultFound:
                raise ObjectNotFound({"parameter":"id"},"{} {} not found".format(self.model.__tablename__,view_kwargs.get("id")))
            
        if view_kwargs.get("order_id") is not None:
            try:
                order=self.session.query(Order).filter_by(id=view_kwargs.get("order_id")).one()
            except NoResultFound :
                raise ObjectNotFound({"parameter":"order_id"},"order {} not found".format(view_kwargs.get("order_id")))
            else:
                if order.user is not None:
                    view_kwargs["id"]=order.user_id
                else:
                    view_kwargs["id"]=None
                    raise ObjectNotFound({"parameter":"order_id"},"Doesn´t have an related user")
        
        # PENDIENTE AGREGAR METODO PATCH PARA "/order/<int:order_id>/user"
    def before_marshmallow(self,args,kwargs):
        if request.method=="PATCH":
            key=[key for key,v in kwargs.items()][0]
            print(kwargs)
            if key != "id":
                if kwargs.get(key) is not None :
                    try:
                        order_=self.data_layer["session"].query(Order).filter_by(id=kwargs[key]).one()
                    except NoResultFound:
                        raise ObjectNotFound({"parmeter":"user_id"},"User {} not Found".format(kwargs[key]))
                    else:
                        if order_.user_id:
                            kwargs["id"]=order_.user_id
                        else:
                            raise ObjectNotFound({"parameter:Object related"},"Doesnt exits any user related") 
    def after_get(self,result):
        return jsonify(result)

    schema=UserSchema
    data_layer={
        "session":db.session,
        "model":User,
        "methods":{
            "after_get":after_get,
            "before_get_object":before_get_object
        }
    }

class UserList(ResourceList):
    def query(self,view_kwargs):
        query_=self.session.query(User)
        if view_kwargs.get("role_id") is not None:
            try:
                # verificamos que exista el role con ese role_id
                self.session.query(Role).filter_by(id=view_kwargs.get("role_id"))
            except NoResultFound :
                raise ObjectNotFound({'parameter': 'id'}, "Role:{} not found".format(view_kwargs.get("role_id")))
            else:
                query_=query_.join(roles_users).join(Role).filter(Role.id==view_kwargs.get("role_id"))
                # lista de usuarios relaciondos con dicho Role
        return query_
    # para crear un usuario en el rol especificado
    def before_create_object(self,data,view_kwargs):
        pass
    def after_create_object(self, obj, data, view_kwargs):
        if view_kwargs.get("role_id") is not None:
            # obtenemos el objeto del role
            print("after_create_o")
            Parent=self.session.query(Role).filter_by(id=view_kwargs["role_id"]).one()
            child=obj
            print(f"OBJETO USER: {child.__dict__}")
            Parent.user.append(child)
            print("session.commit()")
            
            self.session.commit()
            # con return no hace nada
            
    # def after_create_object

    # def before_get(*args,**kwargs):
    #     print(f"KWARGS:{kwargs},ARGS:{args}")
    #     print(args[0].__dict__)
    def after_get(self,result):
            return jsonify(result)
    get_schema_kwargs={"only":["name","email","username","admin"]}
    schema=UserSchema
    data_layer={
    "session":db.session,
    "model":User,
    "methods":{
        "query":query,
        "after_create_object":after_create_object,
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
        "methods":{
            "after_get":after_get,
            }
    }

class UserOrderRelationship(ResourceRelationship):
    
    def after_get(self, result):
        return jsonify(result)

    schema=UserSchema
    data_layer={
        "session":db.session,
        "model":User,
        "methods":{
            "after_get":after_get
            }
    }
#Role
class RoleDetail(ResourceDetail):
    def before_get_object(self,view_kwargs):
        if view_kwargs.get("id") is not None:
            try:
                self.session.query(self.model).filter_by(id= view_kwargs["id"]).one()
            except NoResultFound:
                raise ObjectNotFound({"parameter":"id"},"{} {} not found".format(self.model.__tablename__,view_kwargs.get("id")))
    def after_get(self,result):
        return jsonify(result)

    schema=RoleSchema
    data_layer={
        "session":db.session,
        "model":Role,
        "methods":{
            "after_get":after_get,
            "before_get_object":before_get_object
        }
    }

class RoleList(ResourceList):
    def query(self,view_kwargs):
        query_=self.session.query(Role)
        if view_kwargs.get("user_id") is not None:
            try:
                # verificamos que exista el User con ese role_id
                self.session.query(User).filter_by(id=view_kwargs["user_id"])
            except NoResultFound:
                raise ObjectNotFound({'parameter': 'id'}, "User:{} not found".format(view_kwargs.get("user_id")))
            else:
                query_=query_.join(roles_users).join(User).filter(User.id==view_kwargs.get("user_id"))
        return query_
    # para crear un usuario en el rol especificado
    def after_create_object(self,obj,data,view_kwargs):
        if view_kwargs.get("user_id") is not None:
            role_=obj
            user_=self.session.query(User).filter_by(id=view_kwargs["user_id"]).one()
            user_.role.append(role_)
            self.session.commit()

    def after_get(self,result):
            return jsonify(result)

    schema=RoleSchema
    data_layer={
    "session":db.session,
    "model":Role,
    "methods":{
        "query":query,
        "after_create_object":after_create_object,
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
        "methods":{
        "after_get":after_get        }
    }

# Category
class CategoryDetail(ResourceDetail):
    def before_get_object(self,view_kwargs):
        if view_kwargs.get("id") is not None:
            print("idddddddddddddd")
            try:  
                self.session.query(self.model).filter_by(id= view_kwargs["id"]).one()
            except NoResultFound:
                raise ObjectNotFound({"parameter":"id"},"{} {} not found".format(self.model.__tablename__,view_kwargs.get("id")))        
        if view_kwargs.get("article_id") is not None:
            try:
                art=self.session.query(Article).filter_by(id=view_kwargs["article_id"]).one()
            except NoResultFound :
                raise ObjectNotFound({"parameter":"article_id"},"Article {} not found".format(view_kwargs.get("article_id")))
            else:
                if art.category is not None:
                    print("AQEUIIII")
                    view_kwargs["id"]=art.CategoryId
                else:
                    
                    raise ObjectNotFound({"parameter":"id"},"Doesnt have any Category related")

    def before_marshmallow(self,args,kwargs):
        if request.method=="PATCH":
            key=[key for key,v in kwargs.items()][0]
            if key!="id":
                if kwargs.get(key) is not None:
                    try:
                        article_=self.data_layer["session"].query(Article).filter_by(id=kwargs[key]).one()
                    except NoResultFound:
                        raise ObjectNotFound({"parmeter":"article_id"},"Article {} not Found".format(kwargs[key]))
                    else:
                        if article_.CategoryId:
                            kwargs["id"]=article_.CategoryId
                        else:
                            raise ObjectNotFound({"parameter: Object related"},"Doesnt exits any category related")
        


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
        "methods":{
        "after_get":after_get
        }
    }

# Articles
class ArticleDetail(ResourceDetail):
    def before_get_object(self, view_kwargs):
        if view_kwargs.get("id") is not None:
            try:
                self.session.query(self.model).filter_by(id= view_kwargs["id"]).one()
            except NoResultFound:
                raise ObjectNotFound({"parameter":"id"},"{} {} not found".format(self.model.__tablename__,view_kwargs.get("id")))
        if view_kwargs.get("orderarticle_id") is not None:
            try:
                assc=self.session.query(Order_Article).filter_by(id=view_kwargs["orderarticle_id"]).one()
            except NoResultFound :
                raise ObjectNotFound({"parameter":"orderarticle_id"},"Article {} not found".format(view_kwargs.get("orderarticle_id")))
            else:
                if assc.article_able is not None:
                    view_kwargs["id"]=assc.article_able.id
                else:
                    raise ObjectNotFound({"parameter":"orderarticle_id"},"Doesn't have any article related")
    def before_marshmallow(self,args,kwargs):
        if request.method=="PATCH":
            key=[key for key,v in kwargs.items()][0]
            if key!="id":
                if kwargs.get(key) is not None:
                    try:
                        assc=self.data_layer["session"].query(Order_Article).filter_by(id=kwargs[key]).one()
                    except NoResultFound:
                        raise ObjectNotFound({"parmeter":"orderarticle_id"},"Order_Article {} not Found".format(kwargs[key]))
                    else:
                        if assc.article_id:
                            kwargs["id"]=assc.article_id
                        else:
                            raise ObjectNotFound({"parameter:Object related"},"Doesnt exits any article related")
        

        

    def after_get(self,result):
        return jsonify(result)

    schema=ArticleSchema
    data_layer={
        "session":db.session,
        "model":Article,
        "methods":{
            "after_get":after_get,
            "before_get_object":before_get_object
        }
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
        "methods":{
        "after_get":after_get
        }
    }
class ArticleAsscOrderRelationship(ResourceRelationship):

    def after_get(self, result):
        return jsonify(result)

    schema=ArticleSchema
    data_layer={
        "session":db.session,
        "model":Article,
        "methods":{
            "after_get":after_get
        }
    }

#order

class OrderDetail(ResourceDetail):
    def before_get_object(self, view_kwargs):
        if view_kwargs.get("id") is not None:
            try:
                self.session.query(self.model).filter_by(id= view_kwargs["id"]).one()
            except NoResultFound:
                raise ObjectNotFound({"parameter":"id"},"{} {} not found".format(self.model.__tablename__,view_kwargs.get("id")))            
        if view_kwargs.get("orderarticle_id") is not None:
            try:
                assc=self.session.query(Order_Article).filter_by(id=view_kwargs["orderarticle_id"]).one()
            except NoResultFound :
                raise ObjectNotFound({"parameter":"orderarticle_id"},"Article {} not found".format(view_kwargs.get("orderarticle_id")))
            else:
                if assc.order is not None:
                    view_kwargs["id"]=assc.order.id
                else:
                    raise ObjectNotFound({"parameter":"Order"},"Doesn´t have any related order ")

    def before_marshmallow(self,args,kwargs):
        if request.method=="PATCH":
            key=[key for key,v in kwargs.items()][0]
            if key!="id":
                if kwargs.get(key) is not None:
                    try:
                        assc=self.data_layer["session"].query(Order_Article).filter_by(id=kwargs[key]).one()
                    except NoResultFound:
                        raise ObjectNotFound({"parmeter":"orderarticle_id"},"OrderArticle {} not Found".format(kwargs[key]))
                    else:
                        if assc.order_id:
                            kwargs["id"]=assc.order_id
                        else:
                            raise ObjectNotFound({"parameter:Object related"},"Doesnt exits any order related")
    

                    
    def after_get(self,result):
        return jsonify(result)

    schema=OrderSchema
    data_layer={
        "session":db.session,
        "model":Order,
        "methods":{
            "after_get":after_get,
            "before_get_object":before_get_object,
        }
    }

class OrderList(ResourceList):
    def query(self,view_kwargs):
        query_=self.session.query(Order)
        if view_kwargs.get("user_id") is not None:
            arg="user_id"
            model=User
        elif view_kwargs.get("article_id"):
            arg="article_id"
            model=Order_Article
        else:
            arg=""
            model=None

        if view_kwargs.get(arg) is not None:
            try:
                self.session.query(model).filter_by(id=view_kwargs[arg]).one()
            except NoResultFound:
                raise ObjectNotFound({'parameter': arg}, "{}:{} not found".format(model.__tablename__,view_kwargs.get(arg)))
            else:
                query_=query_.join(model).filter(model.id==view_kwargs.get(arg))
                # retornando query de los usuarios relcionados con el rol especifiado por el id
        return query_

    def before_create_object(self,data, view_kwargs):
        if view_kwargs.get("user_id") is not None:
            print(f"CATEGORY CREATED DATA: {data}, VIEW_KWARGS:{view_kwargs}")
            try:
                user_=self.session.query(User).filter_by(id=view_kwargs["user_id"]).one() 
                data["user_id"]=user_.id
            except NoResultFound:
                raise ObjectNotFound({'parameter': 'id'}, "User:{} not found".format(view_kwargs.get("user_id")))

    def after_get(self,result):
            return jsonify(result)

    schema=OrderSchema
    data_layer={
        "session":db.session,
        "model":Order,
        "methods":{
            "query":query,
            "before_create_object":before_create_object,
            "after_get":after_get
        }
    }
    
class OrderUserRelationship(ResourceRelationship):

    def after_get(self, result):
        return jsonify(result)

    schema=OrderSchema
    data_layer={
        "session":db.session,
        "model":Order,
        "methods":{
            "after_get":after_get
            }
    }

class OrderAsscArticleRelationship(ResourceRelationship):

    def after_get(self, result):
        return jsonify(result)

    schema=OrderSchema
    data_layer={
        "session":db.session,
        "model":Order,
        "methods":{
            "after_get":after_get
            }
    }

class OrderArticleRelationship(ResourceRelationship):

    def after_get(self, result):
        return jsonify(result)

    schema=OrderSchema
    data_layer={
        "session":db.session,
        "model":Order,
        "methods":{
            "after_get":after_get
            }
    }

# orderarticles
class OrderArticleDetail(ResourceDetail):
    
    def before_get_object(self,view_kwargs):
        if view_kwargs.get("id") is not None:
            try:
                self.session.query(self.model).filter_by(id= view_kwargs["id"]).one()
            except NoResultFound:
                raise ObjectNotFound({"parameter":"id"},"{} {} not found".format(self.model.__tablename__,view_kwargs.get("id")))
    def after_get(self,result):
        return jsonify(result)

    schema=OrderArticleSchema
    data_layer={
        "session":db.session,
        "model":Order_Article,
        "methods":{
            "after_get":after_get,
            "before_get_object":before_get_object
            }
    }

class OrderArticleList(ResourceList):
    def query(self,view_kwargs):
        query_=self.session.query(Order_Article)
        if view_kwargs.get("order_id") is not None:
            arg="order_id"
            model=Order
        elif view_kwargs.get("article_id") is not None:
            arg="article_id"
            model=Article
        else:
            arg=""
            model=None

        if view_kwargs.get(arg) is not None:
            try:
                self.session.query(model).filter_by(id=view_kwargs[arg]).one()
            except NoResultFound:
                raise ObjectNotFound({'parameter': arg}, "{}:{} not found".format(model.__tablename__,view_kwargs.get(arg)))
            else:
                query_=query_.join(model).filter(model.id==view_kwargs.get(arg))
                # retornando query de los usuarios relcionados con el rol especifiado por el id
        return query_

    def before_create_object(self,data, view_kwargs):
        if view_kwargs.get("order_id") is not None:
            arg="order_id"
            model=Order
        elif view_kwargs.get("article_id") is not None:
            arg="article_id"
            model=Article
        else:
            arg=""
            model=None
        if view_kwargs.get(arg) is not None:
            print(f"CATEGORY CREATED DATA: {data}, VIEW_KWARGS:{view_kwargs}")
            try:
                model_=self.session.query(model).filter_by(id=view_kwargs[arg]).one() 
                data[arg]=model_.id
            except NoResultFound:
                raise ObjectNotFound({'parameter': 'id'}, "{}:{} not found".format(model.__tablename__,view_kwargs.get("user_id")))
        print(data)
    def after_get(self,result):
            return jsonify(result)

    schema=OrderArticleSchema
    data_layer={
        "session":db.session,
        "model":Order_Article,
        "methods":{
            "query":query,
            "before_create_object":before_create_object,
            "after_get":after_get
        }
    }
    
class OrderArticleArticleRelationship(ResourceRelationship):
    
    def after_get(self, result):
        return jsonify(result)

    schema=OrderArticleSchema
    data_layer={
        "session":db.session,
        "model":Order_Article,
        "methods":{
            "after_get":after_get
            }
    }

class OrderArticleOrderRelatioship(ResourceRelationship):

    def after_get(self, result):
        return jsonify(result)

    schema=OrderArticleSchema
    data_layer={
        "session":db.session,
        "model":Order_Article,
        "methods":{
            "after_get":after_get
            }
    }
