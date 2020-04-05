from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, OAuthRelationship

@admin.register(OAuthRelationship)
class OAuthRelationshipAdmin(admin.ModelAdmin):
    list_display = ('user', 'openid', 'oauth_type')

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )
    list_display = ('username', 'nickname', 'email', 'is_staff', 'is_active', 'is_superuser')
    
    def nickname(self, obj):
        return obj.profile.nickname
    nickname.short_description = '昵称'

# 注销用户
admin.site.unregister(User)
# 重新注册用户
admin.site.register(User, UserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname')