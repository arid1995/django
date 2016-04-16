from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
import datetime

class Question(models.Model):
  title = models.CharField(max_length=200)
  text = models.TextField()
  added_at = models.DateTimeField(default = datetime.datetime.now)
  author = models.ForeignKey(User)
  votes = models.IntegerFi(User, related_name='voted_users')

class Answer(models.Model):
  text = model.TextField()
  author = models.ForeignKey(User)
  question = models.ForeignKey(Question)
  
class Like(models.Model)
  user = models.ForeignKey(User)
  question = Models.ForeignKey(Question)
  is_like = BooleanField()
