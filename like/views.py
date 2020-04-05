from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist
from .models import LikeCount, LikeRecord

# 定义返回的json数据
def SuccessResponse(like_num):
    data = {}
    data['status'] = "SUCCESS"
    data['like_num'] = like_num
    return JsonResponse(data)

def ErrorResponse(code, message):
    data = {}
    data['status'] = "ERROR"
    data['code'] = code       # 返回错误标记
    data['message'] = message
    return JsonResponse(data)

def like_change(request):
    # 获取前端页面传回的数据
    user = request.user
    if not user.is_authenticated:
        return ErrorResponse(400, '您未登录')

    content_type = request.GET.get('content_type')
    object_id = int(request.GET.get('object_id'))

    try:
        content_type = ContentType.objects.get(model= content_type)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return ErrorResponse(401,'未获取到对象')

    # 处理数据
    if request.GET.get('is_like') == 'true':
        # 用户要点赞
        # get_or_created传递两个参数，如果已经创建则返回到like_record，如果没有创建，则进行创建
        like_record, created = LikeRecord.objects.get_or_create(content_type=content_type, 
                                                                object_id=object_id, user= user)
        if created:
            # 未点赞，需要进行点赞 
            like_count, created = LikeCount.objects.get_or_create(content_type= content_type, 
                                                                            object_id= object_id)
            like_count.like_num += 1
            like_count.save()
            return SuccessResponse(like_count.like_num)
        else:
            # 已点赞，不需要进行点赞
            return ErrorResponse(402, '已点赞，不能重复点赞')
    else:
        # 用户取消点赞
        # 判断用户对象是否存在
        if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user= user).exists():
           # 有过点赞，取消点赞
           like_record = LikeRecord.objects.get(content_type=content_type, object_id=object_id, user= user)
           like_record.delete()
           # 点赞总数减1
           like_count, created = LikeCount.objects.get_or_create(content_type= content_type, 
                                                                        object_id= object_id)
           if not created:
               like_count.like_num -= 1
               like_count.save()
               return SuccessResponse(like_count.like_num)
           else:
                # 为点赞，不能减1
                return ErrorResponse(404, '取消点赞错误')
        else:
            # 未点赞，不能取消
            return ErrorResponse(403, '未点赞，不能取消点赞')
