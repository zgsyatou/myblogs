import datetime
from django.contrib.contenttypes.models import ContentType
from .models import ReadNum, ReadDetail
from django.db.models import Sum
from django.utils import timezone
from blog.models import Blog


def read_count_once_read(request, obj):
    ct =ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (ct.model, obj.pk)
    '''设置统计博客于都数量的方法'''
    if not request.COOKIES.get(key):
        if ReadNum.objects.filter(content_type=ct, object_id= obj.pk).count():  # 判断blog是否阅读数为0
            readnum = ReadNum.objects.get(content_type=ct, object_id= obj.pk)
        else:
            # 不存在记录,则进行对象的实例化
            readnum = ReadNum(content_type=ct, object_id= obj.pk)
        # 计数加1
        readnum.read_num += 1
        readnum.save()
        # 统计每天的比克阅读数量

        date = timezone.now().date()  # 获取当前时间X月X日
        #  使用django自带的get_or_create方法来实现返回对象，空则创建
        readDetail, create = ReadDetail.objects.get_or_create(content_type=ct, object_id= obj.pk, date=date)
        readDetail.read_num += 1
        readDetail.save()  
    return key

# 获取前七天每天的博客阅读量
def get_sever_day_read(content_type):
    today = timezone.now().date()
    dates = []
    read_nums = []  
    for i in range(7, 0, -1):     # -1表示倒序排序
        date = today - datetime.timedelta(days= i)
        dates.append(date.strftime('%m/%d'))
        read_detail = ReadDetail.objects.filter(content_type= content_type, date= date)
        result = read_detail.aggregate(read_num_sum= Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)
    return dates, read_nums

# 获取某一天当天的博客阅读数量，并且将倒续排列
def get_one_day_hot(content_type):
    today = timezone.now().date()
    read_detail = ReadDetail.objects.filter(content_type= content_type, date= today).order_by('-read_num')
    return read_detail[:7]  # 使用切片器取前7条博客

# 获取前一天博客阅读数量
def get_yesterday_hot(content_type):
    today = timezone.now().date()
    yesterday =  today - datetime.timedelta(days= 1)
    read_detail = ReadDetail.objects.filter(content_type= content_type, date= yesterday).order_by('-read_num')
    return read_detail[:7]

# 获取前七天的博客阅读数量
def get_berfor_seven_day_hot():
    today = timezone.now().date()
    date =  today - datetime.timedelta(days= 7)
    read_detail = Blog.objects \
                            .filter(read_details__date__lt= today,read_details__date__gte= date) \
                            .values('title', 'id') \
                            .annotate(read_num_sum=Sum('read_details__read_num')) \
                            .order_by('-read_num_sum')
    return read_detail[:7]
