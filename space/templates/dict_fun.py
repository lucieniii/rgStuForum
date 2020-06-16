from django import template

from forum.models import Comment
from space.models import *

register = template.Library()


def get_comment_count(obj):
    return Comment.object.filter(post=obj).count()


register.filter('get_comment_count', get_comment_count)
