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
        exclude = ('is_admin', 'c_time', 'level', 'is_ban', 'is_read', 'levelname')
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
        exclude = ('is_admin', 'c_time', 'exp', 'level', 'is_ban', 'is_read', 'levelname')
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
