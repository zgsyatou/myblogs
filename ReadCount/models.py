from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import exceptions  # 导入错误集合
from django.utils import timezone


class ReadNum(models.Model):
    read_num = models.IntegerField(default = 0,verbose_name= '阅读数量')
    content_type = models.ForeignKey(ContentType, on_delete= models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

class ReadNumExpendMethod():
        #  定义方法，返回对应的博客阅读数量
    def get_read_num(self):
        try:
            ct =ContentType.objects.get_for_model(self)
            readnum = ReadNum.objects.get(content_type=ct, object_id= self.pk)
            return readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0 
# 定义统计没听的博客阅读数量
class ReadDetail(models.Model):
    date = models.DateField(default=timezone.now)  # 获取本地的服务器时间
    read_num = models.IntegerField(default = 0,verbose_name= '阅读数量')
    content_type = models.ForeignKey(ContentType, on_delete= models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')