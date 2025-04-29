from .views import *
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class SujetForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = sujets_forum
        fields = ['sujet_id', 'titre', 'user_id', 'date_creation', 'est_prive']