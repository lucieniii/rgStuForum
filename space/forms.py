from login.models import *
from django.forms import ModelForm
from django import forms
from django.forms import widgets
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError


# 除了等级都能改，专供管理员改自己
class userInfo_all(ModelForm):
    class Meta:
        model = User
        # fields = ["avatar"]
        exclude = ('is_admin', 'c_time', 'level', 'is_ban')
        widgets = {
        }

    def clean_age(self):
        age = self.cleaned_data['age']
        if (not age is None) and age < 1:
            raise ValidationError('年龄不得小于1')
        return age

    def clean_exp(self):
        exp = self.cleaned_data['exp']
        if exp < 0:
            raise ValidationError('经验值不得小于0')
        return exp

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 4:
            raise ValidationError('密码不得少于4位')
        elif len(password) > 16:
            raise ValidationError('密码不得多于16位')
        return password

    ## 每个字段数据格式通过验证都会触发下面的对应的字段名字自定方法
    # def clean_name(self):
    #     value = self.cleaned_data['name']
    #     if User.objects.filter(name=value):
    #         raise ValidationError('用户已存在')
    #     else:
    #         return value

    # 重写，不然会检测username唯一性
    def clean(self):
        return self.cleaned_data


# 除了经验、等级、禁言都能改
class userInfo_user(ModelForm):
    class Meta:
        model = User
        exclude = ('is_admin', 'c_time', 'exp', 'level', 'is_ban')
        widgets = {
        }

    def clean_age(self):
        age = self.cleaned_data['age']
        if (not age is None) and age < 1:
            raise ValidationError('年龄不得小于1')
        return age

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 4:
            raise ValidationError('密码不得少于4位')
        elif len(password) > 16:
            raise ValidationError('密码不得多于16位')
        return password

    # def clean_name(self):
    #     value = self.cleaned_data['name']
    #     if User.objects.filter(name=value):
    #         raise ValidationError('用户已存在')
    #     else:
    #         return value
    def clean(self):
        return self.cleaned_data


# 只能改经验值
class userInfo_admin(ModelForm):
    class Meta:
        model = User
        fields = ['exp']
        widgets = {
        }

    # def clean_name(self):
    #     value = self.cleaned_data['name']
    #     if User.objects.filter(name=value):
    #         raise ValidationError('用户已存在')
    #     else:
    #         return value

    def clean(self):
        exp = self.cleaned_data['exp']
        if exp < 0:
            raise ValidationError('经验值不得小于0')
        return self.cleaned_data

# class UserInfo(forms.Form):
#     username = forms.CharField(
#         required=True,  # 标明是必填字段，不能为空
#         min_length=1, max_length=128,
#         label="用户名",
#         error_messages={"required": "用户名不能为空！！"},
#         widget=widgets.TextInput(attrs={"placeholder": "用户名", "class": "form-control"}),  # 自动生成input框
#
#     )
#
#     # password = forms.CharField(
#     #     widget=widgets.PasswordInput(attrs={"placeholder": "密码", "class": "form-control"}),
#     #     label="密码",
#     # )
#     #
#     # sec_pwd = forms.CharField(
#     #     required=True,
#     #     label="二次密码",
#     #     widget=widgets.PasswordInput(attrs={"placeholder": "二次密码", "class": "form-control"})
#     # )
#
#     age = forms.IntegerField(
#         label="年龄",
#         widget=widgets.NumberInput(attrs={"placeholder": "年龄", "class": "form-control"}),
#         error_messages={"required": "输入不对！！"},
#     )
#
#     email = forms.EmailField(
#         widget=widgets.EmailInput(attrs={"placeholder": "邮箱", "class": "form-control"}),
#         label="邮箱",
#         error_messages={"invalid": "格式错误"}
#     )
#     major = forms.CharField(
#         label="专业",
#         widget=widgets.TextInput(attrs={"placeholder": "用户名", "class": "form-control"}),
#         error_messages={"invalid": "格式错误"}
#     )
#     school = forms.CharField(
#         label="学校",
#         widget=widgets.TextInput(attrs={"placeholder": "用户名", "class": "form-control"}),
#         error_messages={"invalid": "格式错误"}
#     )
#     sex = forms.ChoiceField(
#         initial=1,
#         choices=((1, '男'), (2, '女'))
#     )
#     avatar = forms.ImageField(
#
#     )
#
#     # 定制化二次错误信息
#
#     # 局部钩子
#     # 注意这里必须是以clean_  开头，可以查看源码,下面得到的val都是字符串类型
#     def clean_username(self):
#         val = self.cleaned_data.get("username")
#         if not val.isdigit():
#             return val
#         else:
#             raise ValidationError("用户名非纯数字")
#
#     # def clean_password(self):
#     #     val = self.cleaned_data.get("password")
#     #     if len(val) > 3:
#     #         return val
#     #     else:
#     #         raise ValidationError("密码太短")
#
#     def clean_age(self):
#         val = self.cleaned_data.get("age")
#         if int(val) > 4:
#             return val
#         else:
#             raise ValidationError("岁数太小")
#
#     # 全局钩子
#     # 对于两次输入的密码进行校验是否一致
#     # def clean(self):
#     #     password = self.cleaned_data.get("password")
#     #     sec_pwd = self.cleaned_data.get("sec_pwd")
#     #     if password == sec_pwd:
#     #         return self.cleaned_data
#     #     else:
#     #         raise ValidationError("两次密码不一致")
