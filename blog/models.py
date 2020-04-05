from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
# 导入富文本编辑
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from ReadCount.models import ReadNumExpendMethod, ReadDetail

class BlogType(models.Model):
    '''设置博文的类型，在Blog中展示，外键进行连接'''
    type_name = models.CharField(max_length= 15)

    def __str__(self):
        return self.type_name

class Blog(models.Model,ReadNumExpendMethod):
    '''创建博文的相关的属性，设置相关的字段名称，不设置任何的默认值'''
    title = models.CharField(verbose_name= '标题',max_length= 50)
    blog_type = models.ForeignKey(BlogType, on_delete= models.CASCADE,verbose_name= '类型') # 设置外键，第一个属性为表明
    content = RichTextUploadingField(verbose_name= '内容')
    author = models.ForeignKey(User, on_delete= models.CASCADE,verbose_name= '作者')
    read_details = GenericRelation(ReadDetail)    # 使用自带的方法，关联两个模型
    create_time = models.DateTimeField(verbose_name= '创建时间',auto_now_add = True)
    update_time = models.DateTimeField( verbose_name= '更新时间',auto_now = True)
        
    # 返回用户
    def get_user(self):
        return self.author

    # 返回具体链接
    def get_url(self):
        return reverse('blog_details', kwargs={'blog_pk': self.pk})

    # 返回评论对象讲的email
    def get_email(self):
        return self.author.email
 
    def __str__(self):
        return '<Blog: %s>'% Blog.title
    
    class Meta:
        ordering = ['-create_time']
 