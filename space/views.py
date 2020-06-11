from django.contrib import messages


from django.http import HttpResponse
from django.shortcuts import render, redirect

from space.forms import userInfo
from space.models import *
from login.models import *
from forum.models import *
from login.views import get_login_status





# Create your views here.
def space(request, id):
    is_login = get_login_status(request)
    if is_login:
        userid = request.session.get('user_id', None)
        is_owner = (str(userid) == str(id))
        space_owner = User.objects.get(id=id)
        # print(is_owner)
        user = User.objects.get(id=userid)
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


def settings(request, id):
    # 定制化提示信息，
    is_login = get_login_status(request)
    if is_login:
        userid = request.session.get('user_id', None)
        user = User.objects.get(id=userid)
        is_owner = (str(userid) == str(id))
        space_owner = User.objects.get(id=id)
        if request.method == "POST":
            form = userInfo(request.POST, request.FILES, instance=user)
            # form = UserInfo(request.POST)
            # 如果全部输入信息有效
            if form.is_valid():
                # image = form.cleaned_data.get('avatar')
                # print(image)
                # request.user.avatar = image
                form.save(commit=True)
                messages.success(request, "修改成功")
                return render(request, "space/space.html", locals())
            else:
                # 失败
                # 打印输入的信息
                print("---", form.cleaned_data)  # 得到一个字典
                print("???", form.errors)  # ErrorDict : {"校验错误的字段":["错误信息",]}
                print("!!!", form.errors.get("email"))  # ErrorList ["错误信息",]

                g_error = form.errors.get("__all__")
                print("+++", g_error)  # <ul class="errorlist nonfield"><li>两次密码不一致</li></ul>
                if g_error:
                    g_error = g_error[0]  # 直接获取你自己的错误提示，即两次密码不一致

                return render(request, "space/settings.html", locals())

        else:
            # email = user.email
            # username = user.name
            # # age = user.age
            # data = {'username': username, 'age': 18, 'email': email}
            # form = UserInfo(data)
            form = userInfo(initial={'name': user.name, 'sex': user.sex, 'age': user.age,
                                     'school': user.school, 'major': user.major,
                                     'exp': user.exp, 'email': user.email, 'avatar': user.avatar}, instance=user)
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
        user = User.objects.get(id=userid)
        is_owner = (str(userid) == str(id))
        space_owner = User.objects.get(id=id)
        follows = Follow.objects.filter(FollowerID=userid)
    else:
        return redirect('/index/', locals())
    return render(request, 'space/FriendList.html', locals())


def blackList(request, id):
    is_login = get_login_status(request)
    if is_login:
        userid = request.session.get('user_id', None)
        user = User.objects.get(id=userid)
        is_owner = (str(userid) == str(id))
        space_owner = User.objects.get(id=id)
        blackLists = BlackList.objects.filter(BlockerID=userid)
    else:
        return redirect('/index/', locals())
    return render(request, 'space/BlackList.html', locals())

