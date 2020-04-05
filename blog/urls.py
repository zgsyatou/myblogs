from django.urls import path
from . import views

# 设置路由器信息，保证页面的正常访问
urlpatterns = [
    # 设置博客的展示路由，网址为：http:127.0.0.1:8000/blog
    path('', views.blog_list, name='blog_list'),
    # 设置博客内容的网页地址：http:127.0.0.1:8000/blog/1
    path('<int:blog_pk>', views.blog_details, name= 'blog_details'),
    path('type/<int:blog_type_pk>', views.blog_with_type, name= 'blog_type'),
    # 设置博客按月分类的链接
    path ('date/<int:year>/<int:month>', views.blog_with_date, name='blog_with_date')
]