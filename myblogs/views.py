from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect, get_object_or_404
from django.core.cache import cache
from django.db.models import Q 
from django.core.paginator import Paginator
from ReadCount.tool  import get_sever_day_read, get_one_day_hot, get_yesterday_hot, get_berfor_seven_day_hot
from notifications.models import Notification
from blog.models import Blog

def index(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_sever_day_read(blog_content_type)

# 获取七天的博客访问数据的缓存
    seven_berfor_cache = cache.get('seven_berfor_cache')
    if seven_berfor_cache is None:
        seven_berfor_cache = get_berfor_seven_day_hot()
        cache.set('seven_berfor_cache', seven_berfor_cache, 3600)
    else:
        print('use cache')

    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['one_day_hot'] = get_one_day_hot(blog_content_type)
    context['yesterday_hot'] = get_yesterday_hot(blog_content_type)
    context['seven_day_hot'] = seven_berfor_cache
    return render(request, 'index.html', context)

# 站内消息通知
def my_notifications(request):
    context = {}
    return render(request, 'my_message.html', context)

# 定义处理一度消息与未读消息的方法
def my_notification(request, my_notification_pk):
    my_notification = get_object_or_404(Notification, pk=my_notification_pk)
    my_notification.unread = False
    my_notification.save()
    '''import pdb
                    pdb.set_trace()'''
    return redirect(my_notification.data['url'])

# 搜索
def search(request):
    search_words = request.GET.get('word', '').strip()
    # 分词 一中间的空格划分
    condition = None
    for word in search_words.split(' '):
        if condition is None:
            condition = Q(title__icontains=word)
        else:
            condition = condition | Q(title__icontains=word)
    search_key = []
    if condition is not None:
       search_key = Blog.objects.filter(condition)

    # 分页
    paginator = Paginator(search_key, 15) # 获取所有blog，并进行10篇博客进行分页
    '''将获取的页码传递给page_num，默认为1，获取页面参数'''
    page_num = request.GET.get('page', 1)
    page_of_blogs = paginator.get_page(page_num)

    context = {}
    context['search_words'] = search_words
    context['search_key_count'] = search_key.count()
    context['page_of_blogs'] = page_of_blogs
    return render(request, 'search.html', context)