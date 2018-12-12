from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from one_page.models import Labeled, Unlabeled
from django.contrib.auth.models import User

# Create your models here.


class Question(models.Model):
    qid1 = models.ForeignKey(Labeled, on_delete='CASCADE', related_name='labeled1')
    qid2 = models.ForeignKey(Labeled, on_delete='CASCADE', related_name='labeled2')
    qid3 = models.ForeignKey(Labeled, on_delete='CASCADE', related_name='labeled3')
    qid4 = models.ForeignKey(Unlabeled, on_delete=models.CASCADE, related_name='unlabeled')
    user = models.OneToOneField(User, on_delete='CASCADE', primary_key=True)
