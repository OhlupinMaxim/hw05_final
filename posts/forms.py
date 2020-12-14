from django import forms

from .models import Post, Comment, Group


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("text", "group", "image",)
        labels = {
            "group": "Группы",
            "image": "Изображение"
        }

    text = forms.CharField(widget=forms.Textarea(
        attrs={"placeholder": "Введите текст"}), required=True,
        label="Введите текст")
    group = forms.SelectMultiple(choices=list(Group.objects.values("title")))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)

    text = forms.CharField(widget=forms.Textarea(
        attrs={"placeholder": "Введите текст"}),
        required=True, label="Введите текст")
