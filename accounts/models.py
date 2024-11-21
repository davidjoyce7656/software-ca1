from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    birthdate = models.DateField(default="YYYY-MM-DD")
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Custom related_name
        blank=True
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',  # Custom related_name
        blank=True
    )
    
    def is_over_18(self):
        today = date.today()
        age = today.year - self.birthdate.year - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))