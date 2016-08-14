from django.conf.urls import patterns, url

from questions import views

urlpatterns = [
    url(r'^test/$', views.test, name='test'),
    url(r'^$', views.index, name='index'),
    url(r'^hot/$', views.hot, name='hot'),
    url(r'^tag/(?P<tagValue>\w+)/$', views.tag, name='tag'),
    url(r'^question/(?P<questionId>\d+)/$', views.question, name='question'),
    url(r'^login/$', views.login_me, name='login_me'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^ask/$', views.ask, name='ask'),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^logout/$', views.logout_me, name='logout_me'),
]
