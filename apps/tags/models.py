from django.db import models


class Tag(models.Model):

    label = models.CharField(max_length=40)

    def __str__(self):
        return self.label
