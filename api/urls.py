from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('sujet_forum/', SujetForumList.as_view(), name='sujet-list'),
    path('sujet_forum/<uuid:pk>/', SujetForumDetails.as_view(), name='sujet-forum-details'),
]
