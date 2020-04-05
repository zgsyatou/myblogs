from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType 
from django.http import JsonResponse
from django.urls import reverse
from notifications.signals import notify
from django.core.mail import send_mail
from .models import Comment
from .forms import CommentForm

def manage_comment(request):
    referer = request.META.get('HTTP_REFERER', reverse('index'))
    comment_form = CommentForm(request.POST, user=request.user)
    data = {}

    if comment_form.is_valid():
        #  检查通过，保存数据
        comment = Comment()
        comment.comment_user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']

        # 判断是否为评论而不是回复
        parent = comment_form.cleaned_data['parent']
        if not parent is None:
            comment.top = parent.top if not parent.top is None else parent 
            comment.parent = parent
            comment.reply_to = parent.comment_user
        comment.save()   # 当触发save之后，发送消息到singals中精选chuli

        # 返回数据为Json
        data['status'] = 'SUCCESS'
        data['username'] = comment.comment_user.get_nickname_or_username()
        data['comment_time'] = comment.comment_time.timestamp()
        data['text'] = comment.text
        data['content_type'] = ContentType.objects.get_for_model(comment).model

        if not parent is None:
            data['reply_to'] = comment.reply_to.get_nickname_or_username()
        else:
            data['reply_to'] = ''
        data['pk'] = comment.pk
        data['top_pk'] = comment.top.pk if not comment.top is None else ''
                                
    else:
        #return render(request, 'error.html', { 'message': '评论对象不存在！', 'redirect_to':referer })
        data['status'] = 'ERROR'
        data['message'] = list(comment_form.errors.values())[0][0]
    return JsonResponse(data) 
