from app.ext import ma
from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship,Schema

class RoleSchema(Schema):
    class Meta:
        type_="role"
        self_view = "api_v1.role_detail"
        self_view_kwargs={"id":"<id>"}
        self_view_many="api_v1.role_list"
    id=fields.Integer(as_string=True, dump_only=True)
    name=fields.String()
    user=Relationship(
        related_view="api_v1.user_list",
        related_view_kwargs={"role_id":"<id>"},
        self_view="api_v1.role_users",
        self_view_kwargs={"id":"<id>"},
        many=True,
        schema="UserSchema",
        type_="user"
    )
    
class UserSchema(Schema):
    class Meta:
        type_="user"
        self_view = "api_v1.user_detail"
        self_view_kwargs={"id":"<id>"}
        self_view_many="api_v1.user_list"
    id=fields.Integer(as_string=True, dump_only=True)
    name=fields.String()
    username=fields.String()
    password=fields.String(load_only=True
    )
    email= fields.Email()
    admin=fields.Boolean()
    role=Relationship(
        attribute="role",
        related_view="api_v1.role_list",
        related_view_kwargs={"user_id":"<id>"},
        # endpoint relationship CUIDADO POR AQUI
        self_view="api_v1.user_roles" ,
        self_view_kwargs={"id":"<id>"},
        many=True,
        schema="RoleSchema",
        type_="role"
    )

    order=Relationship(
        attribute="Order",
        related_view="api_v1.order_list",
        related_view_kwargs={"user_id":"<id>"},
        # endpoint relationship CUIDADO POR AQUI
        self_view="api_v1.user_order" ,
        self_view_kwargs={"id":"<id>"},
        many=True,
        schema="OrderSchema",
        type_="order"
    )

class CategorySchema(Schema):
    class Meta:
        type_="category"
        self_view = "api_v1.category_detail"
        self_view_kwargs={"id":"<id>"}
        self_view_many="api_v1.category_list"
    id=fields.Integer(as_string=True, dump_only=True)
    name=fields.String()
    article=Relationship(
        related_view="api_v1.article_list",
        related_view_kwargs={"category_id":"<id>"},
        self_view="api_v1.category_articles",
        self_view_kwargs={"id":"<id>"},
        many=True,
        schema="ArticleSchema",
        type_="article"
    )

class ArticleSchema(Schema):
    class Meta:
        type_="article" 
        self_view="api_v1.article_detail"
        self_view_kwargs={"id":"<id>"}
        self_viwe_many="api_v1.article_list"
    id=fields.Integer(as_string=True, dump_only=True)
    name=fields.String()
    price=fields.Float()
    iva=fields.Float()
    description=fields.String()
    image=fields.String()
    stock=fields.Integer()
    CategoryId=fields.Integer(load_only=True)
    category=Relationship(
        related_view="api_v1.category_detail",
        related_view_kwargs={"article_id":"<id>"},
        self_view="api_v1.article_category",
        self_view_kwargs={"id":"<id>"},
        schema="CategorySchema",
        type_="category"
    )
    orderarticle=Relationship(
        attribute="order_association",
        related_view="api_v1.orderarticle_list",
        related_view_kwargs={"article_id":"<id>"},
        self_view="api_v1.article_assc",
        self_view_kwargs={"id":"<id>"},
        schema="OrderArticleSchema",
        type_="orderarticle"
    )
        
class OrderSchema(Schema):
    class Meta:
        type_="order"
        self_view="api_v1.order_detail"
        self_view_kwargs={'id':'<id>'}
        self_view_many="api_v1.order_list"
    
    id=fields.Integer(as_string=True, dump_only=True)
    status=fields.String()
    description=fields.String()
    date=fields.DateTime()
    # lista de asociaciones
    orderarticle = Relationship(
        attribute="article_association", #que coño es esto
        related_view="api_v1.orderarticle_list",
        related_view_kwargs={"order_id":"<id>"},
        self_view="api_v1.order_assc",
        self_view_kwargs={"id":"<id>"},
        many=True,
        schema="OrderArticleSchema",
        type_="orderarticle"
    )
    # articles = Relationship(
    #     related_view="article_list",
    #     related_view_kwargs={"order_id":"<id>"},
    #     self_view="order_article",
    #     self_view_kwargs={"id":"<id>"},
    #     many=True,
    #     schema="ArticleSchema",
    #     type_="article"
    # )

    # detalle de usuario
    user=Relationship(
        related_view="api_v1.user_detail",
        related_view_kwargs={"order_id":"<id>"},
        self_view="api_v1.order_user",
        self_view_kwargs={"id":"<id>"},
        schema="UserSchema",
        type_="user"
    )

class OrderArticleSchema(Schema):
    class Meta:
        type_="orderarticle"
        self_view_many="api_v1.orderarticle_list"
        self_view="api_v1.orderarticle_detail"
        self_view_kwargs={"id":"<id>"}

    id=fields.Integer(as_string=True, dump_only=True)
    order_id= fields.Integer()
    article_id=fields.Integer()
    item_able=fields.Integer()
    items=fields.Integer(load_only=True)
    order=Relationship(
        related_view="api_v1.order_detail",
        related_view_kwargs={"orderarticle_id":"<id>"},
        self_view="api_v1.orderarticle_order",
        self_view_kwargs={"id":"<id>"},
        schema="OrderSchema",
        type_="order"
    )
    article=Relationship(
        attribute="article_able",
        related_view="api_v1.article_detail",
        related_view_kwargs={"orderarticle_id":"<id>"},
        self_view="api_v1.orderarticle_article",
        self_view_kwargs={"id":"<id>"},
        schema="ArticleSchema",
        type_="article"
    )
