from django.db import models
#importando modelo de usuario en aplicacion auth
from django.contrib.auth.models import User

# Create your models here.


class Twitts(models.Model):
    """
    Clase para la definicion de tabla Twitt que abarcara toda la siguiente informacion acerca de un twitt
    * Texto del twitt (lo que se expresa en el)
    * Fecha de creacion del Twitt
    """

    #Definiedno atributo que almacenara el texto del twitt con un maximo de 250 caracteres y su valor no podra ser nulo
    texto = models.CharField(max_length=250, null=False)
    #Definiendo atributo que almacenara la fecha en que se realizo el twitt
    date = models.DateTimeField(auto_now_add=False)
    #Definiendo atributo el cual contara las reacciones en el twitt
    chevere = models.IntegerField()

    #Definiendo instancia a la tabla para la relacion N-N
    user = models.ManyToManyField(
        User,
        through='UsTw',
        through_fields=('twittid', 'userid'),
    )

    #Defineindo metodo para ver la informacion de la clase
    def __str__(self):
        return ('{} {} {}'.format(self.texto, self.date, self.chevere))


    class Meta:
        #Definiendo restriccion para el ordenamiento de los datos de manera Desendente con su fecha
        ordering = ['-date']

#Tabla de la relacion N - N
class UsTw(models.Model):
    """
    Clase que define estructura de la tabla de relacion entre Usuarios y Twitts la cual es de N - N
    que constara de el atributo extra 'propietario' el cual define el propietario del Twitt.
    """

    #Definiendo llaves foranea de usuario
    userid = models.ForeignKey(
        User, #modelo con el cual se establece la restriccion
        on_delete=models.CASCADE, #Especificando metodo de accion al momento de realizar un borrado en la DB
    )

    #Defienidno llave foranea de twitter
    twittid = models.ForeignKey(
        Twitts,
        on_delete=models.CASCADE,
    )

    #Definiendo atributo en comun de las 2 entidades, solamente podra tener los valores 'True' y 'False'
    propietario = models.BooleanField()
