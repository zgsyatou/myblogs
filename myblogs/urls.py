"""myblogs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include,path
from django.conf import settings
from django.conf.urls.static import static
from . import  views

urlpatterns = [
    # 设置网站的首页，并且引入相关的方法，命名为index
    path('', views.index, name= 'index'),
    path('admin/', admin.site.urls),
    # 设置图片上传的url
    path('ckeditor',include('ckeditor_uploader.urls')),
    # 设置总的路由，并且导入相关的url文件
    path('blog/',include('blog.urls')),
    path('comment/',include('comment.urls')),
    path('like/',include('like.urls')),
    path('user/',include('user.urls')),
    path('notifications/', include('notifications.urls', namespace='notifications')),
    path('my_notifications/',include('my_notifications.urls')),
    path('search/', views.search, name= 'search'),
    path('collected/',include('collected.urls')),
]
# 设置对应的图片出啊到的位置路径
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

