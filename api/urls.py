from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('sujet-forum/', SujetForumList.as_view(), name='sujet-list'),
    path('sujet-forum/<uuid:pk>/', SujetForumDetails.as_view(), name='sujet-forum-details'),
    path('publication/', PublicationList.as_view(), name='publication-list'),
    path('publication/<uuid:pk>/', PublicationDetails.as_view(), name='publications-details'),
    path('commentaires/', CommentairesListCreateView.as_view(), name='commentaires-list'),
    path('commentaires/<uuid:pk>/', CommentairesRetrieveUpdateDestroyView.as_view(), name='commentaires-details'),
    path('messages-privees/', Messages_priveesListCreateView.as_view(), name='messages-privees-list'),
    path('messages-privees/<uuid:pk>/', Messages_priveesRetrieveUpdateDestroyView.as_view(), name='messages-privees-details'),
    path('messages-forum/', Messages_forumListCreateView.as_view(), name='messages-forum-list'),
    path('messages-forum/<uuid:pk>/', Messages_forumRetrieveUpdateDestroyView.as_view(), name='messages-forum-details')
]
