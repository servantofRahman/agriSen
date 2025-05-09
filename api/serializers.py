# from .views import *
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

class SujetForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = sujets_forum
        fields = ['sujet_id', 'titre', 'user_id', 'participants', 'date_creation', 'est_prive']

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

class SujetForumMessagesView(APIView):
    def get(self, request, sujet_id):
        try:
            sujet = sujets_forum.objects.get(sujet_id=sujet_id)
        except sujets_forum.DoesNotExist:
            return Response({"error": "Sujet not found"}, status=status.HTTP_404_NOT_FOUND)

        messages = sujet.messages.all().order_by("-date_message")
        serializer = Messages_forumSerializer(messages, many=True)
        return Response({
            "sujet_id": sujet.sujet_id,
            "titre": sujet.titre,
            "participants": [user.username for user in sujet.participants.all()],
            "messages": serializer.data,
        }, status=status.HTTP_200_OK)







        