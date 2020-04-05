from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist
from .models import CollectRecord, CollectCount

# 定义返回的json数据
def SuccessResponse(collect_num):
    data = {}
    data['status'] = "SUCCESS"
    data['collect_num'] = collect_num
    return JsonResponse(data)

def ErrorResponse(code, message):
    data = {}
    data['status'] = "ERROR"
    data['code'] = code       # 返回错误标记
    data['message'] = message
    return JsonResponse(data)

# 收藏
def collect_change(request):
    # 获取前端页面传回的数据
    user = request.user
    if not user.is_authenticated:
        return ErrorResponse(406, '您未登录')
    content_type = request.GET.get('content_type')
    object_id = request.GET.get('object_id')
    print(object_id)

    try:
        content_type = ContentType.objects.get(model= content_type)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return ErrorResponse(407,'未获取到对象')

    # 处理收藏数据
    if request.GET.get('is_collect') == 'true':
        # 要收藏
        collect_record, created = CollectRecord.objects.get_or_create(content_type=content_type, 
                                                                      object_id=object_id, user= user)
        if created:
            # 未收藏，要收藏
            collect_count, created = CollectCount.objects.get_or_create(content_type=content_type, 
                                                                        object_id=object_id)
            collect_count.collect_num += 1
            collect_count.save()
            return SuccessResponse(collect_count.collect_num)
        else:
            # 已收藏，不能重复收藏
            return ErrorResponse(408,'不能多次收藏同一个影片')
    else:
        # 取消收藏
        if CollectRecord.objects.filter(content_type=content_type, object_id=object_id, 
                                        user=user).exists():
            # 已经收藏，取消收藏
            collect_record = CollectRecord.objects.get(content_type=content_type, 
                                                       object_id=object_id, user=user)
            collect_record.delete()
            # 收藏数量减一
            collect_count, created = CollectCount.objects.get_or_create(content_type=content_type, 
                                                                              object_id=object_id)
            if not created:
                collect_count.collect_num -= 1
                collect_count.save()
                return SuccessResponse(collect_count.collect_num)
            else:
                return ErrorResponse(409,'取消收藏错误')
        else:
            # 没有点赞，不能取消
            return ErrorResponse(410,'没有收藏，不能取消')

# 将收藏的数据返回到收藏页面
def show_collect_info(request):

    if request.method == 'POST':
        user = request.user
        favs = user.favs.filter()
        favs = user.favs

        return render(request, 'collected/collected.html', favs)
