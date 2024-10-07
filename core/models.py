from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    level_of_education = models.CharField(max_length=100)
    school_name = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username
