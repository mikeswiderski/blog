from django.conf import settings
from django.db import models


User = settings.AUTH_USER_MODEL
STATUS = [
    ('DRAFT', 'Draft'),
    ('PUBLISHED', 'Published'),
]

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField() 
    status = models.CharField(max_length=9, choices=STATUS, default='DRAFT',)
    def __str__(self):
        return self.title
