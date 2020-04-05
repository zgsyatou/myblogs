from django.urls import path
from . import views

# 设置路由器信息，保证页面的正常访问
urlpatterns = [
    path('collect_change', views.collect_change, name='collect_change'),
    path('show_collect_info/', views.show_collect_info, name='show_collect_info'),
]