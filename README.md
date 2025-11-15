Este proyecto es una página web para una inmobiliaria. Posee 3 aplicaciones funcionando (Inmobiliaria, Propuedades y Usuarios), y una cuarta que es sólo un bosquejo (Tasaciones), ya que esta última excede a los requisitos de este curso. La aplicación padre, desde donde corre el index y se realizan las herencias, es Inmobiliaria: en su template podemos ver el navbar, un cuerpo principal, y un pie de página. La aplicación Usuario sirve para gestionar los usuarios, donde diferencié 3 tipos (Cliente, Agente y Tasador), para poder definir límites de acceso. Los clientes sólo pueden ver las propiedades y crear su perfil (la idea sería que también puedan realizar consultas o pedir tasaciones, pero estas dos aplicaciones no las desarrollé completamente, para no extralimitarme a los contenidos del curos). Los Agentes, en cambio, pueden modificar el contenido de las propiedades publicadas, pero para poder crear un perfil se solicita una validación extra, para la que hay que introducir el código VALIDAR2025. Los tasador no fueron introducidos, pero serían los encargados de responder a las demandas de tasaciones, y también requerirían una validación para su creación. También está el superuser capaz de editar todo el contenido del sitio desde la app Admin. Finalmente, tenemos la app Propiedades, donde se pueden crear, leer, modificar o eliminar las propiedades que se ofrecen en la inmobiliaria. 


En el siguiente Link se encuentra publicado un video donde muestro el proyecto en funcionamiento:
https://drive.google.com/drive/folders/1yIDdTe1I4l7r7pPYUqcplEp6QF5V88NS?usp=sharing


Para ejecutar este proyecto debes seguir la siguiente secuencia:

1-->  Descargar el proyecto del siguiente link de github: https://github.com/FCasalins/Proyecto-Python-Casalins-Federico-78130.
2-->  Crear la carpeta del proyecto. Desde esa carpeta abrir GitBash haciendo clic derecho, y escribir git clone y pegar el enlace de arriba, y cerrar la línea de comando con espacio+punto.
3-->  En VSC abrir la carpeta del proyecto.
4-->  Crear un entorno virtual: Primero instalar la librería virtualenv usando pip install virtualenv. Luego ejecutar "python -m venv entorno_virtual" para crear el entorno virtual propiamente dicho. Finalmente, activarlo con el comando "entorno_virutal\Scripts\activate".
5-->  Instalar los requeriments con el comando "pip install -r requirements.txt".
6-->  Aplicar las migraciones con "python manage.py migrate".
7-->  Crear un superusuario con "python manage.py createsuperuser".
8-->  Correr el servidor con "python manage.py runserver".   