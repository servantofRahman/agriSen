from django.db import models
import uuid 
from django.contrib.auth.models import AbstractUser

# Create your models here.
class utilisateurs(AbstractUser):
    choix = [('agriculteur', 'Agriculteur'), ('syndic', 'Syndic'), ('utilisateur', 'Utilisateur'), ('admin', 'Admin')]
    type_utilisateur = models.CharField(max_length = 100, choices = choix, default = 'utilisateur')

class sujets_forum(models.Model):
    sujet_id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    titre = models.CharField(max_length=255)
    user_id = models.ForeignKey(utilisateurs, on_delete = models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add= True)
    est_prive = models.BooleanField(default = False)

class messages_forum(models.Model):
    message_id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    sujet_id = models.ForeignKey(sujets_forum, on_delete = models.CASCADE)
    user_id = models.ForeignKey(utilisateurs, on_delete = models.CASCADE)
    contenu = models.TextField(),
    date_message = models.DateTimeField(auto_now_add = True)

class publications(models.Model):
    publication_id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    user_id = models.ForeignKey(utilisateurs, on_delete = models.CASCADE)
    contenu = models.TextField()
    image = models.FileField(upload_to="publication-images/")
    date_publication = models.DateTimeField(auto_now_add = True)
    region = models.CharField(max_length = 100)
    culture_associee = models.CharField(max_length = 100)

class commentaires(models.Model):
    commentaire_id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    publication_id = models.ForeignKey(publications, on_delete = models.CASCADE)
    user_id = models.ForeignKey(utilisateurs, on_delete = models.CASCADE)
    contenu = models.TextField()
    date_commentaire = models.DateTimeField(auto_now_add = True)

class messages_privées(models.Model):
    message_id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    expediteur_id = models.ForeignKey(utilisateurs, on_delete = models.CASCADE, related_name="expediteur")
    destinataire_id = models.ForeignKey(utilisateurs, on_delete = models.CASCADE)
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add = True)
    lu = models.BooleanField(default = False)

class agriculteurs(models.Model):
    agriculteur_id = models.UUIDField(primary_key = True)
    user_id = models.ForeignKey(utilisateurs, on_delete = models.CASCADE)
    region = models.CharField(max_length = 100)
    commune = models.CharField(max_length = 10)
    telephone = models.CharField(max_length = 20)
    photo_profil = models.FileField(upload_to = "photo_profile/")
    bio = models.TextField()

class cultures(models.Model):
    culture_id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    nom_culture = models.CharField(max_length = 100)
    region = models.CharField(max_length = 100)
    saison = models.CharField(max_length = 50)
    besoins_eau = models.CharField(max_length = 100)
    conseils = models.TextField()
    fichier_technique = models.FileField(upload_to = "fichier_technique/")

class meteo (models.Model):
    meteo_id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    region = models.CharField(max_length = 100)
    temperature = models.FloatField()
    humidite = models.FloatField()
    vent = models.FloatField()
    date_enregistrement = models.DateTimeField(auto_now_add = True)

class stocks (models.Model):
    stock_id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    agriculteur_id = models.ForeignKey(agriculteurs, on_delete = models.CASCADE)
    nom_produit = models.CharField(max_length = 100)
    quantite = models.IntegerField()
    unite = models.CharField(max_length = 20)
    prix_unitaire = models.IntegerField()
    date_ajout = models.DateTimeField(auto_now_add = True)

class ventes (models.Model):
    vente_id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    stock_id = models.ForeignKey(stocks, on_delete = models.CASCADE)
    quantite_vendue = models.IntegerField()
    date_vente = models.DateTimeField(auto_now_add = True)
    acheteur_id = models.ForeignKey(utilisateurs, on_delete = models.CASCADE)

