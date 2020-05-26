from django.shortcuts import render


# Create your views here.
def base(request):
    return render(request, 'base/base.html')


def post(request):
    return render(request, 'base/post.html')

