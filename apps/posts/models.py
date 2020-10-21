from django.conf import settings
from django.db import models
from apps.tags.models import Tag


User = settings.AUTH_USER_MODEL

class Post(models.Model):
    
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField() 
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title
