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
from scipy.io import wavfile as wav
import pandas as pd

class Create:
    inst_list = []
    sil = [' 3.0 ', ' 1.0 ']
    snd = [' 0.5 ', ' 0.25 ']
    th = [' 1% ', ' 1.5% ']
    param_list = []
    F_Dict = {}
    Values = pd.DataFrame()

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
        dict_list = []
        key_list = []
        empty_df = pd.DataFrame()
        for i in range(0,len(self.param_list)):
            print("Cargando Prueba " + str(i) + "...\n")
            self.inst_list.append(AudiosDD(i, self.param_list[i][0], self.param_list[i][1], self.param_list[i][2]))
            self.inst_list[i].segment_audio()

            # s = pd.Series(self.inst_list[i].Dict, name = 'Duracion')
            # s.index.name = 'Nombre'
            # s.reset_index()

            # current_df = pd.DataFrame.from_dict(self.inst_list[i].Dict, orient = 'index', columns=['Name','Duration'])
            current_df = pd.DataFrame(list(self.inst_list[i].Dict.iteritems()), columns = ['Name','Duration'])
            print(current_df)
            # current_df = df.set_index('Prueba'+str(self.inst_list[i].inst_number))
            # self.Values.append(current_df)
            # self.Values.append(empty_df)
            # print(current_df)

        # print(self.Values)
    def txt_to_csv(self): # Obtengo un archivo .csv para poder organizar los datos
        print("Creando archivo csv...")
        f = open("datos.txt",'r')
        data = f.readlines()
        for i in range(0,len(data)):
            data[i] = data[i].split()
        f.close()

        summary = open("summary.txt",'r')
        sum_data = summary.readlines()
        for i in range(0,len(sum_data)):
            sum_data[i] = sum_data[i].split()
        summary.close()
        
        f_csv = open("datos.csv", 'w')
        with f_csv:
            writer = csv.writer(f_csv)
            writer.writerows(data)

        sum_csv = open("sum.csv","w")
        with sum_csv:
            writer = csv.writer(sum_csv)
            writer.writerows(sum_data)
            

        
        sum_csv.close()
        f_csv.close()
        print("Archivo csv finalizado!\n")