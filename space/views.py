from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
import math
from space.forms import *
from space.models import *
from login.models import *
from forum.models import *
from login.views import get_login_status

_fake_follow = False
_fake_black = False


def get_space_status(request, userid, ownerid):
    is_login = get_login_status(request)
    is_owner = (str(userid) == str(ownerid))
    space_owner = User.objects.get(id=ownerid)
    user = User.objects.get(id=userid)
    is_Following = _fake_follow
    is_Ban = _fake_black
    level = level_cal(space_owner)
    return is_login, is_owner, space_owner, user, is_Following, is_Ban, level


# Create your views here.
def space(request, id):

    is_login = get_login_status(request)
    if is_login:
        userid = request.session.get('user_id', None)
        is_login, is_owner, space_owner, user, is_Following, is_Ban, level = get_space_status(request, userid, id)

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


def myInfo(request, id):
    is_login = get_login_status(request)
    if is_login:
        userid = request.session.get('user_id', None)
        is_login, is_owner, space_owner, user, is_Following, is_Ban, level= get_space_status(request, userid, id)
        return render(request, "space/myInfo.html", locals())

    return render(request, "space/settings.html")


def settings(request, id):
    # 定制化提示信息，
    is_login = get_login_status(request)
    if is_login:
        userid = request.session.get('user_id', None)
        is_login, is_owner, space_owner, user, is_Following, is_Ban, level = get_space_status(request, userid, id)

        if request.method == "POST":
            if is_owner and user.is_admin:
                form = userInfo_all(request.POST, request.FILES, instance=space_owner)
            elif is_owner:
                form = userInfo_user(request.POST, request.FILES, instance=space_owner)
            elif not is_owner and user.is_admin:
                form = userInfo_admin(request.POST, request.FILES, instance=space_owner)
            now_name = space_owner.name
            # 如果全部输入信息有效
            if form.is_valid():
                value = form.cleaned_data['name']
                print(space_owner.name)
                print(value)
                if User.objects.filter(name=value) and now_name != value:
                    space_owner.name = now_name
                    messages.success(request, "用户名已存在")
                    return render(request, "space/space.html", locals())
                print(1)
                form.save(commit=True)
                messages.success(request, "修改成功")
                return render(request, "space/space.html", locals())
            else:
                print("error")
                # 失败
                # 打印输入的信息
                # print("---", form.cleaned_data)  # 得到一个字典
                # print("???", form.errors)  # ErrorDict : {"校验错误的字段":["错误信息",]}
                # print("!!!", form.errors.get("email"))  # ErrorList ["错误信息",]
                #
                # g_error = form.errors.get("__all__")
                # print("+++", g_error)  # <ul class="errorlist nonfield"><li>两次密码不一致</li></ul>
                # if g_error:
                #     g_error = g_error[0]  # 直接获取你自己的错误提示，即两次密码不一致

                return render(request, "space/settings.html", locals())

        else:
            if is_owner and user.is_admin:
                form = userInfo_all(instance=space_owner)
            elif is_owner:
                form = userInfo_user(instance=space_owner)
            elif not is_owner and user.is_admin:
                form = userInfo_admin(instance=space_owner)
            # # form = userInfo(instance=space_owner)
            # form = userInfo_all(initial={'name': space_owner.name, 'sex': space_owner.sex, 'age': space_owner.age,
            #                          'school': space_owner.school, 'major': space_owner.major,
            #                          'exp': space_owner.exp, 'email': space_owner.email, 'avatar': space_owner.avatar},
            #                 instance=space_owner)
            # # 访问者是自己，除了经验值都能改
            # if is_owner:
            #     form.fields['exp'].widget.attrs['readonly'] = True
            #     # form.fields['exp'].disabled = True
            # # 访问者不是自己但是是管理员，只能改经验值
            # elif user.is_admin:
            #     for i in form.fields.values():
            #         i.widget.attrs['readonly'] = True
            #         # i.disabled = True
            #         # i.required = False
            #     form.fields['exp'].disabled = False
            # # 什么也不能改
            # else:
            #     for i in form.fields.values():
            #         i.widget.attrs['readonly'] = True
            #         # i.disabled = True
            #         # i.required = False
            #     form.fields['avatar'].widget.attrs['disabled'] = True
            #     form.fields['sex'].widget.attrs['disabled'] = True
            # # form = UserInfo(request.POST)

            return render(request, "space/settings.html", locals())

    return render(request, "space/settings.html")

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
    blackLists = BlackList.objects.filter(BlockerID=userid)
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


def friendList(request, id):
    is_login = get_login_status(request)
    if is_login:
        userid = request.session.get('user_id', None)
        is_login, is_owner, space_owner, user, is_Following, is_Ban, level= get_space_status(request, userid, id)

        follows = Follow.objects.filter(FollowerID=userid)
    else:
        return redirect('/index/', locals())
    return render(request, 'space/FriendList.html', locals())


def blackList(request, id):
    is_login = get_login_status(request)
    if is_login:
        userid = request.session.get('user_id', None)
        is_login, is_owner, space_owner, user, is_Following, is_Ban, level = get_space_status(request, userid, id)

        blackLists = BlackList.objects.filter(BlockerID=userid)
    else:
        return redirect('/index/', locals())
    return render(request, 'space/BlackList.html', locals())


def BlogList(request):
    is_login = get_login_status(request)
    if is_login:
        userid = request.session.get('user_id', None)
        user = User.objects.get(id=userid)
        follow_posts = Post.objects.filter(favoritepost=userid)
    else:
        return redirect('/index/', locals())
    return render(request, 'space/BlogList.html', locals())


def follow(request):
    global _fake_follow
    request.GET.get("userId", None)
    request.GET.get("targetId", None)
    if _fake_follow:
        _fake_follow = False
    else:
        _fake_follow = True
    data = {
        "isFollowing": _fake_follow
    }
    return JsonResponse(data)


def black(request):
    global _fake_black
    request.GET.get("userId", None)
    request.GET.get("targetId", None)
    if _fake_black:
        _fake_black = False
    else:
        _fake_black = True
    data = {
        "isBlacking": _fake_black
    }
    # print(data)
    return JsonResponse(data)


def level_cal(user):
    return int(math.sqrt(int(user.exp)) // 10 + 1)
