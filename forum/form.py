from django import forms
from .models import Post
from .models import Comment
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget


# 评论表单
# 表单对应有一个数据库模型 用ModelForm
class CommentForm(forms.ModelForm):
    # content = forms.CharField(label="评论内容", max_length=1024, widget=forms.Textarea(
    # attrs={'class': 'form-control', 'placeholder': "comment", 'autofocus': ''}))
    # content = forms.CharField(label="", max_length=1024, widget=CKEditorWidget(), required=True)
    content = forms.CharField(label="", max_length=204800, widget=CKEditorUploadingWidget(), required=True)

    # content = RichTextFormField(label="")

    class Meta:
        model = Comment  # 表明这个表单对应的数据库模型是 Comment 类
        fields = ['content']  # 指定了表单需要显示的字段


# 帖子表单
# class PostForm(forms.ModelForm):
# sections = (
#    (0, "讨论区"),
#    (1, "刷题区"),
#    (2, "校园区"),
#    (3, "课程推荐区"),
#    (4, "资源区"),
# )
# title = forms.CharField(label="标题", max_length=128, widget=forms.TextInput(
#     attrs={'class': 'form-control', 'placeholder': "Title", 'autofocus': ''}))
# content = forms.CharField(label="文章内容", max_length=1024, widget=forms.Textarea(
#     attrs={'class': 'form-control', 'placeholder': "content", 'autofocus': ''}))
# section = forms.ChoiceField(label='文章标签', widget=forms.widgets.Select(choices=sections))

# file = forms.FileField(label="文件上传")
# image = forms.ImageField(label="图片上传")

# bool = forms.BooleanField(required=False)
# urf = forms.URLField(label="url格式")
# data = forms.DateField(label="日期格式")
# email = forms.EmailField(label="邮箱格式")
# class Meta:
# 指明数据模型来源
# model = Post
# 定义表单包含的字段
# fields = ('title', 'content', 'section', 'level_restriction')
# fields = ('title', 'content')

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ["title", "content", "section", "level_restriction"]


# 提及表单
class MentionForm(forms.Form):
    pass
