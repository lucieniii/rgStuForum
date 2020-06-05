from django.http import HttpResponse
from django.shortcuts import render
from space.models import *
from login.models import *
from forum.models import *


# Create your views here.
def space(request):
    userid = request.session.get('user_id', None)
    posts = Post.objects.filter(author=userid)
    # 限定显示30个字符
    for i in posts:
        if len(i.content) > 30:
            i.content = i.content[0:30] + "..."
    context = {"posts": posts}
    if posts:
        return render(request, "space/space.html", context)
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
