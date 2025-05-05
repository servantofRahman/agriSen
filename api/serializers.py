# from .views import *
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class SujetForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = sujets_forum
        fields = ['sujet_id', 'titre', 'user_id', 'date_creation', 'est_prive']

class PublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = publications
        fields = ['publication_id', 'user_id', 'contenu', 'image', 'date_publication', 'region', 'culture_associee']

class CommentairesSerializer(serializers.ModelSerializer):
    class Meta:
        model = commentaires
        fields = ['commentaire_id', 'publication_id', 'user_id', 'contenu', 'date_commentaire']

class Message_priveesSerializer(serializers.ModelSerializer):
    class Meta:
        model = messages_privees
        fields ='__all__' 

class Messages_forumSerializer(serializers.ModelSerializer):
    class Meta:
        model = messages_forum
        fields = '__all__'







        