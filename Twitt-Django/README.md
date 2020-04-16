# Mini Twitt #

Aplicativo web basado en twitter, realizado con el Framework Django para afianzar conocimientos en este (ya que apenas incursiono en el), nuestro aplicativo constará de las siguientes caracteristicas

* Caracteristicas generales del sitio

	* Portada mostando twitt's de diversos usarios

	* Posibilidad de realizar Re-Twitt

	* Posibilidad de dar chevere (me gusta) a un Twitt o Re-Twitt

	* Autenticación por mensaje de activación

* Las acciónes que podrá realizar el usuario són

	* Modificación de perfil
	
	* Realizar un Twitt
	
	* Realizar un Re-Twitt
	
	* Reaccionar con 'Chevere' a un Twitt
	
	* Cambiar contraseña
	
	* Visitar perfil de otros usuarios
	
	* Seguir a otros usuarios
	
	* Eliminar cuenta
	
Para la realización de dicho aplicativo primero debe planearse como sera la logica de negocio las cuales en Django son establecidas en las **views** (vistas) que interactuan con el **modelo** del aplicativo el cual define la estructura de la base de datos, por ende realizaremos a continuación el modelado de la base de datos.

Antes de proseguir cabe aclarar que Django es un framework basado en un comportamiento MVT (Model - Views - Template) un poco diferente al modelo MVC ( Model - View - Controller) porque al momento de realizar una peticion desde el Template (Plantilla) lo recibe la 'View' (vista) en la cual se define toda la logica de negocio del aplicativo y esta realiza la consulta en el 'Model' (Modelo), por ultimo realizando el proceso inverso para así lograr el renderizado del Template.

## Modelado Base de Datos ##

Para realizar el modelo debemos mirar el problema los requerimientos, a partir de esto definir las entidades que se establecerán en este y sus relaciones.

Una entidad es la representación de un objeto por así decirlo en una BD (Base de Datos) el cual consta de unos atributos un ejemplo de una entidad seria una **persona** la cual puede tener los atributos **edad, nombre y estatura**.

Dicho lo anterior y meditando los requerimientos del aplicativo defini 2 entidades las cuales son 

**Usuario** 
**Twitt**

Y unas caracteristicas para cada uno

* **Usuario**

	* Nombre de usuario (Unico)
	* Nombre
	* Apellidos
	* Contraseña
	* Correo electronico (Unico)
	
* **Twitt**
	
	* Texto
	* Fecha de creación

* **Seguido**
	
	* Usuario seguidor (Useguidor)
	* Usuario seguido (Useguido)
	
	
Pero viendo mis entidades, Django ya me proporciona una la de usuario la cual se encuentra en su aplicativo preinstalado de autenticación, pero seguire imaginandolo como si lo hiciera desde 0. Para realizar el siguiente paso establecer las relaciones de las entidades y su cardinalidad.

Para aquello pense 1 usuario puede tener N Twitt's y 1 Twitt's puede tener N Usuarios pero claramente 1 de estos seriá el autor del Twitt, Lo cual establece una relación con cardinalidad N - N.

Además de analizarlo de la relación entre 1 seguido y 1 usuario, lo vi de la siguiente manera 1 usuario puede seguir N "seguidos" y 1 seguido solamente puede ser seguido por 1 usuario.

**Nota: este tipo de relaciones entre entidades no es absolutamente optima o correcta pueden existir otras soluciones, si alguno quisiera corregir mi esquema se aceptan todas las criticas**

Como se toda relación con cardinalidad N - N obligatoriamente debe tener una tabla de relación donde las llaves primarias de cada entidad en la relación trasienden como llaves Foráneas en la tabla de relación y en esta tabla se definen los atributos que comparten ambas entidades por la cuan la definire de la siguiente forma

Tabla de relación: 

* **UsTw** 
	* Llave primaria de User (Llave Foránea)
	* Llave primaria de Twitt (Llave Foránea)
	* Propietario (Campo que me indica si el usuario es propietario del Twitt)
	
Pensando en la reacción 'Chevere' del aplicativo como será un aplicativo sencillo consistirá en ser un contador sin guardar la información del usuario que realiza la reacción pero si podria avisar que han reaccionado al aplicativo, por lo anterior añado el atributo **reacción**.

Ya planeado el modelo y las caracteristicas del aplicativo se procede a crear el proyecto.

## Creando proyecto en Django ##

**NOTA: El aplicativo lo realizare en un sistema Linux basado en Ububtu 16.04**

Instalar un entorno virtual es opcional, lo cual consiste en tener un espacio reservado del sistema que funciona de manera "independiente" al sistema operativo local, para mas información observar

https://virtualenv.pypa.io/en/stable/

El entorno virtual lo creare con python 3.5 con el siguiente comando

`$ virtualenv -p /usr/bin/python3.5 Twitt`

Activo el entorno virtual `$ source Twitt/bin/activate`

Instalo Django `$ pip install django`

Creo el proyecto en Django `$ django-admin startproject Twitt`

Lo que me creara el directorio **Twitt** el cual constara de un archivo **manage.py** y el directorio principal del proyecto que consta con el mismo nombre, en el cúal se encontrarán 4 archivos brevemente descritos a continuación

**__init__.py** Archivo para especificación del directorio como un modulo en paquete o modulo en python.

**settings.py** Archivo donde se establecen las configuraciónes en Django.

**urls.py** Archivo donde se establecen las URL'S del aplicativo

**wsgi.py** Archivo que permite la ejecución de un -Web Server Gateway Interface- para la ejecucion del aplicativo en servidores.


## Definicion de Aplicaciones para el Proyecto ##

Como buena practica de programación cada entidad o modelo de un aplicativo deberia ser tratado independiente mente es decir que los metodos de control deben estar separados, por lo anterior he decidido crear 2 aplicaciones en mi proyecto una para el control de usuario y otra para el control de Twitt's.

Creando aplicacion de usuarios `$ django-admin startapp Usuario`

Creando aplicación de Twitt's `$ django-admin startapp Twitts`

Creando aplicacion de seguidos `$ django-admin startapp Seguido`

Los procesos anteriores crearan los respectivos directorios para las aplicaciónes los cuales cuentan con los siguientes archivos y directorios

**__init__.py** Archivo para especificación del directorio como un modulo en paquete o modulo en python.

**admin.py** Archivo para la ejecución del registro en aplicativo por defecto en django admin.

**apps.py** Archivo donde se realiza la declaración del aplicativo.

**models.py** Archivo donde se especifican los modelos.

**test.py** Archivo donde se crean las pruebas de la aplicación.

**views.py** Archivo donde se establecen las vistas.

Ya hemos creado el proyecto y las aplicacions en este provemos si sirve ejecutando el comando `$ python manage.py runserver` en la raíz del proyecto, lo cual nos resulta que el servidor se ejecuta en la dirección 

http://127.0.0.1:8000/

Al ingresar en esta se debe apreciar la siguiente pantalla

![](/capturas/1.png) 

Ademas Django cuenta con un aplicativo de administración el cual no hemos configurado aún pero puede visitarlo con la siguiente dirección

http://127.0.0.1:8000/admin/

Y se podra apreciar

![](/capturas/2.png) 


## Creando Modelos ##

Ahora procedere a establecer los modelos en los aplicativos como ya se han descritos anteriormente, para ellos debo editar el archivo **models.py** en ambos directorios de las aplicaciones.

*Pero antes de ellos registraré la aplicación en el proyecto editando el archivo **settings.py** y su variable **INSTALLED_APPS** en la cual especificare*

![](/capturas/3.png)

Realizando esto quedaria así

### Modelo usuarios ###

![](/capturas/4.png)

### Modelo Twitt ###

![](/capturas/5.png)

### Tabla de relación N-N

![](/capturas/6.png)

**Nota: declarana en el mismo archivo models del aplicativo Twitts**

### Modelo Seguido ###

![](/capturas/7.png)

**Nota: en realidad parece una tabla de relación resultante de una relación N-N de Usuario - Usuario, pero más adelante veré su trabajo y definire si es lo mismo**

## Configurando base de datos en PostgreSQL ##

El ultimo paso a realizar ya despues de tener definidos los modelos es crear sus migraciónes e migrarlas a una base de datos, valga la redundancia, pero para ello es necesario ya tener establecido la configuración de la base de datos en mi caso utilizare **PostgreSQL** ya que pienso utilizar la plataforma **heroku** o **Google Cloud** para desplegar o montar el aplicativo.

### Configurando Conexión con PostgreSQL ##

Para necesitamos de un requerimiento obligatorio el cual consta de un paquete en python denominado **psycopg2**, el cual lo instale con el siguiente comando

`$ pip install psycopg2`

y cree mi archivo **requirements.txt** en el cual instanciare todos los paquetes utilizados en el proyecto, con el comando

`$ pip freeze > requirements.txt`

Ya yo cuento con una base de datos creada llamada **Twitter** por ende procedo a configurar el archivo **settings.py** y su variable **DATABASES** con la siguiente estructura

![](/capturas/8.png)

Por ultimo procedo a crear e migrar las migraciones, valga la redundancia con los siguientes comandos

Creando migraciones `$ python manage.py makemigrations`

Errores

```
ERROR 1

  self.remote_field.through_fields[0] and self.remote_field.through_fields[1]):
TypeError: 'set' object does not support indexing

Por lo que puedo entender el error se debe a lo establecido en la relación ManyToMany en el modelo Twitts con el atributo **through_fields** la cual lo especifique como un diccionario

through_fields={'twittid', 'userid'}

pero este es un conjunto de argumentos por lo cual debo especificarlo de la siguiente manera

through_fields=('twittid', 'userid')

ERROR 2

SystemCheckError: System check identified some issues:

ERRORS:
Seguido.Seguido.Useguido: (fields.E304) Reverse accessor for 'Seguido.Useguido' clashes with reverse accessor for 'Seguido.Useguidor'.
	HINT: Add or change a related_name argument to the definition for 'Seguido.Useguido' or 'Seguido.Useguidor'.
Seguido.Seguido.Useguidor: (fields.E304) Reverse accessor for 'Seguido.Useguidor' clashes with reverse accessor for 'Seguido.Useguido'.
	HINT: Add or change a related_name argument to the definition for 'Seguido.Useguidor' or 'Seguido.Useguido'.
Twitts.Twitts: (models.E014) 'ordering' must be a tuple or list (even if you want to order by only one field).

en el que me especifican claramente un error de "colision" a momento de definir
las 2 restricciones en la tabla seguidos y me sugieren para solucionarlo
establecer un nombre a cada restriccion de la relación.

por ende las defini como

Atributo Useguidor
	related_name="Usuario_que_sigue"

Atributo Useguido
	related_name='Usuario_seguido'
	
ERROR 3

SystemCheckError: System check identified some issues:

ERRORS:
Twitts.Twitts: (models.E014) 'ordering' must be a tuple or list (even if you want to order by only one field).

En este me equivoque tratando al atributo ordening como un conjunto de argumentos definiendolo

ordering = ('-date')

no como una tupla de la siguiente manera

ordering = ['-date']

```
Al realizar la migración la respuesta es
```
Migrations for 'Seguido':
  Seguido/migrations/0001_initial.py
    - Create model Seguido
Migrations for 'Twitts':
  Twitts/migrations/0001_initial.py
    - Create model Twitts
    - Create model UsTw
    - Add field user to twitts
```

Migrando `$ python manage.py migrate`.

Con lo anterior ya tenemos la base de datos configurada.

## Configuración de archivos estaticos y plantillas ##

En esta sección configuraremos las rutas para la identificación de los archivos estaticos y las plantillas de mi proyecto las cuales quiero definirla en los directorios **templates** y **static** posicionados en la raiz de mi proyecto

Creando carpeta templates `$ mkdir templates`

Creando carpeta static `$ mkdir static`

Es necesario aclarar las funciones de lo archivos contenidos en cada carpeta

* **Templates:** son archivos de tipo html que se renderizaran para mostrar la información suministrada por una vista (views).

* **Static:** son archivos de cualquier tipo se caracterizan por no ser manipulados por las vistas pero si utilizados en las plantillas (templates) como pueden ser imagenes, archivos css, js.

Tambien existen los archivos de media que son contenidos dinamicos por asi decirlos como videos pero por el momento no los usaremos, pero el directorio para estos lleva el nombre de **media**.

Por ultimo registraremos la ruta de los archivos estaticos modificando 1 variable y añadiendo 1 en el archivo **settings.py** de nuestro aplicativo las cuales son

TEMPLATES (modificada)

STATICFILES_DIRS (añadida)

En la variable TEMPLATES la pondremos de la siguiente forma

```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```
El atributo de la variable modificado fue **DIRS** en el cual se le especifica que detectara la carpeta que se encuentre en la ruta base (ruta del proyecto), la cual es definida por la variable **BASE_DIR**

Creación de variable STATICFILES_DIRS la que se pondra de la siguiente forma

```
STATICFILES_DIRS=(os.path.join(BASE_DIR, 'static'),)
```


## Creando autenticación ##

Como se ha planteado ya anteriormente para la creación de la autenticacion y todo referente al registro utilizaremo una aplicación en django **django redux registration** su documentación se puede encontrar en 

https://django-registration-redux.readthedocs.io/en/latest/

Para la utilización de django-redux-registration ya este cuenta con unas plantillas (templates) establecidas, pero en mi caso las quise personalizar por lo cual

* Cree dentro del directorio **templates** la carpeta **registration**
* Dentro de la carpeta **registration** estableci todas las plantillas que queria editar por mi cuenta 
* Utilice **Bootstrap** para la creación de estas por ende para la correcta utilización realice

	* Cree en el directorio **static** anexe las carpetas **css, js, fonts** proporcionadas por bootstrap
	
Ya establecidas las 16 plantillas a utilizar las que se pueden caracterizar o seccionar de la siguiente forma

* **Plantillas para activación de cuentaa**

* **Plantillas para registro de usuario**

* **Plantilla para cambio de contraseña**

* **Plantilla para restauración de contraseña**

No entrare en profundo detalle, pero con el nombre de las plantillas supongo que harán la relación con lo ya dicho.

Por ultimo registraremos la aplicación django redux en nuestro proyecto, anexando 'registration' y 'crispy_forms' a nuestra variable INSTALLED_APPS en el archivo settings.py

```
INSTALLED_APPS = [
    'Twitts.apps.TwittsConfig',
    'Usuario.apps.UsuarioConfig',
    'Seguido.apps.SeguidoConfig',
    'registration',
    'crispy_forms',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

Instalamos los paquetes 

Intalando Django redux `$ pip install django-registration-redux`

Intalando crispy para el manejo de formularios `$ pip install --upgrade django-crispy-forms`

Documentacion de crispy http://django-crispy-forms.readthedocs.io/

### Registrando urls por defecto ###

Modificamos el archivo urls.py del directorio del proyecto, dejandolo de la siguiente forma

```
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('registration.backends.default.urls')),
]
```
Por ultimo probamos nuestra aplicacion

* Migramos los cambios

	* `$ python manage.py makemigrations`
`
	* `$ python manage.py migrate`
	
* Ejecutando el servidor `$ python manage.py runserver`

Por erro las plantillas instancian algunas vistas que aun no tengo y me aparece 

![](/capturas/9.png)

Pero se sabe que se envia la petición.

## Configurando URL's y View's en Usuario ##

Ya tengo las vistas definidas al igual que las urls, para esto ultimo se debe crear el archivo **urls.py** en el directorio de la aplicación.

En el commit correspondiente encontraran los cambios y el codigo comentado

Los temas tratados son 

* Generacion de plantillas para usuario
* Personalización de formulario de registro
* Personalización de URL's para registro
* Creación de vistas para usuarios
* Creación de vista para Twitt
* Configuración de email

![](/capturas/10.png)