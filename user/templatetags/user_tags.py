from django import template
# 将GEt参数修改为字典所需要的样子
from urllib.parse import urlencode
from django.conf import settings

register = template.Library()

@register.simple_tag
# 获取前端页面QQ登录所需要的参数
def get_qq_url():
    parse = {
        'response_type' : 'code',
        'client_id' : settings.QQ_APP_ID,
        'redirect_uri' : settings.QQ_RESVER,
        'state' : settings.QQ_STATE,
    }
    return 'https://graph.qq.com/oauth2.0/authorize' + urlencode(parse)
