from django.db import models
import uuid 
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class utilisateurs(AbstractUser):
    choix = [('agriculteur', 'Agriculteur'), ('syndic', 'Syndic'), ('utilisateur', 'Utilisateur'), ('admin', 'Admin')]
    type_utilisateur = models.CharField(max_length = 100, choices = choix, default = 'utilisateur')

class sujets_forum(models.Model):
    sujet_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titre = models.CharField(max_length=255)
    user_id = models.ForeignKey(utilisateurs, on_delete=models.CASCADE)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="forum_sujets")
    date_creation = models.DateTimeField(auto_now_add=True)
    est_prive = models.BooleanField(default=False)

class messages_forum(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sujet_id = models.ForeignKey(sujets_forum, on_delete=models.CASCADE, related_name="messages")
    user_id = models.ForeignKey(utilisateurs, on_delete=models.CASCADE, null=True, blank=True)
    contenu = models.TextField()
    date_message = models.DateTimeField(auto_now_add=True)
    audio = models.FileField(upload_to='messages_audio/', null=True, blank=True)



