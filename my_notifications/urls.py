from django.urls import path
from . import views

# 设置路由器信息，保证页面的正常访问
urlpatterns = [
    path('',views.my_notifications, name= 'my_notifications'),
    path('<int:my_notification_pk>',views.my_notification, name= 'my_notification'),
    path('delete_my_readed_notifications',views.delete_my_readed_notifications, name= 'delete_my_readed_notifications'),
]