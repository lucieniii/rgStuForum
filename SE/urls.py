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
from django.urls import path, include, re_path
from login import views as view_login
from forum import views as view_forum
from space import views as view_space
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', view_forum.index, name='index'),
    path('ForumBoard/<int:id>/', view_forum.forumBoard, name='ForumBoard'),
    path('FollowUser/', view_forum.followUser, name='FollowUser'),
    path('Mention/', view_forum.mention, name='Mention'),
    path('FollowPost/', view_forum.followPost, name='FollowPost'),
    # re_path(r'^PostContent/(?P<s>[0-9]+(&[0-9]+)*)/$', view_forum.PostContent, name='PostContent'),
    path('PostContent/<str:s>/', view_forum.PostContent, name='PostContent'),
    path('login/', view_login.login, name='login'),
    path('post_create/', view_forum.post_create, name='post_create'),
    path('post_update/<int:id>/', view_forum.post_update, name='post_update'),
    path('post_list/', view_forum.post_list, name='post_list'),
    path('register/', view_login.register, name='register'),
    # path('post_safe_delete/<int:id>/', view_forum.post_safe_delete, name='post_safe_delete'),
    path('logout/', view_login.logout, name='logout'),
    path('base/', view_forum.base, name='base'),
    path('space/<int:id>/', view_space.space, name='space'),
<<<<<<< HEAD
    path('settings/', view_space.settings, name='settings'),
    path('FriendList/', view_space.friendList, name='FriendList'),
    path('BlackList/', view_space.blackList, name='BlackList'),
    path('BlogList/', view_space.BlogList, name='BlogList'),
=======
    path('settings/<int:id>', view_space.settings, name='settings'),
    path('FriendList/<int:id>', view_space.friendList, name='FriendList'),
    path('BlackList/<int:id>', view_space.blackList, name='BlackList'),
    path('ajax/thumb/', view_forum.thumb, name='thumb'),
    path('ajax/follow/', view_space.follow, name='follow'),
    path('ajax/black/', view_space.black, name='black'),
>>>>>>> 26438383c1da452b093766b1bd7bc756c3037a60
    # path('notice/', include('notice.urls', namespace='notice')),
    url(r'', include('ckeditor_uploader.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 图片相关
