from django.contrib import admin
from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        
    path('sujet-forum/', SujetForumList.as_view(), name='sujet-list'),
    path('sujet-forum/public/', SujetForumListPublic.as_view(), name='sujet-list'),
    path('sujet-forum/<uuid:pk>/', SujetForumDetails.as_view(), name='sujet-forum-details'),
    path('sujet-forum/messages/<uuid:sujet_id>/', SujetForumMessagesView.as_view()),
    path('messages-forum/', Messages_forumListCreateView.as_view(), name='messages-forum-list'),
    path('messages-forum/<uuid:pk>/', Messages_forumRetrieveUpdateDestroyView.as_view(), name='messages-forum-details')
]
