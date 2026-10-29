from django.contrib import admin
from .models import Categorie

admin.site.register(Categorie)

admin.site.site_header = "Panou de Administrare Site"
admin.site.site_title = "Admin Site"
admin.site.index_title = "Bine ai venit în panoul de administrare"

