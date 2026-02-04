from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    user_type = [
        ('operator','Operator'),
        ('manager','Manager')
    ]

    role = models.CharField(choices=user_type, max_length=15 ,default='operator')
    manager_request = models.BooleanField(default=False)

    class Meta:
        db_table = 'user_detail'