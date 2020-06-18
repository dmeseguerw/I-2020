import os
import subprocess
import string
import glob
import statistics #para obtener desv estandar
import csv
import matplotlib.pyplot as plt
import pandas as pd

class AudiosDD:

    def __init__(self, inst_number, sil, snd, thd):
        print("Creando instancias...")
        self.inst_number = inst_number
        self.lista = []
        self.plot_image = ''
        self.desv = 0.0
        self.av = 0.0
        self.max = 0.0
        self.min = 0.0
        self.sors = '1'
        self.si = sil
        self.sn = snd
        self.th = thd
        self.df = pd.DataFrame()
        self.Dict = {}
        self.dictcounter = 0
        print("Instancias creadas!\n")

    def segment_audio(self):
        print("     Comenzando segmentación de audios...")
        os.system('sox aura.wav out.wav silence ' + self.sors + ' ' + self.sn + ' ' + self.th + ' ' + self.sors + ' ' + self.si + ' ' + self.th + ' : newfile : restart')
        
        if(os.path.exists('./splitted')==False):
            os.system("mkdir splitted")
            
        os.system('mv out* ./splitted')

        AudiosDD.get_durations(self)
        print("     Proceso finalizado!\n")


    def get_durations(self): #Obtener las duraciones de los segmentos, se guardan en datos.txt y se retorna una lista con las duraciones en orden
        print("         Obteniendo duración de los audios...")
        all_files = sorted(glob.glob("./splitted/out*"))
        self.lista = []

        for file in all_files:
            duration = subprocess.getoutput('soxi -D ' + file)
            self.Dict[file[11:]] = duration
            self.lista.append(float(duration))

        print("         Duraciones obtenidas y guardadas!\n")

        AudiosDD.std_dev(self)
        AudiosDD.average(self)
        AudiosDD.plot_durations(self)
        AudiosDD.delete_audio(self)


    def std_dev(self): #Obtengo la desviacion estandar de las duraciones de los segmentos
        print("         Obteniendo desviación estándar...")
        lista = self.lista  
        self.desv = statistics.pstdev(lista)
        print("         Desviación estándar obtenida y guardada!\n")
    

    def average(self): #Obtengo el promedio de duracion de los segmentos
        print("         Obteniendo duración promedio...")
        self.av = statistics.mean(self.lista)
        print("         Duración promedio obtenida y guardada!\n")


    def plot_durations(self): #Obtengo una grafica que muestra en comparacion todas las duraciones de los segmentos
        print("         Obteniendo gráfica...")
        values = self.lista
        names = list(range(0,len(self.lista)))
        plt.bar(names,values)
        plt.title("Duración de los audios segmentados")
        plt.xlabel("Audio")
        plt.ylabel("Tiempo (s)")
        plt.xticks(np.arange(0, len(self.lista), 1))
        image_name = 'test' + str(self.inst_number) + '.png'

        if (os.path.exists("./Images")==False):
            os.system("mkdir Images")

        plt.savefig("./Images/"+image_name)

        self.plot_image = image_name
        plt.clf()
        print("         Gráfica obtenida y guardada!\n")


    def delete_audio(self):
        print("         Eliminando audios...")
        os.system("rm ./splitted/*")
        print("         Audios eliminados!\n")