from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation


# Create your models here.

class Labeled(models.Model):
    review = models.CharField(max_length=10000)
    polarity = models.BooleanField()

    content_type = models.ForeignKey(ContentType, on_delete='CASCADE')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Unlabeled(models.Model):
    review = models.CharField(max_length=10000)
    score = models.IntegerField(default=0)

    content_type = models.ForeignKey(ContentType, on_delete='CASCADE')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Movie(models.Model):
    title = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    labeled = GenericRelation(Labeled)
    unlabeled = GenericRelation(Unlabeled)

    def get_fields(self):
        data = [('Title', self.title), ('Director', self.director)]
        return data

    def __str__(self):
        return self.title


class Rests(models.Model):
    title = models.CharField(max_length=100)
    cuisine = models.CharField(max_length=20)
    location = models.CharField(max_length=20)
    labeled = GenericRelation(Labeled)
    unlabeled = GenericRelation(Unlabeled)

    def get_fields(self):
        data = [('Name', self.title), ('Cuisine', self.cuisine), ('Location', self.location)]
        return data

    def __str__(self):
        return self.title
