from django.db import models

class Categorie(models.Model):
    nume = models.CharField(max_length=200, unique=True)
    descriere = models.TextField(null=True)
    culoare = models.CharField(max_length=100, null=True)
    sigla = models.ImageField(upload_to='sigle/')
    data_creare = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return f"{self.nume}: {self.descriere}, {self.culoare}"

