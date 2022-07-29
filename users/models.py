import uuid
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=100, null=True)
    years_of_exp = models.DecimalField(max_digits=2, decimal_places=1)
    description = models.TextField(max_length=4000)
    resume = models.FileField(default="default.png" , upload_to="resumes", max_length=100, null = True, serialize=True)
    