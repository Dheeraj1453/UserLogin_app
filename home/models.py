from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    gender = models.CharField(
        max_length=10,
        choices=[
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other'),
        ]
    )

    def __str__(self):
        return self.user.username

#users contacts model
class Contact(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='contacts'
    )

    image = models.ImageField(
        upload_to='contacts/',
        blank=True,
        null=True
    )

    name = models.CharField(max_length=100)

    contact_number = models.CharField(max_length=20)

    relation = models.CharField(max_length=50)

    def __str__(self):
        return self.name