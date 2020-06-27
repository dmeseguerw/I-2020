#!/usr/bin/python
import os
import string
from Segmentation import Segmentation
import itertools
import pandas as pd
import numpy as np
from Results import Results

class Automatic:
    
    def __init__(self, file_name, silence_rng, sound_rng, th_rng):
        self.file_name = file_name
        self.silence_param = [float(i) for i in silence_rng]
        self.sound_param = [float(i) for i in sound_rng]
        self.threshold_param =  [float(i) for i in th_rng]
        self.inst_list = []
        self.all_combinations = []
        self.Durations_DF=pd.DataFrame(columns = ['Name','Duration'])
        self.Summary_DF = pd.DataFrame(columns = ['STD','Av_Duration'])

    def get_parameters(self):
        new_sil = []
        new_snd = []
        n_th = []

        for i in np.arange(self.silence_param[0], self.silence_param[1]+self.silence_param[2], self.silence_param[2]): 
            new_sil.append(str(round(i,1)))
        for i in np.arange(self.sound_param[0], self.sound_param[1]+self.sound_param[2], self.sound_param[2]):
            new_snd.append(str(round(i, 1)))
        for i in np.arange(self.threshold_param[0], self.threshold_param[1] + self.threshold_param[2], self.threshold_param[2]):
            n_th.append(str(round(i,1)))

        new_th = []
        for i in range(0,len(n_th)):
            new_th.append(n_th[i] + "%")
            
        self.silence_param = new_sil
        self.sound_param = new_snd
        self.threshold_param = new_th


    def all_param(self): #Crea una lista con todas las posibles combinaciones entre los parámetros adjuntos en las listas sil, snd y th
        print("Obteniendo todas las posibles combinaciones de parámetros...")
        new_list = [self.silence_param, self.sound_param, self.threshold_param]
        self.all_combinations = list(itertools.product(*new_list))
        print(str(len(self.all_combinations)) + " combinaciones obtenidas!\n")
        # print(self.all_combinations)

    def create_instances(self): #Crea todas las instancias de la clase Segmentation para cada set de parámetros distintos.
        st_dev = []
        av_dur = []
        for i in range(0,len(self.all_combinations)):
            print("Cargando Prueba " + str(i) + "...\n")
            
            self.inst_list.append(Segmentation(i, self.all_combinations[i][0], self.all_combinations[i][1], self.all_combinations[i][2]))
            self.inst_list[i].segment_audio(self.file_name)
            self.inst_list[i].get_durations()
            
            lista_dur = self.inst_list[i].durations_list
            self.inst_list[i].std_dev = Results().std_dev(lista_dur)
            self.inst_list[i].average = Results().average(lista_dur)

            Results().plot_durations(lista_dur, self.inst_list[i].inst_number)

            self.inst_list[i].delete_audio()

            # Este bloque es para crear el dataframe de todas las duraciones de todas las pruebas
            self.Durations_DF = Results().get_durations_df(self.inst_list[i], self.Durations_DF)

            # Este bloque es para crear el dataframe de la duracion promedio y desviacion estandar de cada prueba
            
            st_dev.append(self.inst_list[i].std_dev)
            av_dur.append(self.inst_list[i].average)

            self.Summary_DF = Results().get_summary_df(self.inst_list[i], st_dev, av_dur, i, self.Summary_DF)

        # Este bloque agrega al dataframe los valores maximos y minimos de duracion promedio y desviacion estandar
        # self.Summary_DF.loc[0, 'MAX_Dur'] = max(av_dur)
        # self.Summary_DF.loc[0, 'MIN_Dur'] = min(av_dur)
        # self.Summary_DF.loc[0, 'MAX_STD'] = max(st_dev)
        # self.Summary_DF.loc[0, 'MIN_STD'] = min(st_dev)


        Results().create_CSV(self.Summary_DF, self.Durations_DF)

    