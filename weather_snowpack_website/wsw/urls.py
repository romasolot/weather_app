"""wsw URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.contrib import admin
from django.contrib.auth import views
from django.http import HttpResponseRedirect
from django.conf import settings
import wsw.views

urlpatterns = [
    url(r'^favicon.ico/$', lambda x: HttpResponseRedirect(settings.STATIC_URL + 'ico/favicon.ico')),
    url(r'^admin/', admin.site.urls),
    url(r'^dashboard/', wsw.views.dashboard, name='dashboard'),
    url(r'^ex_ch1/', wsw.views.ex_ch1, name='ex_ch1'),
    url(r'^ex_ch2/', wsw.views.ex_ch2, name='ex_ch2'),
    url(r'^$', lambda r: HttpResponseRedirect('dashboard')),
    url(r'^', include('django.contrib.auth.urls')),
]
