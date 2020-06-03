from django import forms
from .models import Comment


# 评论表单
# 表单对应有一个数据库模型 用ModelForm
class CommentForm(forms.ModelForm):
    content = forms.CharField(label="评论内容", max_length=1024, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': "comment", 'autofocus': ''}))

    class Meta:
        model = Comment  # 表明这个表单对应的数据库模型是 Comment 类
        fields = ['content']  # 指定了表单需要显示的字段
