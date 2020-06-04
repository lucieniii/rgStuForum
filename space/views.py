from django.shortcuts import render


def index(request):
    is_login = True
    if not request.session.get('is_login', None):
        is_login = False
    return render(request, 'login/index.html', locals())


# Create your views here.
def space(request):
    return render(request, "space/space.html")


def settings(request):
    return render(request, "space/settings.html")
