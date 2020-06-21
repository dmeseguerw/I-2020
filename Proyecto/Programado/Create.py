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
import pandas as pd
import numpy as np

class Create:
    def __init__(self, file_name, silence_rng, silence_step, sound_rng, sound_step, th_rng, th_step):
        self.file_name = file_name
        self.sil = [float(i) for i in silence_rng]
        self.snd = [float(i) for i in sound_rng]
        self.th =  [float(i) for i in th_rng]
        self.sil_step = silence_step
        self.snd_step = sound_step
        self.th_step = th_step
        self.inst_list = []
        self.param_list = []
        self.F_Dict = {}
        self.Values=pd.DataFrame(columns = ['Name','Duration'])
        self.empty = pd.DataFrame()
        self.df = pd.DataFrame(columns = ['STD','Av_Duration'])

    def get_parameters(self):
        new_sil = []
        new_snd = []
        n_th = []

        for i in np.arange(self.sil[0], self.sil[1]+self.sil_step, self.sil_step): 
            new_sil.append(str(round(i,1)))
        for i in np.arange(self.snd[0], self.snd[1]+self.snd_step, self.snd_step):
            new_snd.append(str(round(i, 1)))
        for i in np.arange(self.th[0], self.th[1] + self.th_step, self.th_step):
            n_th.append(str(round(i,1)))

        new_th = []
        for i in range(0,len(n_th)):
            new_th.append(n_th[i] + "%")
            
        self.sil = new_sil
        self.snd = new_snd
        self.th = new_th



    # def unzip(self, fn):
    #     file_name = fn
    #     with ZipFile(file_name, 'r') as zip:
    #         zip.extractall()

    def all_param(self): #Crea una lista con todas las posibles combinaciones entre los parámetros adjuntos en las listas sil, snd y th
        print("Obteniendo todas las posibles combinaciones de parámetros...")
        new_list = [self.sil, self.snd, self.th]
        self.param_list = list(itertools.product(*new_list))
        print(str(len(self.param_list)) + " combinaciones obtenidas!\n")
        # print(self.param_list)


    def create_instances(self): #Crea todas las instancias de la clase AudiosDD para cada set de parámetros distintos.
        serie = pd.Series()
        st_dev = []
        av_dur = []
        for i in range(0,len(self.param_list)):
            print("Cargando Prueba " + str(i) + "...\n")
            self.inst_list.append(AudiosDD(self.file_name, i, self.param_list[i][0], self.param_list[i][1], self.param_list[i][2]))
            self.inst_list[i].segment_audio()
            self.inst_list[i].delete_audio()

            # Este bloque es para crear el dataframe de todas las duraciones de todas las pruebas
            keys = list(self.inst_list[i].Dict.keys())
            values = list(self.inst_list[i].Dict.values())
            self.Values = self.Values.append(pd.Series(name='Prueba'+str(self.inst_list[i].inst_number)))
            self.Values = self.Values.append(pd.DataFrame(list(zip(keys,values)), columns = ['Name','Duration']))

            # Este bloque es para crear el dataframe de la duracion promedio y desviacion estandar de cada prueba
            st_dev.append(self.inst_list[i].desv)
            av_dur.append(self.inst_list[i].av)
            p = pd.DataFrame({"STD":[st_dev[i]], "Av_Duration":[av_dur[i]]})
            self.df = self.df.append(p, ignore_index = True)
            self.df.index.rename('Test', inplace=True)

        # Este bloque agrega al dataframe los valores maximos y minimos de duracion promedio y desviacion estandar
        self.df.loc[0, 'MAX_Dur'] = max(av_dur)
        self.df.loc[0, 'MIN_Dur'] = min(av_dur)
        self.df.loc[0, 'MAX_STD'] = max(st_dev)
        self.df.loc[0, 'MIN_STD'] = min(st_dev)


        if (os.path.exists("./CSV_Files") == False):
            os.system("mkdir CSV_Files")

        self.df.to_csv("./CSV_Files/Summary.csv")
        self.Values.to_csv("./CSV_Files/Values.csv")

    def plot_av_durations(self):

        names = list(range(0,len(self.inst_list)))
        values = self.df['Av_Duration'].tolist()
        plt.bar(names,values)
        plt.title("Duración promedio de las pruebas")
        plt.xlabel("Prueba")
        plt.ylabel("Tiempo (s)")
        plt.xticks(np.arange(0, len(self.inst_list), 1))
        if (os.path.exists("./Images_Global") == False):
            os.system("mkdir Images_Global")

        plt.savefig("./Images_Global/Plot_Av_Dur.png")
        plt.clf()

    def plot_stds(self):
        names = list(range(0,len(self.inst_list)))
        values = self.df['STD'].tolist()
        plt.bar(names,values)
        plt.title("Desviacion estandar de las pruebas")
        plt.xlabel("Prueba")
        plt.ylabel("Tiempo (s)")
        plt.xticks(np.arange(0, len(self.inst_list), 1))
        if (os.path.exists("./Images_Global") == False):
            os.system("mkdir Images_Global")

        plt.savefig("./Images_Global/STD.png")

        plt.clf()