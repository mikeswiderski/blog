from django.conf import settings
from django.db import models
from apps.tags.models import Tag
from apps.users.models import User


class Post(models.Model):

    DRAFT = 'DRAFT'
    PUBLISHED = 'PUBLISHED'
    STATUSES = [
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
    ]
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    status = models.CharField(max_length=9, choices=STATUSES, default=DRAFT,)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title
