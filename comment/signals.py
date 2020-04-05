from django.db.models.signals import post_save
from notifications.signals import notify
from django.utils.html import strip_tags
from django.dispatch import receiver
from django.conf import settings
import threading
from .models import Comment

@receiver(post_save, sender=Comment)
# 处理评论的信号接收器
def send_notification(sender, instance, **kwargs):
    # 发送站内消息
    if instance.reply_to is None:
        # 评论
        recipient = instance.content_object.get_user()
        if instance.content_type.model == 'blog':
            blog = instance.content_object
            verb = '{0}评论了你的《{1}》'.format(instance.comment_user.get_nickname_or_username(), 
                                             blog.title)
        else:
            raise Exception('unknow coment object type')
    else:
        # 回复
        recipient = instance.reply_to
        verb = '{0}回复了你的评论"{1}"'.format(
               instance.comment_user.get_nickname_or_username(),
               strip_tags(instance.parent.text)
               )
    url = instance.content_object.get_url() + '#comment_' + str(instance.pk)
    notify.send(instance.comment_user, recipient=recipient, verb=verb, action_object=instance, url=url)

# 发送邮件内容格式
# 多线程处理发送邮件的方法
class SendEmial(threading.Thread):
    def __init__(self, subject, text, email, fail_silently=False):
        self.subject = subject
        self.text = text
        self.email = email
        self.fail_silently = fail_silently
        threading.Thread.__init__(self)

    def run(self):
        send_mail(self.subject, 
                  '', 
                  settings.EMAIL_HOST_USER, 
                 [self.email], 
                 fail_silently=self.fail_silently,
                 html_message=self.text
                 )
