from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("pag1", views.pag1, name="f"),
    path("pag2", views.pag2, name="g"),
    path("info", views.info, name="info"),
    path("log", views.log, name="log"),
    path("istoric", views.istoric, name="istoric"),
    path("despre", views.despre, name="despre"),
    re_path(r"^accesare(?P<id>\d{1,})$", views.pagina_accesare, name="pagina_accesare"),
    re_path(r"^pag/(?P<nr>\w{0,})$", views.aduna_numere, name="aduna_numere"),
    path("liste", views.afiseaza_liste, name="liste"),
    re_path(r"^nume_corect/[A-Z][a-z]*(?:-[A-Z][a-z]*){0,1} [A-Z][a-z]*$", views.numara_nume, name="numara_nume"),
    re_path(r"^subsir/(?P<s>\d*[ab]*\d*)$", views.cauta_subsir, name="cauta_subsir"),
    path("categorii", views.afisare_categorii, name="categorii"),
    path("operatii", views.operatii, name="operatii"),
    path("afisare", views.afisare, name="afisare"),
    path("redirectionare", views.redirectionare, name="redirectionare"),

]
