from django.db import models
from django.contrib.auth.models import User


class User(User):
    pass


class Collection(models.Model):
    collection_name = models.CharField(max_length=200)
    collection_description = models.CharField(max_length=20000, default="-")
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=200, default=None)
    description = models.CharField(max_length=200000, default=None)
    genres = models.CharField(max_length=20000, default=None)
    uuid = models.UUIDField(unique=False)
    collection_uuid = models.UUIDField(unique=False)

    def __str__(self):
        return self.collection_name


class MovieDetails(models.Model):
    title = models.CharField(max_length=200, default=None)
    description = models.CharField(max_length=200000, default=None)
    genres = models.CharField(max_length=20000, default=None)
    uuid = models.UUIDField()


class RequestsCounter(models.Model):
    count = models.ForeignKey("self", related_name="calls", null=True, blank=True, on_delete=models.CASCADE)
    hits = models.IntegerField()
