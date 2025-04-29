from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('sujet-forum/', SujetForumList.as_view(), name='sujet-list'),
    path('sujet-forum/<uuid:pk>/', SujetForumDetails.as_view(), name='sujet-forum-details'),
]
