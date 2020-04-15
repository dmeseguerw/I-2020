import os
import subprocess
import string
import glob
import statistics #para obtener desv estandar y promedio
import csv
import matplotlib.pyplot as plt
from AudiosDD import AudiosDD
import itertools
from zipfile import ZipFile 

class Create:
    inst_list = []
    sil = [' 3.0 ', ' 5.0 ', ' 2.0 ']
    snd = [' 0.5 ', ' 0.9 ', ' 1.2 ']
    th = [' 1% ', ' 1.5% ',' 0.9% ' ]
    param_list = []

    def unzip(self, fn):
        file_name = fn
        with ZipFile(file_name, 'r') as zip:
            zip.extractall()

    def all_param(self): #Crea una lista con todas las posibles combinaciones entre los parámetros adjuntos en las listas sil, snd y th
        print("Obteniendo todas las posibles combinaciones de parámetros...")
        new_list = [self.sil, self.snd, self.th]
        self.param_list = list(itertools.product(*new_list))
        print("Combinaciones obtenidas!\n")


    def create_instances(self): #Crea todas las instancias de la clase AudiosDD para cada set de parámetros distintos.
        for i in range(0,len(self.param_list)):
            print("Cargando Prueba " + str(i) + "...\n")
            self.inst_list.append(AudiosDD(i, self.param_list[i][0], self.param_list[i][1], self.param_list[i][2]))
            self.inst_list[i].segment_audio()
    
    def txt_to_csv(self): # Obtengo un archivo .csv para poder organizar los datos
        print("Creando archivo csv...")
        f = open("datos.txt",'r')
        data = f.readlines()
        for i in range(0,len(data)):
            data[i] = data[i].split()
        f.close()
        
        f_csv = open("datos.csv", 'w')
        with f_csv:
            writer = csv.writer(f_csv)
            writer.writerows(data)

        f_csv.close()
        print("Archivo csv finalizado!\n")