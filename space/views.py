from django.shortcuts import render


# Create your views here.
def sapce(request):
    return render(request, "space/space.html")


def settings(request):
    return render(request, "space/settings.html")