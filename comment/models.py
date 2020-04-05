from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete= models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField(verbose_name= '评论内容')
    comment_time = models.DateTimeField(auto_now_add=True, verbose_name= '评论时间')
    comment_user =models.ForeignKey(User, related_name='comments', on_delete= models.CASCADE, verbose_name='评论者')

    # 创建一个字段来记录一条评论下的所有回复
    top = models.ForeignKey('self', related_name= 'top_comment', null= True, on_delete= models.CASCADE, verbose_name='品论这条')
    # 回复功能的字段名,使用related_name来解决关联两个外键的冲突的方法
    parent = models.ForeignKey('self', related_name= 'paren_comment', null= True, on_delete= models.CASCADE, verbose_name= '品论这条')
    reply_to = models.ForeignKey(User, related_name='replies', null= True, on_delete= models.CASCADE, verbose_name='回复者')

    def __str__(self):
        return self.text

    def get_url(self):
        return self.content_object.get_url()

    def get_user(self):
        return self.comment_user

    class Meta:
        ordering = ['comment_time']
        