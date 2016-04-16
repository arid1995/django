from django.http import HttpResponse


def index(request):
  
  return HttpResponse(request.method)
# Create your views here.
