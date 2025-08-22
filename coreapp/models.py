from django.db import models

# Create your models here.

class Filmes(models.Model):
    titulo = models.CharField(max_length=255)
    sinopse = models.TextField()
    capa = models.URLField()
    id_tmdb = models.IntegerField()

class Streaming(models.Model):
    nome = models.CharField(max_length=100)
    url = models.URLField()