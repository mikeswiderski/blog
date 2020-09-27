from django.forms import ModelForm
from django import forms
from .models import Post
from apps.tags.models import Tag


class PostModelForm(ModelForm):
    tags = forms.CharField(max_length=255, required=False)
    class Meta:
        model = Post
        fields = [
            'title',
            'body',
            'tags'
          ]


def save(self, commit=True, *args, **kwargs):
    instance = super().save(commit=False, *args, **kwargs)
    tags = self.cleaned_data.get('tags')
    tags_l = [tag.strip() for tag in tags.split(',') if tags]
    final_ids = []
    for tag in tags_l:
        obj, created = Tag.objects.get_or_create(label=tag)
        final_ids.append(obj.id)
    qs = Tag.objects.filter(id__in=final_ids).distinct()
    if commit:
        instance.tags.clear()
        instance.tags.add(qs)
        instance.save()
    return instance 
