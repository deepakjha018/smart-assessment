from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    EDUCATION_CHOICES = [
        ('School', 'School'),
        ('Undergraduate', 'Undergraduate'),
        ('Postgraduate', 'Postgraduate'),
        ('Other', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(
        upload_to='profiles/',
        default='profiles/default.png'
    )

    education_level = models.CharField(
        max_length=20,
        choices=EDUCATION_CHOICES,
        blank=True
    )

    preferred_category = models.CharField(
        max_length=100,
        blank=True
    )

    def __str__(self):
        return self.user.username
