import markdown
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, HttpResponse, reverse
from django.shortcuts import render
from django.template.defaultfilters import striptags

from login.models import User
from login.views import get_login_status
# from . import models
from .form import PostForm, CommentForm, UpdatePostForm
from .models import Post, Comment, UpAndDown
from space.models import *

UP_AND_DOWN_EXP = 40
CREATE_POST_EXP = 70
COMMENT_EXP = 20
MUST_READ_POST_ID = 1


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
    if is_login:
        userid = request.session.get('user_id', None)
        user = User.objects.get(id=userid)
    # 限定显示30个字符
    top_posts = Post.objects.filter(is_top=True)
    hot_posts = Post.objects.filter(is_top=False).order_by("-views")[0:5]

    for i in hot_posts:
        i.content = striptags(i.content)
        # print(i.content)
        if len(i.content) > 30:
            i.content = i.content[0:30] + "..."

    for i in hot_posts:
        i.content = striptags(i.content)
        # print(i.content)
        if len(i.content) > 100:
            i.content = i.content[0:100] + "..."

    return render(request, "forum/index.html", locals())


# 返回热帖hot_posts,以及普通帖子normal_posts
def forumBoard(request, id):
    if id not in (1, 2, 3, 4, 5):
        return HttpResponse("不存在这个板块")
    hot_posts = Post.objects.filter(section=str(id)).order_by("-views")[0:3]
    normal_posts = Post.objects.filter(section=str(id)).order_by("-last_edit")

    is_login = get_login_status(request)

    if is_login:
        userid = request.session.get('user_id', None)
        user = User.objects.get(id=userid)

    for i in hot_posts:
        i.content = striptags(i.content)
        # print(i.content)
        if len(i.content) > 30:
            i.content = i.content[0:30] + "..."

    for i in normal_posts:
        i.content = striptags(i.content)
        # print(i.content)
        if len(i.content) > 100:
            i.content = i.content[0:100] + "..."
    return render(request, 'forum/ForumBoard.html', locals())


# def followUser(request):
#    is_login = get_login_status(request)
#    if is_login:
#        userid = request.session.get('user_id', None)
#        user = User.objects.get(id=userid)
#        # follow_list =
#    else:
#        return redirect('/index/', locals())
#    return render(request, 'forum/FollowUser.html', locals())


def mention_old(request):
    return render(request, 'forum/Mention.html')


def mention(request):
    is_login = get_login_status(request)
    if is_login:
        userid = request.session.get('user_id', None)
        user = User.objects.get(id=userid)
        posts = Post.objects.filter(author=userid)
        to_post = Comment.objects.filter(post__in=posts, reply_to_comment__isnull=True).order_by("-created")
        my_comment = Comment.objects.filter(user=user)
        to_comment = Comment.objects.filter(Q(reply_to_comment__in=my_comment, reply_to__isnull=True) | Q(reply_to=user)).order_by("-created")
        for comment in to_post:
            comment.content = striptags(comment.content)
            if len(comment.content) > 30:
                comment.content = comment.content[0:30] + '...'
        for comment in to_comment:
            comment.content = striptags(comment.content)
            if len(comment.content) > 30:
                comment.content = comment.content[0:30] + '...'
        # Comment表里没有post的title属性，故在本地进行查询
        # 发现可以直接使用comment.user访问User类，那就不需要下面的东西了
        '''
        comments_tmp = Comment.objects.filter(user=userid)
        comments = []
    
        for i in comments_tmp:
            post = Post.objects.get(author=i.user, id=i.post)
            title = post.title
            author = user.name
            tag = post.tag
            dic = {'title': title, 'author': author, 'tag': tag}
            comments.append(dic)
        '''
        # 限定显示100个字符
        for i in posts:
            if len(i.content) > 100:
                i.content = i.content[0:100] + "..."
        return render(request, "forum/Mention.html", locals())
    else:
        return redirect('/index/', locals())


def followPost_old(request):
    return render(request, 'forum/FollowPost.html')


# def followPost(request):
#     is_login = get_login_status(request)
#     if is_login:
#         userid = request.session.get('user_id', None)
#         user = User.objects.get(id=userid)
#     else:
#         return redirect('/index/', locals())
#     return render(request, 'forum/FollowPost.html', locals())


def PostContent(request, s):
    is_login = get_login_status(request)
    if is_login:
        userid = request.session.get('user_id', None)
        user = User.objects.get(id=userid)
    else:
        return redirect('/index/', locals())
    comment_form = CommentForm(request.POST)
    ls = s.split("&")

    if request.method == 'GET':
        if len(ls) > 1:
            return redirect("/index/", locals())
        post = Post.objects.get(id=int(ls[0]))

        if post.id == MUST_READ_POST_ID and not user.is_read:
            user.is_read = True
            user.save()
        if not user.is_read and not user.is_admin:
            messages.success(request, "您没有看新手上路帖！")
            return redirect('/index/', locals())

        if int(post.level_restriction) > user.level and not user.is_admin:
            messages.success(request, "您等级不够，无法查看此帖！")
            return redirect("/index/", locals())
        comments = Comment.objects.filter(post=int(ls[0]))
        post.views += 1
        post.save()
        try:
            UpAndDown.objects.get(user=user, post=post)
            is_thumbed_post = True
        except:
            is_thumbed_post = False
        # 将markdown语法渲染成html样式
        comments_lv1 = []
        for comment in comments:
            if not comment.reply_to_comment_id:
                # print(comment.reply_to_id)
                try:
                    UpAndDown.objects.get(user=user, comment=comment)
                    comments_lv1.append([comment, [], True])
                except:
                    comments_lv1.append([comment, [], False])

        for comment_list in comments_lv1:
            for comment in comments:
                if comment.reply_to_comment_id == comment_list[0].id:
                    try:
                        UpAndDown.objects.get(user=user, comment=comment)
                        comment_list[1].append([comment, True])
                    except:
                        comment_list[1].append([comment, False])
        # print(comments_lv1)
        # print(1)
        is_owner = (str(userid) == str(post.author.id))
        try:
            FavoritePost.objects.get(UserID=user, PostID=post)
            print(1)
            is_favourite = True
        except:
            is_favourite = False
        return render(request, 'forum/PostContent.html', locals())
    elif request.method == 'POST':
        post = Post.objects.get(id=int(ls[0]))
        if user.is_ban:
            messages.success(request, "您已被禁言，暂时不能回复")
            return redirect(reverse('PostContent', kwargs={"s": str(post.id)}), locals())
        # 当调用 form.is_valid() 方法时，Django 自动帮我们检查表单的数据是否符合格式要求。
        if comment_form.is_valid():
            # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库。
            new_comment = comment_form.save(commit=False)
            # 将评论和被评论的文章关联起来。
            new_comment.post = post
            new_comment.user = user
            if ls[1] != '0':
                new_comment.reply_to_id = int(ls[1])
            if ls[2] != '0':
                new_comment.reply_to_comment_id = int(ls[2])
            # 最终将评论数据保存进数据库，调用模型实例的 save 方法
            user.exp += COMMENT_EXP  # 发评论加经验
            user.save()
            new_comment.save()
            post.last_edit = new_comment.created
            post.save()
            return redirect(reverse('PostContent', kwargs={"s": str(post.id)}), locals())
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # print(1)


def post_update(request, id):

    is_login = get_login_status(request)
    if is_login:
        userid = request.session.get('user_id', None)
        user = User.objects.get(id=userid)
    else:
        return redirect('/index/', locals())
    # 获取需要修改的具体文章对象
    if user.is_ban:
        messages.success(request, "您已经被禁言，暂时不能修改帖子")
        # return redirect(reverse('space', args=str(user.id)), locals())
        return redirect(reverse('PostContent', kwargs={"id": str(user.id)}), locals())
    post = Post.objects.get(id=id)
    # 判断用户是否为 POST 提交表单数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        update_form = UpdatePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if update_form.is_valid():
            # 保存新写入的 title、body 数据并保存
            post.title = request.POST['title']
            post.content = request.POST['content']
            post.section = request.POST['section']
            post.save()
            return redirect(reverse('PostContent', kwargs={"s": str(post.id)}), locals())
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")

    # 如果用户 GET 请求获取数据
    else:
        # 创建表单类实例
        post_form = PostForm(initial={'title': post.title, 'content': post.content, 'section': post.section})
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        context = {'post': post, 'post_form': post_form}
        # 将响应返回到模板中
        return render(request, 'base/post_update.html', locals())


def post_create(request):
    is_login = get_login_status(request)
    if is_login:
        userid = request.session.get('user_id', None)
        user = User.objects.get(id=userid)
    else:
        return redirect('/index/', locals())
    if user.is_ban:
        messages.success(request, "您已经被禁言，暂时不能发帖")
        return redirect('/index/', locals())
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        post_form = PostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_post = Post()
            new_post.title = post_form.cleaned_data.get("title", None)
            new_post.content = post_form.cleaned_data.get("content", None)
            new_post.section = post_form.cleaned_data.get("section", None)
            new_post.level_restriction = post_form.cleaned_data.get("level_restriction", None)
            # new_post = post_form.save(commit=False)
            # 指定数据库中 id=1 的用户为作者
            # 如果你进行过删除数据表的操作，可能会找不到id=1的用户
            # 此时请重新创建用户，并传入此用户的id
            new_post.author = user
            # 将新文章保存到数据库中
            user.exp += CREATE_POST_EXP  # 发文章加经验
            user.save()
            new_post.save()
            # 完成后返回到文章列表
            return redirect('/index/', locals())
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
    is_login = get_login_status(request)
    userid = request.session.get('user_id', None)
    user = User.objects.get(id=userid)
    search = request.GET.get('search')
    searchPost = request.GET.get('searchPost')
    # 用户搜索逻辑
    print(search, searchPost)
    if search:
        if searchPost == 'true':
            # 用 Q对象 进行联合搜索
            post_list = Post.objects.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search)
            ).order_by('-views')
        else:
            # 将 search 参数重置为空
            user_list = User.objects.filter(
                Q(name__icontains=search)
            )
    else:
        print('hh')
        search = ''
        if searchPost:
            post_list = Post.objects.all().order_by('-views')
        else:
            user_list = User.objects.all()

    if searchPost == 'true':
        # print('in search post')
        context = {'posts': post_list, 'search': search, 'user': user, 'is_login': True, 'userid': userid}
        return render(request, 'base/PostList.html', context)
    else:
        # print('in search user')
        # print(user_list)
        context = {'users': user_list, 'search': search, 'user': user, 'is_login': True, 'userid': userid}
        return render(request, 'base/UserList.html', context)


def post_safe_delete(request, id):
    id = int(id)
    is_login = get_login_status(request)
    if not is_login:
        return redirect('/index/', locals())
    userid = request.session.get('user_id', None)
    user = User.objects.get(id=userid)
    post = Post.objects.get(id=id)
    post.delete()
    context = {'is_login': is_login, 'user': user}
    return redirect(reverse('space', kwargs={"id": str(userid)}), context)


def comment_safe_delete(request, id):
    id = int(id)
    is_login = get_login_status(request)
    if not is_login:
        return redirect('/index/', locals())
    userid = request.session.get('user_id', None)
    user = User.objects.get(id=userid)
    comment = Comment.objects.get(id=id)
    post_id = comment.post.id
    comment.delete()
    return redirect(reverse('PostContent', kwargs={"s": str(post_id)}), locals())


def post_rank(request):
    # 文档内容
    # 获取显示的文章id
    nid = request.GET.get('nid')
    # 获取文章
    post_data = Post.objects.filter(id=nid).first()
    # 获取到的文章调用increase_views方法
    Post.increase_views(post_data)
    # 根据自增的views字段进行排序，并获取最高的5条数据
    hot_doc = Post.objects.order_by("-views")[0:5]
    return render(request, "?????.html", {"post_data": post_data, 'hot_doc': hot_doc})  # TODO


# 拉黑
def black(request):
    pass


def thumb(request):
    userid = request.session.get('user_id', None)
    user = User.objects.get(id=userid)
    data = {
        "totalThumb": 0,
        "isThumb": False
    }

    type = request.GET.get("type", None)
    id = request.GET.get("id", None)

    if type == '0':  # 文章
        post = Post.objects.get(id=id)
        try:
            up_and_down = UpAndDown.objects.get(user=user, post=post)  # 已经点过赞了, 将要被取消点赞
            up_and_down.delete()
            post.absoluteUps -= 1
            post.author.exp -= UP_AND_DOWN_EXP  # 减少经验值
            post.author.save()
            post.save()
            data["isThumb"] = True
            data["totalThumb"] = post.absoluteUps
        except UpAndDown.DoesNotExist:
            UpAndDown.objects.create(user=user, post=post)  # 没有点过赞, 将要被点赞
            post.absoluteUps += 1
            post.author.exp += UP_AND_DOWN_EXP
            post.author.save()
            post.save()
            data["totalThumb"] = post.absoluteUps
    else:  # 评论
        comment = Comment.objects.get(id=id)
        try:
            up_and_down = UpAndDown.objects.get(user=user, comment=comment)  # 已经点过赞了, 将要被取消点赞
            up_and_down.delete()
            comment.absoluteUps -= 1
            comment.user.exp -= UP_AND_DOWN_EXP
            comment.user.save()
            comment.save()
            data["isThumb"] = True
            data["totalThumb"] = comment.absoluteUps
        except UpAndDown.DoesNotExist:
            UpAndDown.objects.create(user=user, comment=comment)  # 没有点过赞
            comment.absoluteUps += 1
            comment.user.exp -= UP_AND_DOWN_EXP
            comment.user.save()
            comment.save()
            data["totalThumb"] = comment.absoluteUps
    return JsonResponse(data)


def comment_list(request):
    is_login = get_login_status(request)
    userid = request.session.get('user_id', None)
    user = User.objects.get(id=userid)
    my_posts = Post.objects.filter(author=user)
    my_comments = Comment.objects.filter(user=user)

    my_posts_comments = []
    for post in my_posts:
        comments = Comment.objects.filter(post=post)
        for comment in comments:
            comment.content = striptags(comment.content)
            if len(comment.content) > 30:
                comment.content = comment.content[0:30] + "..."
        my_posts_comments.extend(comments)

    my_comments_comments = []
    for my_comment in my_comments:
        comments = Comment.objects.filter(reply_to_comment=my_comment)
        for comment in comments:
            comment.content = striptags(comment.content)
            if len(comment.content) > 30:
                comment.content = comment.content[0:30] + "..."
        my_comments_comments.extend(comments)

    context = {"posts_comments": my_posts_comments, "comments_comments": my_comments_comments, "userid": userid,
               "user": user, "is_login": is_login}
    return render(request, 'forum/Mention.html', context)


def followUser(request):
    is_login = get_login_status(request)
    if not is_login:
        return redirect('/index/', locals())

    userid = request.session.get('user_id', None)
    user = User.objects.get(id=userid)
    follows = Follow.objects.filter(FollowerID=userid)
    post_list = []
    for follower in follows:
        posts = Post.objects.filter(author=follower.FollowedID)
        post_list.extend(posts)
    for post in post_list:
        post.content = striptags(post.content)
        if len(post.content) > 100:
            post.content = post.content[0:100] + "..."
    return render(request, 'forum/FollowUser.html', locals())


def followPost(request):
    is_login = get_login_status(request)
    if not is_login:
        return redirect('/index/', locals())
    userid = request.session.get('user_id', None)
    user = User.objects.get(id=userid)
    favorites = FavoritePost.objects.filter(UserID=userid)
    post_list = []

    for f in favorites:
        posts = Post.objects.filter(id=f.PostID.id)
        post_list.extend(posts)
    for post in post_list:
        post.content = striptags(post.content)
        if len(post.content) > 100:
            post.content = post.content[0:100] + "..."
    return render(request, 'forum/FollowPost.html', locals())


def all_lists(request):
    is_login = get_login_status(request)
    if not is_login:
        return redirect('index', locals())
    userid = request.session.get('user_id', None)
    user = User.objects.get(id=userid)
    if not user.is_admin:
        return redirect('index', locals())
    post_list = Post.objects.all()
    user_list = User.objects.all()

    context = {"posts": post_list, "users": user_list, "userid": userid,
               "user": user, "is_login": is_login}
    return render(request, 'forum/AllList.html', context)


def make_post_top(request):
    is_login = get_login_status(request)
    if not is_login:
        return redirect('index', locals())
    userid = request.session.get('user_id', None)
    user = User.objects.get(id=userid)
    if not user.is_admin:
        return redirect('index', locals())

    data = {
        "isTop": False
    }
    post_id = request.GET.get("post_id", None)
    post = Post.objects.get(id=post_id)
    if post.is_top:
        post.is_top = False
    else:
        post.is_top = True
        data["isTop"] = True
    post.save()
    return JsonResponse(data)
