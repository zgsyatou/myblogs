from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

# 获取收藏对象
class CollectRecord(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete= models.CASCADE)
    object_id = models.PositiveIntegerField()
    fav = GenericForeignKey('content_type', 'object_id')

    user = models.ForeignKey(User, on_delete= models.CASCADE, verbose_name='收藏者')
    collect_time = models.DateTimeField(auto_now_add=True)

# 统计收藏数量
class CollectCount(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete= models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    collect_num = models.IntegerField(default = 0)
