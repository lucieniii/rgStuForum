from . import models
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
import markdown
from django.shortcuts import render, get_object_or_404
from .form import PostForm, CommentForm
from .models import Post, Section, Comment
from login.models import User
from login.views import get_login_status


# from django.contrib.auth.models import User
# from notifications.signals import notify


# Create your views here.
def base(request):
    return render(request, 'base/base.html')


# index-views old
def index_old(request):
    is_login = get_login_status(request)
    return render(request, 'forum/index.html', locals())


def index(request):
    is_login = get_login_status(request)
    user_id = request.session.get('user_id', None)
    top_posts = Post.objects.filter(is_top=True)
    hot_posts = Post.objects.filter(is_top=False).order_by("-views")[0:5]
    if is_login:
        user = User.objects.get(id=user_id)
    # 限定显示30个字符
    for i in top_posts:
        if len(i.content) > 30:
            i.content = i.content[0:30] + "..."

    return render(request, "forum/index.html", locals())


# 返回热帖hot_posts,以及普通帖子normal_posts
def forumBoard(request, id):
    if id == 1:  # 讨论区
        hot_posts = Post.objects.filter(section=1).order_by("-views")[0:3]
    elif id == 2:  # 课程推荐
        hot_posts = Post.objects.filter(section=2).order_by("-views")[0:3]
    elif id == 3:  # 刷题
        hot_posts = Post.objects.filter(section=3).order_by("-views")[0:3]
    elif id == 4:  # 校园周边
        hot_posts = Post.objects.filter(section=4).order_by("-views")[0:3]
    elif id == 5:  # 资源共享
        hot_posts = Post.objects.filter(section=5).order_by("-views")[0:3]
    else:
        return HttpResponse("不存在这个板块")
    is_login = get_login_status(request)
    user_id = request.session.get('user_id', None)
    normal_posts = Post.objects.order_by("create_time")
    if is_login:
        user = User.objects.get(id=user_id)
    return render(request, 'forum/ForumBoard.html', locals())


def followUser(request):
    return render(request, 'forum/FollowUser.html')


def mention(request):
    return render(request, 'forum/Mention.html')


def followPost(request):
    return render(request, 'forum/FollowPost.html')


def PostContent(request, id):
    is_login = get_login_status(request)
    user_id = request.session.get('user_id', None)
    comment_form = CommentForm(request.POST)
    if not is_login:
        return redirect("/index/", locals())
    else:
        user = User.objects.get(id=user_id)
    if request.method == 'GET':
        post = Post.objects.get(id=id)
        comments = Comment.objects.filter(post=id)
        # 将markdown语法渲染成html样式
        comments_lv1 = []
        for comment in comments:
            if comment.reply_to is None:
                comments_lv1.append([comment, []])

        for comment_list in comments_lv1:
            for comment in comments:
                if comment.reply_to_comment_id == comment_list[0].id:
                    comment_list[1].append(comment)
        # print(comments_lv1)
        return render(request, 'forum/PostContent.html', locals())
    elif request.method == 'POST':
        post = Post.objects.get(id=id)
        # 当调用 form.is_valid() 方法时，Django 自动帮我们检查表单的数据是否符合格式要求。
        if comment_form.is_valid():
            # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库。
            new_comment = comment_form.save(commit=False)
            # 将评论和被评论的文章关联起来。
            new_comment.post = post
            new_comment.user = user
            # 最终将评论数据保存进数据库，调用模型实例的 save 方法
            new_comment.save()
            return redirect(post)
        else:
            return HttpResponse("表单内容有误，请重新填写。")


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
    if request.method == 'GET':
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


# 拉黑
def black(request):
    pass
