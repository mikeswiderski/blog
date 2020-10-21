from django.db import models
from django.core.validators import RegexValidator 


validate_alphanumeric = RegexValidator(r'^[a-zA-Z0-9- ]*$', 'Letters, digits, space, dash only.')

class Tag(models.Model):
    
    label = models.CharField(max_length=40, validators=[validate_alphanumeric])
    
    def __str__(self):
        return self.label
