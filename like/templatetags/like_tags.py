from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import LikeCount, LikeRecord

register = template.Library()

@register.simple_tag
#获取点赞数量
def get_like_num(obj):
    content_type = ContentType.objects.get_for_model(obj)
    like_count, created = LikeCount.objects.get_or_create(content_type= content_type, object_id= obj.pk)
    return like_count.like_num 

@register.simple_tag(takes_context= True)   # takes_context= True 阔以获取到模板页面的对象
# 获取active的状态，使点赞图标改变
def get_like_status(context, obj):
    user= context['user']
    if not user.is_authenticated:
        return ''
    content_type = ContentType.objects.get_for_model(obj)
    if LikeRecord.objects.filter(content_type= content_type, object_id= obj.pk, user= user).exists():
        return 'active'
    else:
        return ''

@register.simple_tag
# 获取粗腰的具体的模型
def  get_content_type(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return content_type.model
