from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
import math

from django.template.defaultfilters import striptags

from space.forms import *
from space.models import *
from login.models import *
from forum.models import *
from login.views import get_login_status
# add for letter
from forum.form import PostForm, CommentForm
from forum.models import Post, Comment, UpAndDown
UP_AND_DOWN_EXP = 40
CREATE_POST_EXP = 70
COMMENT_EXP = 20


def get_space_status(request, userid, ownerid):
    is_login = get_login_status(request)
    is_owner = (str(userid) == str(ownerid))
    space_owner = User.objects.get(id=ownerid)
    user = User.objects.get(id=userid)
    try:
        BlackList.objects.get(BlockerID=userid, BlockedID=ownerid)
        is_Black = True
    except:
        is_Black = False
    try:
        Follow.objects.get(FollowerID=userid, FollowedID=ownerid)
        is_Following = True
    except:
        is_Following = False
    return is_login, is_owner, space_owner, user, is_Following, is_Black


# Create your views here.
def space(request, id):
    is_login = get_login_status(request)
    if is_login:
        userid = request.session.get('user_id', None)
        is_login, is_owner, space_owner, user, is_Following, is_Black = get_space_status(request, userid, id)

        posts = Post.objects.filter(author=id)
        comments = Comment.objects.filter(user=id)
        for post in posts:
            post.comment_count = len(Comment.objects.filter(post=post))
            # print(post.get_absolute_url())
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
        # 限定显示30个字符
        for i in posts:
            # print(i.comment_set.all().count)
            i.content = striptags(i.content)
            if len(i.content) > 30:
                i.content = i.content[0:30] + "..."
        for i in comments:
            # print(i.comment_set.all().count)
            i.content = striptags(i.content)
            if len(i.content) > 30:
                i.content = '{}...'.format(str(i.content)[0:29])
        return render(request, "space/space.html", locals())
    else:
        return redirect('/index/', locals())


def myInfo(request, id):
    is_login = get_login_status(request)
    if is_login:
        userid = request.session.get('user_id', None)
        is_login, is_owner, space_owner, user, is_Following, is_Black = get_space_status(request, userid, id)
        return render(request, "space/myInfo.html", locals())
    # return redirect(reverse('settings', kwargs={'id': id}), locals())
    return render(request, "forum/index.html", locals())


def settings(request, id):
    # 定制化提示信息，
    is_login = get_login_status(request)
    if is_login:
        userid = request.session.get('user_id', None)
        is_login, is_owner, space_owner, user, is_Following, is_Black = get_space_status(request, userid, id)

        if request.method == "POST":
            flag = 0
            if is_owner and user.is_admin:
                flag = -1
                form = userInfo_all(request.POST, request.FILES, instance=space_owner)
            elif is_owner:
                flag = 0
                form = userInfo_user(request.POST, request.FILES, instance=space_owner)
            elif not is_owner and user.is_admin:
                flag = 1  # 因为这里没有name，特殊处理
                form = userInfo_admin(request.POST, request.FILES, instance=space_owner)
            now_name = space_owner.name
            # 如果全部输入信息有效
            if form.is_valid() and flag != 1:
                value = form.cleaned_data['name']
                print(space_owner.name)
                print(value)
                if User.objects.filter(name=value) and now_name != value:
                    space_owner.name = now_name
                    messages.success(request, "用户名已存在")
                    return redirect(reverse('space', args=str(id)), locals())
                print(1)
                form.save(commit=True)
                messages.success(request, "修改成功")
                return redirect(reverse('space', args=str(id)), locals())
            elif form.is_valid():  # 无name字段
                form.save(commit=True)
                messages.success(request, "修改成功")
                return redirect(reverse('space', args=str(id)), locals())
            else:
                if flag == -1:
                    messages.success(request, "修改失败！注意年龄/经验值不得小于0, 密码长度需要在4~16之间，使用合法邮箱格式")
                elif flag == 0:
                    messages.success(request, "修改失败！注意年龄不得小于0，密码长度需要在4~16之间，使用合法邮箱格式")
                else:
                    messages.success(request, "修改失败！经验值不得小于0")
                print("error")
                # 失败
                # 打印输入的信息
                print("---", form.cleaned_data)  # 得到一个字典
                print("???", form.errors)  # ErrorDict : {"校验错误的字段":["错误信息",]}
                print("!!!", form.errors.get("email"))  # ErrorList ["错误信息",]

                g_error = form.errors.get("__all__")
                print("+++", g_error)  # <ul class="errorlist nonfield"><li>两次密码不一致</li></ul>

                return redirect(reverse('space', args=str(id)), locals())

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

    return render(request, "space/settings.html", locals())

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
        is_login, is_owner, space_owner, user, is_Following, is_Black = get_space_status(request, userid, id)
        follows = Follow.objects.filter(FollowerID=id)
    else:
        return redirect('/index/', locals())
    return render(request, 'space/FriendList.html', locals())


def letterList(request, id):
    is_login = get_login_status(request)
    if is_login:
        userid = request.session.get('user_id', None)
        is_login, is_owner, space_owner, user, is_Following, is_Black = get_space_status(request, userid, id)
        messages = Message.objects.filter(ReceiverID=id)
    else:
        return redirect('/index/', locals())
    return render(request, 'space/LetterList.html', locals())


def letter(request, id):
    is_login = get_login_status(request)
    if is_login:
        userid = request.session.get('user_id', None)
        is_login, is_owner, space_owner, user, is_Following, is_Black = get_space_status(request, userid, id)
        follows = Follow.objects.filter(FollowerID=id)
    else:
        return redirect('/index/', locals())
    return render(request, 'space/Letter.html', locals())


def blackList(request, id):
    is_login = get_login_status(request)
    if is_login:
        userid = request.session.get('user_id', None)
        is_login, is_owner, space_owner, user, is_Following, is_Black = get_space_status(request, userid, id)
        blackLists = BlackList.objects.filter(BlockerID=id)
    else:
        return redirect('/index/', locals())
    return render(request, 'space/BlackList.html', locals())


def BlogList(request, id):
    is_login = get_login_status(request)
    if is_login:
        userid = request.session.get('user_id', None)
        is_login, is_owner, space_owner, user, is_Following, is_Black = get_space_status(request, userid, id)
        favoritePosts = FavoritePost.objects.filter(UserID=id)
    else:
        return redirect('/index/', locals())
    return render(request, 'space/BlogList.html', locals())


# 关注
def follow(request):
    is_follow = False
    followerid = request.GET.get("userId", None)
    follower = User.objects.get(id=followerid)
    followedid = request.GET.get("targetId", None)
    followed = User.objects.get(id=followedid)
    # if Follow.objects.filter(FollowerID=followerid, FollowedID=followedid):
    #     print(1)
    # else: print(2)
    try:
        f = Follow.objects.get(FollowerID=followerid, FollowedID=followedid)
        f.delete()
        is_follow = False
    except:
        print(1)
        new_follow = Follow()
        new_follow.FollowerID = follower
        new_follow.FollowedID = followed
        new_follow.save()
        is_follow = True

    data = {
        "isFollowing": is_follow
    }
    return JsonResponse(data)


def black(request):
    is_black = False
    blockerid = request.GET.get("userId", None)
    blocker = User.objects.get(id=blockerid)
    blockedid = request.GET.get("targetId", None)
    blocked = User.objects.get(id=blockedid)
    try:
        f = BlackList.objects.get(BlockerID=blockerid, BlockedID=blockedid)
        f.delete()
        is_black = False
    except:
        new_black = BlackList()
        new_black.BlockerID = blocker
        new_black.BlockedID = blocked
        new_black.save()
        is_black = True

    data = {
        "isBlacking": is_black
    }
    # print(data)
    return JsonResponse(data)


def ban(request):
    userid = request.session.get('user_id', None)
    ownerid = request.GET.get("id", None)
    space_owner = User.objects.get(id=ownerid)
    user = User.objects.get(id=userid)
    data = {'is_ban': space_owner.is_ban}
    # type = request.GET.get("type", None)
    # id = request.GET.get("id", None)

    # 访客是管理员且被访问者不是管理员
    if user.is_admin and not space_owner.is_admin:
        if space_owner.is_ban:
            space_owner.is_ban = False
            data['is_ban'] = False
        else:
            space_owner.is_ban = True
            data['is_ban'] = True
        space_owner.save()

    return JsonResponse(data)


def level_cal(user):
    return int(math.sqrt(int(user.exp)) // 10 + 1)


def favorite(request):
    userid = request.session.get('user_id', None)
    data = {
        "isFavorite": False
    }

    post_id = request.GET.get("post_id", None)
    try:
        favor = FavoritePost.objects.get(UserID=userid, PostId=post_id)  # 已经关注了，将要取消关注
        favor.delete()
    except FavoritePost.DoesNotExist:
        FavoritePost.objects.create(UserID=userid, PostId=post_id)  # 没有关注，将要关注
        data["isFavorite"] = True

    return JsonResponse(data)