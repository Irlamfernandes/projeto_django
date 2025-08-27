from django.db import models

class Filmes(models.Model):
    titulo = models.CharField(verbose_name="Titulo",null=True, blank=True, max_length=255)
    sinopse = models.TextField(verbose_name="Sinopse",null=True, blank=True, max_length=1000)
    descricao = models.TextField(verbose_name="Descricao",null=True, blank=True, max_length=2000)
    capa = models.URLField(verbose_name="URL da capa",null=True,blank=True)
    id_tmdb = models.IntegerField(verbose_name="ID no TMDB")

class Streaming(models.Model):
    nome = models.CharField(verbose_name="Nome do streaming",max_length=100)
    url = models.URLField(verbose_name="URL do streaming")