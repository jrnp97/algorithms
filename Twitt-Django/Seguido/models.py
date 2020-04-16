# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#Importando modelo Usuario

from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Seguido(models.Model):
    """
    Modelo en el cual se especifica la relacion 1 - N entre un usuario y un 'seguido'
    """
    Useguidor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="Usuario_que_sigue"
    )

    Useguido = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='Usuario_seguido'
    )
