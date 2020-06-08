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
    path('index/', view_forum.index, name='index'),
    path('ForumBoard/<int:id>/', view_forum.forumBoard, name='ForumBoard'),
    path('FollowUser/', view_forum.followUser, name='FollowUser'),
    path('Mention/', view_forum.mention, name='Mention'),
    path('FollowPost/', view_forum.followPost, name='FollowPost'),
    path('login/', view_login.login, name='login'),
    path('register/', view_login.register, name='register'),
    path('logout/', view_login.logout, name='logout'),
    path('base/', view_forum.base, name='base'),
    path('space/', view_space.space, name='space'),
    path('settings/', view_space.settings, name='settings'),
    # path('notice/', include('notice.urls', namespace='notice')),
    path('post_list/', view_forum.post_list, name='post_list'),
    path('post/<int:id>/', view_forum.post_detail, name='post_detail'),
    path('post_create/', view_forum.post_create, name='post_create'),
    path('PostContent', view_forum.PostContent, name='PostContent')
]