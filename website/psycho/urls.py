"""how_u_feel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))

"""
from django.conf.urls import url, patterns
from django.views.generic import TemplateView

urlpatterns = patterns('psycho.views',
                       url(r'^$', 'registration', name='url_registration'),
                       url(r'^quizz/(?P<id>\d+)/(?P<user>\d+)/$', 'TestDetail', name='url_quizz'),
                       url(r'^activity/(?P<user>\d+)/$','AssignActivity', name='url_activity'),
                       url(r'^greetings/$', TemplateView.as_view(template_name='psycho/greetings.html'), name='url_greetings'),
                       url(r'^intro/(?P<user>\d+)/$','ActivityIntro', name='url_intro'),

)
