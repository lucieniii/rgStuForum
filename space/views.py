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
    return render(request, "space/space.html", context)


def settings(request):
    return render(request, "space/settings.html")
