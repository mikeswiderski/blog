from django.forms import ModelForm
from django import forms
from .models import Post
from apps.tags.models import Tag
import re


pattern = re.compile(r'^[a-zA-Z0-9- ]*$')

class PostModelForm(ModelForm):

    tags = forms.CharField(max_length=255, required=False)

    class Meta:
        model = Post
        fields = [
            'title',
            'body',
            'tags',
        ]

    def clean_tags(self):
        tags = self.cleaned_data.get('tags', None)
        clean_tags = []

        tags = [tag.strip() for tag in tags.split(',') if tags]

        for tag in tags:
            if pattern.match(tag):
                continue
            else:
                raise forms.ValidationError('Letters, digits, space, dash only.')

        
        for tag in tags:
            t, created = Tag.objects.get_or_create(label=tag)
            t.save()
            clean_tags.append(t)
    
        return clean_tags
