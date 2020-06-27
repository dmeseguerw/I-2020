#!/usr/bin/python
import os
import subprocess
import string
import statistics #para obtener desv estandar
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class Results:

    def std_dev(self, lista_dur): #Obtengo la desviacion estandar de las duraciones de los segmentos
        print("         Obteniendo desviación estándar...")
        lista = lista_dur  
        desv = round(statistics.pstdev(lista),2)
        print("         Desviación estándar obtenida y guardada!\n")
        return desv
    
    def average(self, lista_dur): #Obtengo el promedio de duracion de los segmentos
        print("         Obteniendo duración promedio...")
        av = round(statistics.mean(lista_dur),2)
        print("         Duración promedio obtenida y guardada!\n")
        return av

    def plot_durations(self, lista_dur, inst_number): #Obtengo una grafica que muestra en comparacion todas las duraciones de los segmentos
        print("         Obteniendo gráfica...")
        values = lista_dur
        names = list(range(0,len(lista_dur)))
        plt.bar(names,values, color="#216583")
        plt.title("Duración de los audios segmentados")
        plt.xlabel("Audio")
        plt.ylabel("Tiempo (s)")
        plt.xticks(np.arange(0, len(lista_dur), 1))
        image_name = 'test' + str(inst_number) + '.png'

        if (os.path.exists("./Images")==False):
            os.system("mkdir Images")

        plt.savefig("./Images/"+image_name)


        plt.clf()
        print("         Gráfica obtenida y guardada!\n")

    def plot_av_durations(self, inst_list, Summary_DF):

        names = list(range(0,len(inst_list)))
        values = Summary_DF['Av_Duration'].tolist()
        plt.bar(names,values, color="#216583")
        plt.title("Duración promedio de las pruebas")
        plt.xlabel("Prueba")
        plt.ylabel("Tiempo (s)")
        plt.xticks(np.arange(0, len(inst_list), 1))
        if (os.path.exists("./Images_Global") == False):
            os.system("mkdir Images_Global")

        plt.savefig("./Images_Global/Plot_Av_Dur.png")
        plt.clf()

    def plot_stds(self, inst_list, Summary_DF):
        names = list(range(0,len(inst_list)))
        values = Summary_DF['STD'].tolist()
        plt.bar(names,values, color="#216583")
        plt.title("Desviacion estandar de las pruebas")
        plt.xlabel("Prueba")
        plt.ylabel("Tiempo (s)")
        plt.xticks(np.arange(0, len(inst_list), 1))
        if (os.path.exists("./Images_Global") == False):
            os.system("mkdir Images_Global")

        plt.savefig("./Images_Global/STD.png")

        plt.clf()

    def get_durations_df(self, test, Durations_DF):
        keys = list(test.durations_dict.keys())
        values = list(test.durations_dict.values())
        Durations_DF = Durations_DF.append(pd.Series(name='Prueba'+str(test.inst_number)))
        Durations_DF = Durations_DF.append(pd.DataFrame(list(zip(keys,values)), columns = ['Name','Duration']))

        return Durations_DF

    def get_summary_df(self, test, st_dev, av_dur,i, Summary_DF):
        p = pd.DataFrame({"STD":[st_dev[i]], "Av_Duration":[av_dur[i]]})
        Summary_DF = Summary_DF.append(p, ignore_index = True)
        Summary_DF.index.rename('Test', inplace=True)
        return Summary_DF

    def create_CSV(self, Summary_DF, Durations_DF):
        if (os.path.exists("./CSV_Files") == False):
            os.system("mkdir CSV_Files")

        Summary_DF.to_csv("./CSV_Files/Summary.csv")
        Durations_DF.to_csv("./CSV_Files/Values.csv")