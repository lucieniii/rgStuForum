from django.shortcuts import render
from .form import CommentForm
from forum.models import Post
from .models import Comment
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse


# Create your views here.
def post_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        # 当调用 form.is_valid() 方法时，Django 自动帮我们检查表单的数据是否符合格式要求。
        if comment_form.is_valid():
            # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库。
            new_comment = comment_form.save(commit=False)
            # 将评论和被评论的文章关联起来。
            new_comment.post = post
            new_comment.user = request.user
            # 最终将评论数据保存进数据库，调用模型实例的 save 方法

            new_comment.save()
            return redirect(post)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
            # comment_list = post.comment_set.all()
            # context = {'post': post,
            #            'form': comment_form,
            #            'comment_list': comment_list
            #            }
            # return render(request, 'base/post_detail.html', context=context)  # TODO render
    # 不是 post 请求，说明用户没有提交数据，重定向到文章详情页
    return redirect(post)  # TODO 重定向
