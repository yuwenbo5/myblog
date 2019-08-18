# -*- coding:utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
    url('^/?$',views.index),
    url(r'^login/$',views.login),
    url(r'^logout/$',views.logout),
    url(r'^index/$', views.index),
    url(r'^setinfo/$', views.setinfo),
    url(r'^password/$', views.password),
    url(r'^adv/$', views.adv),
    url(r'^page/$', views.page),
    url(r'^book/$', views.book),
    url(r'^column/$', views.column),
    url(r'^bloglist/$', views.bloglist),
    url(r'^addblog/$', views.addblog),
    url(r'^cate/$', views.cate),
    url(r'^cateedit/$',views.cateedit),
    url(r'^document/$',views.document),
    url(r'^collection/$',views.collection),
    url(r'^link/$',views.link),
    url(r'^photos/$',views.photos),
    url(r'^picture/$',views.picture),
    url(r'^ajax/$', views.ajaxPost),
    url(r'^upload_editor/$',views.upload_editor),
    url(r'^delete_action/$',views.delete_action),
]

