from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(utilisateurs)
admin.site.register(sujets_forum)
admin.site.register(messages_forum)
