"""SE URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from login import views as view_login
from forum import views as view_forum
from space import views as view_space

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', view_login.index, name='index'),
    path('login/', view_login.login, name='login'),
    path('register/', view_login.register, name='register'),
    path('logout/', view_login.logout, name='logout'),
    path('base/', view_forum.base, name='base'),
    path('space/', view_space.base, name='space'),
    path('settings/', view_space.settings, name='settings'),
    # path('post/', view_forum.post, name='post'),
]