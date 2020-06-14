from flask import Blueprint
from .resources import *
from app.ext import api


api_v1 = Blueprint("api_v1",__name__)


# user
api.route(UserDetail,"user_detail","/user/<int:id>","/order/<int:order_id>/user")#GET PATCH DELETE,          pendiente el post user, cambiar al resource list 
api.route(UserList,"user_list","/user", "/role/<int:role_id>/user")#GET users, POST User.
api.route(UserRelationship,"user_roles","/user/<int:id>/relationship/role")#GET POST PATCH DELETE relationship
api.route(UserOrderRelationship,"user_order","/user/<int:id>/relationship/order")#GET POST PATCH DELETE relationship 
# role
api.route(RoleDetail,"role_detail", "/role/<int:id>") #GET PATCH DELETE role
api.route(RoleList,"role_list", "/role" ,"/user/<int:user_id>/role") #GET POST role, POST role=>user
api.route(RoleRelationship,"role_users","/role/<int:id>/relationship/user") #GET POST PATCH DELETE relationship            
# category
api.route(CategoryDetail,"category_detail","/category/<int:id>", "/article/<int:article_id>/category") #GET PATCH DELETE category   
api.route(CategoryList, "category_list", "/category") #GET POST CATEGORY
api.route(CategoryRelationship, "category_articles", "/category/<int:id>/relationship/article") #GET POST PATCH DELETE relationship     DELETE NO FUNCION CORREGIR 204

# articles
api.route(ArticleDetail,"article_detail","/article/<int:id>","/orderarticle/<int:orderarticle_id>/article")##GET PATCH DELETE USER E PATCH ARTICLE_ID
api.route(ArticleList, "article_list", "/article", "/category/<int:category_id>/article")#GET POST ARTICLE, POST ARTICLE => CATEGORY
api.route(ArticleRelationship, "article_category", "/article/<int:id>/relationship/category")#GET POST PATCH DELETE relationship
api.route(ArticleAsscOrderRelationship, "article_assc", "/article/<int:id>/relationship/orderarticle")#GET POST PATCH DELETE relationship

# Order(1)
api.route(OrderDetail,"order_detail","/order/<int:id>", "/orderarticle/<int:orderarticle_id>/order")# GET PATCH DELETE ORDER
api.route(OrderList, "order_list","/order","/user/<int:user_id>/order","/articleorder/<int:article_id>/order")## GET POST ORDER, POST ORDER =>USER
api.route(OrderAsscArticleRelationship, "order_assc","/order/<int:id>/relationship/orderarticle")#GET POST PATCH DELETE relationship
api.route(OrderUserRelationship, "order_user","/order/<int:id>/relationship/user")##GET POST PATCH DELETE relationship
   
# Order_Article:
api.route(OrderArticleDetail,"orderarticle_detail","/orderarticle/<int:id>")# GET PATCH DELETE ORDER_ARTICLE ASSOCIATION

api.route(OrderArticleList, "orderarticle_list", 
         "/orderarticle", 
         "/order/<int:order_id>/orderarticle", 
         "/article/<int:article_id>/orderarticle")##GET POST ARTICLE_ASSOCIATION, POST ORDER_ARTICLE => ORDER, POST ORDER_ARTICLE => ARTICLE

api.route(OrderArticleArticleRelationship, "orderarticle_article", "/orderarticle/<int:id>/relationship/article")#GET POST PATCH DELETE relationship

api.route(OrderArticleOrderRelatioship, "orderarticle_order", "/orderarticle/<int:id>/relationship/order")#GET POST PATCH DELETE relationship
