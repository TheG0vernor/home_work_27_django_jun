from django.db import models


# Create your models here.
class Ads(models.Model):
    name = models.CharField(max_length=25)
    author = models.CharField(max_length=25)
    price = models.PositiveIntegerField(default=0)
    description = models.CharField(max_length=460, blank=True)
    address = models.CharField(max_length=260)
    is_published = models.BooleanField(default=False)


class Category(models.Model):
    name = models.CharField(max_length=25)
