from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.template import loader
from questions.models import Question, Tag, Profile, Answer, User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from questions.forms import loginForm, signupForm, settingsForm, questionForm, answerForm

def test(request):
  template = loader.get_template('questions/test.html')
  return HttpResponse(template.render({}, request))

def index(request):
  profile = Profile.objects.getProfile(request.user)
  recent = Question.objects.recentQuestions()
  tBags = Tag.objects.all()
  page, paginator = paginate(recent, request)
  context = {
    'recent': page,
    'paginator': paginator,
    'tags': tBags,
    'profile': profile
  }
  template = loader.get_template('questions/index.html')
  return HttpResponse(template.render(context, request))

def tag(request, tagValue):
  profile = Profile.objects.getProfile(request.user)
  tBg = Tag.objects.filter(name=tagValue)[:1]
  recent = Question.objects.filter(tag=tBg)
  tBags = Tag.objects.all()
  page, paginator = paginate(recent, request)
  context = {
    'recent': page,
    'paginator': paginator,
    'tags': tBags,
    'profile': profile,
  }
  template = loader.get_template('questions/index.html')
  return HttpResponse(template.render(context, request))

def question(request, questionId):#page with answers and stuff
  profile = Profile.objects.getProfile(request.user)
  question = get_object_or_404(Question, pk=questionId)
  tBags = Tag.objects.all()
  answers = Answer.objects.getAnswersToQuestion(questionId)
  page, paginator = paginate(answers, request)
  form = answerForm()
  error_message = ''

  if request.method == 'POST':
    form = answerForm(request.POST)
    if form.is_valid():
      Answer.objects.createAnswer(profile, form.cleaned_data['answerTextField'], question)
      return redirect('/question/' + str(questionId))
    else:
      error_message = form.errors  # 'Form\'s not valid'

  context = {
    'question': question,
    'answers': page,
    'paginator': paginator,
    'tags': tBags,
    'form': form,
    'error_message': error_message,
    'profile': profile,
  }

  template = loader.get_template('questions/question.html')
  return HttpResponse(template.render(context, request))

def hot(request):
  profile = Profile.objects.getProfile(request.user)
  hot = Question.objects.bestQuestions()
  page, paginator = paginate(hot, request)
  tBags = Tag.objects.all()

  context = {
    'recent': page,#me too lazy me not want to rewrite! arghhh!!!
    'paginator': paginator,
    'tags': tBags,
    'profile': profile,
  }
  template = loader.get_template('questions/hot.html')
  return HttpResponse(template.render(context, request))

def signup(request):
  profile = Profile.objects.getProfile(request.user)
  tBags = Tag.objects.all()
  error_message = ''
  form = signupForm()
  if request.method == 'POST':
    form = signupForm(request.POST, request.FILES)
    if form.is_valid():
      if (request.POST['repeat'] == request.POST['passwordField']):
        Profile.objects.createProfile(form.cleaned_data['usernameField'], form.cleaned_data['firstNameField'],
              form.cleaned_data['emailField'], form.cleaned_data['passwordField'], form.cleaned_data['imageField'])
        return redirect('/')
      else:
        error_message = 'Passwords don\'t match'
    else:
      error_message = form.errors  # 'Form\'s not valid'

  context = {
    'tags': tBags,
    'error_message': error_message,
    'form': form,
    'profile': profile
  }

  template = loader.get_template('questions/signup.html')
  return HttpResponse(template.render(context, request))

def settings(request):
  profile = Profile.objects.getProfile(request.user)
  import logging
  logging.warning(profile.user.__dict__)

  tBags = Tag.objects.all()
  error_message = ''

  if request.method == 'POST':
    form = settingsForm(request.POST, request.FILES)
    if form.is_valid():
      request.user.first_name = form.cleaned_data['firstNameField']
      request.user.email = form.cleaned_data['emailField']
      Profile.objects.changeProfile(request.user, form.cleaned_data['imageField'])
      return redirect('/')
    else:
      error_message = form.errors  # 'Form\'s not valid'
  else:
    form = settingsForm(initial={
      'firstNameField': profile.user.first_name,
      'emailField': profile.user.email,
      'imageField': profile.avatar,
    })

  context = {
    'tags': tBags,
    'error_message': error_message,
    'form': form,
    'profile': profile
  }

  template = loader.get_template('questions/settings.html')
  return HttpResponse(template.render(context, request))

def login_me(request):
  tBags = Tag.objects.all()
  error_message = ''
  form = loginForm()
  if request.method == 'POST':
    form = loginForm(request.POST)
    if form.is_valid():
      username = request.POST['usernameField']
      password = request.POST['passwordField']
      user = authenticate(username=username, password=password)
      if user is not None:
        login(request, user)
        return redirect('questions.views.index')
        # Redirect to a success page.
      else:
        error_message = 'Sorry lad, can\'t find you here'
    else:
      error_message = 'Form\'s not valid'

  context = {
    'tags': tBags,
    'error_message': error_message,
    'form': form,
  }

  template = loader.get_template('questions/login.html')
  return HttpResponse(template.render(context, request))

def logout_me(request):
  logout(request)
  return redirect('/')

def ask(request):
  profile = Profile.objects.getProfile(request.user)
  tBags = Tag.objects.all()
  error_message = ''
  form = questionForm()

  if request.method == 'POST':
    form = questionForm(request.POST)
    if form.is_valid():
      Question.objects.createQuestion(profile, form.cleaned_data['titleField'], form.cleaned_data['questionTextField'],
              form.cleaned_data['tagsField'].split())
      return  redirect('/')
    else:
      error_message = form.errors

  context = {
    'profile': profile,
    'tags': tBags,
    'error_message': error_message,
    'form': form,
  }

  template = loader.get_template('questions/ask.html')
  return HttpResponse(template.render(context, request))

def paginate(objects_list, request): 
  paginator = Paginator(objects_list, 10)
  try:
    page = request.GET.get('page')
    objPage = paginator.page(page)
  except PageNotAnInteger:
    objPage = paginator.page(1)
  except EmptyPage:
    objPage = paginator.page(paginator.num_pages)
  return objPage, paginator