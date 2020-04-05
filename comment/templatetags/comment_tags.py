from django import template
from django.contrib.contenttypes.models import ContentType
from ..models  import Comment
from ..forms  import CommentForm

register = template.Library()

@register.simple_tag
#获取评论数量
def get_comment_num(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(content_type=content_type, object_id= obj.pk).count()

@register.simple_tag
# 评论表单
def get_comment_from(obj):
    content_type = ContentType.objects.get_for_model(obj)
    form = CommentForm(initial={'content_type':content_type,
                         'object_id':obj.pk, 'reply_comment_id': 0})
    return form

@register.simple_tag
 # 获取评论列表
def get_comments_list(obj):
    content_type = ContentType.objects.get_for_model(obj)
    comment = Comment.objects.filter(content_type=content_type,object_id= obj.pk, parent= None)
    return comment.order_by('-comment_time')
 
        