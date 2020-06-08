from django.http import HttpResponse
from django.shortcuts import render
from space.models import *
from login.models import *
from forum.models import *
from login.views import get_login_status


# Create your views here.
def space(request):
    # is_login = get_login_status(request)
    userid = request.session.get('user_id', None)
    user = User.objects.get(id=userid)
    posts = Post.objects.filter(author=userid)
    comments = Comment.objects.filter(user=userid)
    # Comment表里没有post的title属性，故在本地进行查询
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
    if posts:
        return render(request, "space/space.html", locals())
    else:
        return HttpResponse("暂无发帖记录")


def settings(request):
    pass
    '''
    userid = request.session.get('user_id', None)
    follows = Follow.objects.filter(FollowerID=userid)
    context = {"follows": follows}
    if follows:
        return render(request, "space/settings.html", context)
    else:
        return HttpResponse("暂无关注用户")
    '''

    '''
    userid = request.session.get('user_id', None)
    favoritePosts = FavoritePost.objects.filter(UserID=userid)
    context = {"favoritePosts": favoritePosts}
    if favoritePosts:
        return render(request, "space/settings.html", context)
    else:
        return HttpResponse("暂无收藏帖子")
    '''
