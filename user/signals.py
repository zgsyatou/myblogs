from django.db.models.signals import post_save
from notifications.signals import notify
from django.dispatch import receiver
from django.urls import reverse
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
# 处理评论的信号接收器
def send_notification(sender, instance, **kwargs):
    # 发送站内消息
    if kwargs['created'] == True:
      verb = '注册成功，随意浏览吧！'
      url = reverse('user_info')
      notify.send(instance, recipient=instance, verb=verb, action_object=instance, url=url)
