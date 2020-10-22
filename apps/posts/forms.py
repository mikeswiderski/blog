from django.forms import ModelForm
from django import forms
from .models import Post
from apps.tags.models import Tag
import re


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
        validated_tags = []

        tags = [tag.strip() for tag in tags.split(',') if tags]

        for tag in tags:
            if re.match('^[a-zA-Z0-9- ]*$', tag):
                validated_tags.append(tag)
            else:
                raise forms.ValidationError('Letters, digits, space, dash only.')

        if len(tags) == len(validated_tags):
            for tag in validated_tags:
                t, created = Tag.objects.get_or_create(label=tag)
                t.save()
                clean_tags.append(t)
    
        return clean_tags
