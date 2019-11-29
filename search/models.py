from django.db import models
from django.contrib.postgres.fields import HStoreField
# Create your models here.


class Documents(models.Model):
    document = models.CharField(max_length=255)

    def __str__(self):
        return self.document


class InvertedIndex(models.Model):
    word = models.CharField(max_length=100)
    list = HStoreField()

    def __str__(self):
        return self.word

