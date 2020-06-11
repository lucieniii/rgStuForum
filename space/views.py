from django.http import HttpResponse
from django.shortcuts import render, redirect
from space.models import *
from login.models import *
from forum.models import *
from login.views import get_login_status


# Create your views here.
def space(request, id):
    is_login = get_login_status(request)
    if is_login:
        userid = request.session.get('user_id', None)
        is_owner = userid == id
        # print(is_owner)
        user = User.objects.get(id=id)
        posts = Post.objects.filter(author=id)
        comments = Comment.objects.filter(user=id)
        for post in posts:
            post.comment_count = len(Comment.objects.filter(post=post))
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
            # print(i.comment_set.all().count)
            if len(i.content) > 100:
                i.content = i.content[0:100] + "..."
        return render(request, "space/space.html", locals())
    else:
        return redirect('/index/', locals())


def settings(request):
    is_login = get_login_status(request)
    if is_login:
        userid = request.session.get('user_id', None)
        user = User.objects.get(id=userid)
        return render(request, "space/settings.html", locals())
    else:
        return redirect('/index/', locals())

    '''
    is_login = get_login_status(request)
    if is_login:
    '''

    '''
    # 返回个人信息
    userid = request.session.get('user_id', None)
    user = User.objects.get(id=userid)
    return render(request, "space/settings.html", locals())
    '''

    '''
    # 返回关注用户
    userid = request.session.get('user_id', None)
    follows = Follow.objects.filter(FollowerID=userid)
    return render(request, "space/settings.html", locals())
    '''

    '''
    # 返回收藏帖子
    userid = request.session.get('user_id', None)
    favoritePosts = FavoritePost.objects.filter(UserID=userid)
    return render(request, "space/settings.html", locals())
    '''

    '''
    # 返回黑名单
    userid = request.session.get('user_id', None)
    blackList = BlackList.objects.filter(BlockerID=userid)
    return render(request, "space/settings.html", locals())
    '''

    '''
    # 返回私信
    userid = request.session.get('user_id', None)
    messages = Message.objects.filter(SenderID=userid)
    return render(request, "space/settings.html", locals())
    '''

    '''
    # 返回权限信息
    userid = request.session.get('user_id', None)
    permissions = Permission.objects.filter(SenderID=userid)
    return render(request, "space/settings.html", locals())
    '''


def FriendList(request):
    is_login = get_login_status(request)
    if is_login:
        userid = request.session.get('user_id', None)
        user = User.objects.get(id=userid)
    else:
        return redirect('/index/', locals())
    return render(request, 'space/FriendList.html', locals())


def BlackList(request):
    is_login = get_login_status(request)
    if is_login:
        userid = request.session.get('user_id', None)
        user = User.objects.get(id=userid)
    else:
        return redirect('/index/', locals())
    return render(request, 'space/BlackList.html', locals())
