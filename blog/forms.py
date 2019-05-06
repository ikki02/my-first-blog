from django import forms
from .models import Post, Image


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)


class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = '__all__'  # 多分、全フィールドを自動で指定できる。
