from . import models
from django.shortcuts import render, get_object_or_404, redirect
import markdown
from django.shortcuts import render, get_object_or_404
from .form import CommentForm
from .models import Post, Tag


# Create your views here.
def base(request):
    return render(request, 'base/base.html')


# 文章详情页面的视图函数
def post_detail(request, pk):
    # post = get_object_or_404(Post, pk=pk)
    # post.body = markdown.markdown(post.body,
    #                               extensions=[
    #                                   'markdown.extensions.extra',
    #                                   'markdown.extensions.codehilite',
    #                                   'markdown.extensions.toc',
    #                               ])
    # # 记得在顶部导入 CommentForm
    # form = CommentForm()
    # # 获取这篇 post 下的全部评论
    # comment_list = post.comment_set.all()
    #
    # # 将文章、表单、以及文章下的评论列表作为模板变量传给 detail.html 模板，以便渲染相应数据。
    # context = {'post': post,
    #            'form': form,
    #            'comment_list': comment_list
    #            }
    # return render(request, 'post.html', context=context)
    return render(request, 'base/post.html')


def post_rank(request):
    # 文档内容
    # 获取显示的文章id
    nid = request.GET.get('nid')
    # 获取文章
    post_data = models.Post.objects.filter(id=nid).first()
    # 获取到的文章调用increase_views方法
    models.Post.increase_views(post_data)
    # 根据自增的views字段进行排序，并获取最高的5条数据
    hot_doc = models.Post.objects.order_by("-views")[0:5]
    return render(request, "?????.html", {"post_data": post_data, 'hot_doc': hot_doc})  # TODO


def post_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        # 当调用 form.is_valid() 方法时，Django 自动帮我们检查表单的数据是否符合格式要求。
        if form.is_valid():
            # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库。
            comment = form.save(commit=False)
            # 将评论和被评论的文章关联起来。
            comment.post = post
            # 最终将评论数据保存进数据库，调用模型实例的 save 方法
            comment.save()
            return redirect(post)
        else:
            comment_list = post.comment_set.all()
            context = {'post': post,
                       'form': form,
                       'comment_list': comment_list
                       }
            return render(request, '????.html', context=context)  # TODO render
    # 不是 post 请求，说明用户没有提交数据，重定向到文章详情页
    return redirect(post)  # TODO 重定向
