from django.forms import ModelForm
from .models import Comment


class CommentModelForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
