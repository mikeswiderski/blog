from django.forms import ModelForm
from .models import Post


class PostModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostModelForm, self).__init__(*args, **kwargs)
        if self.instance.status == 'PUBLISHED':
            self.fields.pop('status')

    class Meta:
        model = Post
        fields = ['title', 'body', 'status',]
        