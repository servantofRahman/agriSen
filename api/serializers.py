# from .views import *
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.contrib.auth import get_user_model

User = get_user_model()

class SujetForumSerializer(serializers.ModelSerializer):
    participants = serializers.ListField(
        child=serializers.EmailField(),
        write_only=True,
        required=False
    )
    participant_emails = serializers.SerializerMethodField(read_only=True)
    message_count = serializers.SerializerMethodField(read_only=True)
    author_username = serializers.SerializerMethodField(read_only=True)  # ✅

    class Meta:
        model = sujets_forum
        fields = [
            'sujet_id', 'titre', 'participants', 'participant_emails',
            'date_creation', 'est_prive', 'message_count', 'author_username' 
        ]
        read_only_fields = ['user_id']

    def validate(self, data):
        est_prive = data.get('est_prive')
        participants = data.get('participants')

        if est_prive and not participants:
            raise serializers.ValidationError({
                'participants': 'Participants are required when est_prive is True.'
            })
        return data

    def create(self, validated_data):
        emails = validated_data.pop('participants', [])
        users = get_user_model().objects.filter(email__in=emails)
        sujet = sujets_forum.objects.create(**validated_data)
        if users:
            sujet.participants.set(users)
        return sujet

    def get_participant_emails(self, obj):
        return [user.email for user in obj.participants.all()]

    def get_message_count(self, obj):
        return obj.messages.count()

    def get_author_username(self, obj):
        if not obj.est_prive and obj.user_id:
            return obj.user_id.username
        return None

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

        messages = sujet.messages.all().order_by("date_message")
        serializer = Messages_forumSerializer(messages, many=True)
        return Response({
            "sujet_id": sujet.sujet_id,
            "titre": sujet.titre,
            "participants": [user.username for user in sujet.participants.all()],
            "messages": serializer.data,
        }, status=status.HTTP_200_OK)







        
