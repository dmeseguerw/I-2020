# Automatic Audio Segmentation System
## Daniel Meseguer Wong

El siguiente programa consiste en un sistema automatizado de segmentación de audios de larga duración. Se utiliza Tkinter para implementar una interfaz gráfica.

### Prerequisites:

###### -SoX
###### -python3
###### -python3-matplotlib
###### -python3-numpy
###### -python3-pil
###### -python3-tk
###### -python3-pandas

### Installing and running:

##### Se encuentran 4 archivos de Python:
######    **Segmentation.py** contiene una clase Segmentation con todos los métodos para la segmentación y obtención de datos.
######    **Results.py** contiene una clase Results con los métodos para obtener datos y gráficos de las segmentaciones.
######    **Automatic.py** contiene una clase Automatic que ejecuta todas las posibles combinaciones de parámetros dentro de cierto rango, y crea objetos de Segmentation
######    **test.py** contiene las pruebas a realizar para ejecutar el programa


##### Se cuenta con un Makefile, por lo que se recomienda instalar en la terminal el comando make mediante:
######                *sudo apt-get install make*

##### Posibles comandos con el Makefile:
######    *make install_dep : instala todas las dependencias utilizadas por el programa.*
######    *make app : abre la aplicación desarrollada con Tkinter.*
######   *make clean : limpia los directorios utilizados por la aplicación*
######    *make all : ejecuta en orden los comandos anteriores*

##### Si se desea ejecutar la aplicación sin utilizar el makefile:
######    *python3 App.py*



