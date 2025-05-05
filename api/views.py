from django.shortcuts import render
from rest_framework import serializers
from rest_framework import generics
from .serializers import *
from .models import *
from rest_framework.response import Response

# Create your views here.
class SujetForumList(generics.ListCreateAPIView):
    queryset = sujets_forum.objects.all()
    serializer_class = SujetForumSerializer

class SujetForumDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = sujets_forum.objects.all()
    serializer_class = SujetForumSerializer
    lookup_field = 'pk'

class PublicationList(generics.ListCreateAPIView):
    queryset = publications.objects.all()
    serializer_class = PublicationSerializer

class PublicationDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = publications.objects.all()
    serializer_class = PublicationSerializer
    lookup_field = 'pk'

class CommentairesListCreateView(generics.ListCreateAPIView):
    queryset = commentaires.objects.all()
    serializer_class = CommentairesSerializer

class CommentairesRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = commentaires.objects.all()
    serializer_class = CommentairesSerializer
    lookup_field = 'pk'

class Messages_priveesListCreateView(generics.ListCreateAPIView):
    queryset = messages_privees.objects.all()
    serializer_class = Messages_priveesSerializer

class Messages_priveesRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = messages_privees.objects.all()
    serializer_class = Messages_priveesSerializer
    lookup_field = 'pk'

class Messages_forumListCreateView(generics.ListCreateAPIView):
    queryset = messages_forum.objects.all()
    serializer_class = Messages_forumSerializer

class Messages_forumRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = messages_forum.objects.all()
    serializer_class = Messages_forumSerializer
    lookup_field = 'pk'





