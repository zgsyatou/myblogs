from django.shortcuts import render, redirect, get_object_or_404
from notifications.models import Notification
from django.urls import reverse


# 站内消息通知
def my_notifications(request):
    context = {}
    return render(request, 'my_notifications/my_message.html', context)

# 定义处理一条未读消息的方法
def my_notification(request, my_notification_pk):
    my_notification = get_object_or_404(Notification, pk=my_notification_pk)
    my_notification.unread = False
    my_notification.save()
    return redirect(my_notification.data['url'])

# 定义一键删除已读消息
def delete_my_readed_notifications(request):
    notifications = request.user.notifications.read()
    notifications.delete()
    return redirect(reverse('my_notifications'))
