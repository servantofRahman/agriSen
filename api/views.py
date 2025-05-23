from django.shortcuts import render
from django.db.models import Q
from rest_framework import serializers
from rest_framework import generics
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.
class LoginView(APIView):
    """Allows users to log in and receive a JWT token."""
    
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if not user:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        
        return Response({
            "message": "Login successful!",
            "username": user.username,
            "role": user.type_utilisateur,
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh)
        }, status=status.HTTP_200_OK)


class RegisterView(APIView):
    """Allows new users (Agriculteurs, Syndics, etc.) to register and get a JWT token."""

    def post(self, request):
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        email = request.data.get("email")
        username = request.data.get("username")
        password = request.data.get("password")
        type_utilisateur = request.data.get("type_utilisateur")  # updated field

        if not all([first_name, last_name, email, username, password, type_utilisateur]):
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        valid_roles = [choice[0] for choice in utilisateurs.choix]
        if type_utilisateur not in valid_roles:
            return Response({"error": f"Invalid user type. Must be one of: {', '.join(valid_roles)}"}, status=status.HTTP_400_BAD_REQUEST)

        if utilisateurs.objects.filter(username=username).exists():
            return Response({"error": "Username already taken."}, status=status.HTTP_400_BAD_REQUEST)

        if utilisateurs.objects.filter(email=email).exists():
            return Response({"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        user = utilisateurs.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=password,
            type_utilisateur=type_utilisateur
        )

        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "User registered successfully!",
            "username": user.username,
            "type_utilisateur": user.type_utilisateur,
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh)
        }, status=status.HTTP_201_CREATED)

class SujetForumList(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SujetForumSerializer

    def get_queryset(self):
        user = self.request.user
        return sujets_forum.objects.filter(
        est_prive=True
    ).filter(
        Q(user_id=user.id) | Q(participants=user)
    ).distinct()

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

class SujetForumListPublic(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SujetForumSerializer

    def get_queryset(self):
        data = sujets_forum.objects.filter(est_prive=False).all()[:10]
        return data
    
    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

class SujetForumDetails(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = sujets_forum.objects.all()
    serializer_class = SujetForumSerializer
    lookup_field = 'pk'

class Messages_forumListCreateView(generics.ListCreateAPIView):
    queryset = messages_forum.objects.all()
    serializer_class = Messages_forumSerializer

class Messages_forumRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = messages_forum.objects.all()
    serializer_class = Messages_forumSerializer
    lookup_field = 'pk'





