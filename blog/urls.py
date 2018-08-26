# -*- coding:utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index/$', views.index),
    url(r'^about/$', views.about),
    url(r'^list/$', views.list),
    url(r'^article/$', views.article),
    url(r'^contact/$', views.contact),
    url(r'^ajax', views.ajaxPost),
]

