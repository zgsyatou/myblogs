# 导入统计的方法
from django.db.models import Count
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from ReadCount.tool import read_count_once_read
from django.shortcuts import get_object_or_404, render
from .models import Blog, BlogType
from comment.models import Comment
from comment.forms import CommentForm


# 设置每页展示的博客数量变量
blog_num_of_page = 10

def blog_list_with_public(request,blog_all_list):
    paginator = Paginator(blog_all_list, blog_num_of_page) # 获取所有blog，并进行10篇博客进行分页
    '''将获取的页码传递给page_num，默认为1，获取页面参数'''
    page_num = request.GET.get('page', 1)
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number # 获取当前页码
    # 获取当前页码的前后各两页
    current_page_range = list(range(max(current_page_num - 2, 1),current_page_num)) + \
    list(range(current_page_num, min(current_page_num + 2 , paginator.num_pages ) + 1 ))
    # 添加省略号标记
    if current_page_range[0] - 1 >= 2:
        current_page_range.insert(0, '...')
    if paginator.num_pages - current_page_range[-1] >= 2:
        current_page_range.append('...')
    # 添加首页与尾页
    if current_page_range[0] != 1:
        current_page_range.insert(0,1)
    if current_page_range[-1] != paginator.num_pages:
        current_page_range.append(paginator.num_pages)

    '''统计各分类博客的数量,此方法无法统计类型数量，提示无法解析字段blog_type'''
    '''blog_types = BlogType.objects.all()
    blog_type_list = []
    for blog_type in blog_types:
        blog_type.blog_count = BlogType.objects.filter(blog_type = blog_type).count()
        blog_type_list.append(blog_type)'''
        
    ''' 设置统计各个月份的博客数量 '''
    blog_dates = Blog.objects.dates('create_time', 'month', order= 'DESC')
    blog_date_dic = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(create_time__year=blog_date.year,
                                        create_time__month=blog_date.month).count()
        blog_date_dic[blog_date] = blog_count

    context = {}
    # 传入所需要的变量
    context['current_page_range'] = current_page_range
    context['bloglist'] = page_of_blogs.object_list
    context ['page_of_blogs'] = page_of_blogs
    # context['bloglist'] = Blog.objects.all() # 采用此方法获取全部的博客
    '''采用count()统计当前博客的数量'''
    context['blog_count'] = Blog.objects.all().count()
    '''获取所有的博客分类的数量，使用annotate的Count方法来获取'''
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    context['blog_dates'] = blog_date_dic
    # 返回字典
    return context

'''显示博客的列表'''
def blog_list(request):
    blog_all_list = Blog.objects.all()
    context = blog_list_with_public(request,blog_all_list)
    return render(request,'blog/blog_list.html',context)


'''分类处理的方法，点击对应的标签可跳转页面'''
def blog_with_type(request,blog_type_pk):
    # 从BlogType中获取blog_type的ID值，并且将其传送给blog_type_pk
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk) 
    # 将获取到的blog_type的ID值传递给blogtype
    # context['bloglist'] = Blog.objects.filter(blog_type=blog_type)
    # context['blog_types'] = BlogType.objects.all()
    blog_all_list = Blog.objects.filter(blog_type=blog_type)
    context = blog_list_with_public(request,blog_all_list)
    # 传入所需要的变量
    context['blog_type'] = blog_type
    return render(request, 'blog/blog_type.html',context)

# 设置按年和按月分类博客的方法
def blog_with_date(request, year, month):
    '''获取索要查询的年和月'''
    blog_all_list = Blog.objects.filter(create_time__year=year, create_time__month=month)
    context = blog_list_with_public(request,blog_all_list)
    context['blog_with_date'] = '%s年%s月' % (year, month)
    return render(request,  'blog/blog_date.html', context)

'''显示博客的内容'''
def blog_details(request, blog_pk):
    # 可能获取不到对应的博客，Blog传入的对象
    blog = get_object_or_404(Blog, pk=blog_pk)
    read_cookie_key = read_count_once_read(request, blog)
    # 获取博客的类型
    # blog_conntent_type = ContentType.objects.get_for_model(blog)
    # comment = Comment.objects.filter(content_type=blog_conntent_type, object_id= blog.pk, parent= None)
        
    context = {}
    # 获取前一页
    context['perversion_blog'] = Blog.objects.filter(create_time__gt=blog.create_time).last()
    # 获取后一页
    context['next_blog'] = Blog.objects.filter(create_time__lt=blog.create_time).first() 
    context['blogdetails'] = blog
    # context['comment'] = comment.order_by('-comment_time')
    # 获取评论的数目
    # context['comment_count'] = Comment.objects.filter(content_type=blog_conntent_type, object_id= blog.pk).count()
    # context['comment_form'] = CommentForm(initial={'content_type':blog_conntent_type,'object_id':blog_pk, 'reply_comment_id': 0})
    response = render(request,'blog/blog_details.html',context)  # 获取响应
    ''' 设置cookie的写的方法,返回的是一个字典，格式：（他有键（需要识别的字段）和值 ，
    设置时间：max_age（设置有效时间 秒），expries），若无设置时间参数，则默认关闭浏览器一次'''
    response.set_cookie(read_cookie_key,'true')  # 阅读标记
    return response
    