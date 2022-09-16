# Django
from django.db import models


class Product(models.Model):
    title = models.CharField(
        max_length = 60,
        blank = False,
        null = False
        )
    description = models.TextField(
        blank = False,
        null = False
        )
    # image = models.ImageField(
    #     upload_to = 'products/',
    #     blank = True,
    #     null = True
    #     )
    price = models.DecimalField(
        decimal_places = 2,
        max_digits = 10,
        null = False,
        blank= False
        )
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.title