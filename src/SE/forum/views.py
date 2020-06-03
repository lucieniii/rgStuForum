from . import models
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
import markdown
from django.shortcuts import render, get_object_or_404
from .form import PostForm
from .models import Post, Tag
from comment.models import Comment
from login.models import User
# from django.contrib.auth.models import User
# from notifications.signals import notify


# Create your views here.
def base(request):
    return render(request, 'base/base.html')


# index-views
def index(request):
    return render(request, 'forum/index.html')


def forumBoard(request):
    return render(request, 'forum/ForumBoard.html')


def followUser(request):
    return render(request, 'forum/FollowUser.html')


def mention(request):
    return render(request, 'forum/Mention.html')


def followPost(request):
    return render(request, 'forum/FollowPost.html')


def post_create(request):
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        post_form = PostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_post = post_form.save(commit=False)
            # 指定数据库中 id=1 的用户为作者
            # 如果你进行过删除数据表的操作，可能会找不到id=1的用户
            # 此时请重新创建用户，并传入此用户的id
            new_post.author = User.objects.get(id=1)
            # 将新文章保存到数据库中
            new_post.save()
            # 完成后返回到文章列表
            return redirect("post_list")
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = PostForm()
        context = {'article_post_form': article_post_form}
        return render(request, 'base/post_create.html', locals())


def post_detail(request, id):
    post = Post.objects.get(id=id)
    comments = Comment.objects.filter(post=id)
    # 将markdown语法渲染成html样式
    post.content = markdown.markdown(post.content,
                                     extensions=[
                                         # 包含 缩写、表格等常用扩展
                                         'markdown.extensions.extra',
                                         # 语法高亮扩展
                                         'markdown.extensions.codehilite',
                                     ])
    return render(request, 'base/post_detail.html', locals())


# 文章详情页面的视图函数
def post_list(request):
    # post = get_object_or_404(Post, pk=id)
    # post.body = markdown.markdown(post.body,
    #                               extensions=[
    #                                   'markdown.extensions.extra',
    #                                   'markdown.extensions.codehilite',
    #                                   'markdown.extensions.toc',
    #                               ])
    # # 记得在顶部导入 CommentForm
    # form = CommentForm()
    # # 获取这篇 post 下的全部评论
    # comment_list = post.comment_set.all()
    #
    # # 将文章、表单、以及文章下的评论列表作为模板变量传给 detail.html 模板，以便渲染相应数据。
    # context = {'post': post,
    #            'form': form,
    #            'comment_list': comment_list
    #            }
    # return render(request, 'post_list.html', context=context)
    posts = Post.objects.all()
    return render(request, 'base/post_list.html', locals())


def post_rank(request):
    # 文档内容
    # 获取显示的文章id
    nid = request.GET.get('nid')
    # 获取文章
    post_data = models.Post.objects.filter(id=nid).first()
    # 获取到的文章调用increase_views方法
    models.Post.increase_views(post_data)
    # 根据自增的views字段进行排序，并获取最高的5条数据
    hot_doc = models.Post.objects.order_by("-views")[0:5]
    return render(request, "?????.html", {"post_data": post_data, 'hot_doc': hot_doc})  # TODO
