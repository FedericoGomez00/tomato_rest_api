# Django
from django.db import models

# users
from users.models import UserProfile


class BlogPost(models.Model):
    """
    Model of blogpost
    """
    title = models.CharField(
        max_length = 120,
        blank = False,
        null = False
        )
    body = models.TextField(
        blank = False,
        null = False
        )
    author = models.ForeignKey(
        UserProfile,
        null = True,
        on_delete = models.SET_NULL)
    created = models.DateField(auto_now = True)
    # likes = models.ManyToManyField(UserProfile)
    is_active = models.BooleanField(default = True)

    def __str__(self):
        return self.title