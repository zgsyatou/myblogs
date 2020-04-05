from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from collected.models import CollectRecord

# 创建关联类型
class OAuthRelationship(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    openid = models.CharField(max_length=128)
    OAUTH_TYPE_CHIOSE = (
            (0, 'QQ'),
            (1, 'WeChat'),
            (0, 'Sina'),
            (0, 'GitHub'),
        )
    oauth_type = models.IntegerField(default=0,choices=OAUTH_TYPE_CHIOSE)
    
    def __str___(self):
        return '<OAuthRelationship: %s>' % self.user.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    nickname = models.CharField(max_length= 16, verbose_name= '昵称')
    favs = GenericRelation(CollectRecord)

    def __str__(self):
        return '<Profile %s for %s>' % (self.nickname, self.user.username)
# 动态绑定nickname
def get_nickname(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nickname
    else: 
        return ''

# 判断用户是否有昵称
def has_nickname(self):
    return Profile.objects.filter(user=self).exists()

# 判断用户的用户名或者昵称
def get_nickname_or_username(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nickname
    else: 
        return '[%s]' %  self.username

User.get_nickname = get_nickname
User.has_nickname = has_nickname
User.get_nickname_or_username = get_nickname_or_username