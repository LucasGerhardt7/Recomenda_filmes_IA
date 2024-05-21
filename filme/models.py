from django.db import models

# Create your models here.


class Usuario(models.Model):
    idUsuario = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=150, blank=True, null=True)
    data_nascimento = models.DateField()
    genero = models.CharField(max_length=150, blank=True, null=True)
    

class Categoria(models.Model):
    idCategoria = models.AutoField(primary_key=True)
    nomeCategoria = models.CharField(max_length=100)

class Filme(models.Model):
    idFilme = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=200, blank=False, null=False)
    classificacao = models.IntegerField()
    lancamento = models.DateField()
    avaliacao = models.FloatField(blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, blank=True, null=True)


class FilmeRecomedado(models.Model):
    idFilmeRecomendado = models.AutoField(primary_key=True)
    idFilme = models.ForeignKey(Filme, on_delete=models.SET_NULL, blank=True, null=True)
    idUsuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, blank=True, null=True)
    