from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(sujets_forum)
admin.site.register(messages_forum)
admin.site.register(publications)
admin.site.register(commentaires)
admin.site.register(messages_privées)
admin.site.register(agriculteurs)
admin.site.register(stocks)
admin.site.register(ventes)
admin.site.register(meteo)
admin.site.register(cultures)