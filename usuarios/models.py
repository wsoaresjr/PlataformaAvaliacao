# usuarios/models.py
import hashlib
from django.db import models

class Usuario(models.Model):
    GRUPOS_CHOICES = [
        ('Administradores', 'Administradores'),
        ('Estudantes', 'Estudantes'),
    ]

    CodUsuario = models.AutoField(primary_key=True)
    Nome = models.CharField(max_length=100)
    Username = models.CharField(max_length=50, unique=True)
    Senha = models.CharField(max_length=256)  # Aumenta o tamanho para armazenar hash
    Grupo = models.CharField(max_length=15, choices=GRUPOS_CHOICES)

    def set_password(self, raw_password):
        self.Senha = hashlib.sha256(raw_password.encode()).hexdigest()

    def check_password(self, raw_password):
        return self.Senha == hashlib.sha256(raw_password.encode()).hexdigest()

    def __str__(self):
        return self.Nome





from django.db import models
from usuarios.models import Usuario

class Resultado(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='resultados')
    respostas = models.JSONField()
    acertos = models.IntegerField()
    percentual_acertos = models.FloatField()
    data_inicio = models.DateTimeField()  # Novo campo
    data_fim = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Resultado de {self.usuario.Nome} em {self.data_fim}'
