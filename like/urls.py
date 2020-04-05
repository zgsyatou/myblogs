from django.urls import path
from . import views

# 设置路由器信息，保证页面的正常访问
urlpatterns = [
    path('like_change', views.like_change, name='like_change'),
]