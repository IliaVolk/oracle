"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create$', views.create_meeting),
    url(r'^auth$', views.auth),
    url(r'^auth_begin$', views.auth_begin),
    url(r'^redirect$', views.auth_redirect),
    url(r'^logout$', views.logout),
    url(r'^meetings$', views.view_meetings),
    url(r'^invitations$', views.view_invitations),
    url(r'^edit/(?P<id>\d+)/$', views.edit),
    url(r'^update/(?P<id>\d+)/', views.update),
    url(r'^edit/(?P<id>\d+)/accept$', views.accept),
    url(r'^edit/(?P<id>\d+)/discard$', views.discard),
    url(r'^edit/(?P<id>\d+)/delete$', views.delete_meeting),
    url(r'^access_denied$', views.access_denied)
]



