from __future__ import unicode_literals
from django.http import Http404
from django.contrib.auth.models import User
from django.db import models
import datetime

class TagManager(models.Manager):
  def getTag(self, tagName):
    try:
      result = Tag.objects.get(name=tagName)
      result.popularity += 1
    except Exception:
      result = Tag(name=tagName, popularity=1)
    return result

class QuestionManager(models.Manager):
  def recentQuestions(self):
    try:
      result = self.order_by('added_at').reverse()
    except Exception:
      result = self.order_by('added_at').reverse()
    return result

  def bestQuestions(self):
    try:
      result = self.order_by('votes').reverse()
    except Exception:
      result = self.order_by('votes').reverse()
    return result

  def createQuestion(self, profile, _title, _text, tags):
    quest = Question()
    quest = Question(title = _title, text=_text, author=profile, votes=0)
    quest.save()
    for tag in tags:
      tbag = Tag.objects.getTag(tag)
      tbag.save()
      quest.tag.add(tbag)

class AnswerManager(models.Manager):
  def getAnswersToQuestion(self, questionId):
    try:
      result = self.filter(question = questionId).order_by('added_at').reverse()
    except Exception:
      raise Http404 #FIXME: get rid of exception handling here
    return result

  def createAnswer(self, profile, _text, quest):
    ans = Answer(text=_text, author=profile, question=quest)
    ans.votes = 0
    ans.save()


class ProfileManager(models.Manager):
  def getProfile(self, usr):
    try:
      result = self.get(user = usr)
    except Exception:
      result = None
    return result

  def createProfile(self, usrname, firstName, _email, psword, image):
    usr = User.objects.create_user(username = usrname, first_name = firstName, email = _email, password=psword)
    usr.save()
    prof = Profile()
    prof.avatar = image
    prof.user = usr
    prof.save()

  def changeProfile(self, usr, image):
    prof = Profile.objects.get(user = usr)
    prof.avatar = image
    usr.save()
    prof.save()

class Profile(models.Model):
  user = models.OneToOneField(User)
  avatar = models.ImageField()
  objects = ProfileManager()

class Tag(models.Model):
  name = models.SlugField(max_length = 30)
  popularity = models.IntegerField()
  objects = TagManager()

class Question(models.Model):
  title = models.CharField(max_length = 200)
  text = models.TextField()
  added_at = models.DateTimeField(default = datetime.datetime.now)
  author = models.ForeignKey(Profile)
  votes = models.IntegerField()
  tag = models.ManyToManyField(Tag)
  liked = models.ManyToManyField(Profile, related_name = 'liked')
  objects = QuestionManager()

class Answer(models.Model):
  text = models.TextField()
  author = models.ForeignKey(Profile)
  added_at = models.DateTimeField(default = datetime.datetime.now)
  question = models.ForeignKey(Question)
  votes = models.IntegerField()
  voted = models.ManyToManyField(Profile, related_name = 'voted')
  objects = AnswerManager()