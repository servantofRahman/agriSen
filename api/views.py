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
    