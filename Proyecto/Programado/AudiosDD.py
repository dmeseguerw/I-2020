import os
import subprocess
import string
import glob
import statistics #para obtener desv estandar
import csv
import matplotlib.pyplot as plt

class AudiosDD:

    def __init__(self, inst_number):
        self.inst_number = inst_number
        self.lista = []
        self.plot_image = ''
        self.desv = 0.0
        self.av = 0.0

    def segment_audio(self, si_long, snd_long, thd, siorsnd):
        os.system('sox aura.wav out.wav silence' + siorsnd + snd_long + thd + siorsnd + si_long + thd + ': newfile : restart')
        os.system('mv out* ./splitted')
        AudiosDD.get_durations(self)

    def get_durations(self): #Obtener las duraciones de los segmentos, se guardan en datos.txt y se retorna una lista con las duraciones en orden
        all_files = sorted(glob.glob("./splitted/out*"))
        self.lista = []
        data_file = open("datos.txt", "a")
        data_file.write("Prueba1\n")
        for file in all_files:
            outputs = subprocess.getoutput('soxi -D ' + file)
            self.lista.append(outputs)
            data_file.write(file[11:] + " " + outputs + '\n')
        data_file.close()

        self.lista = list(map(float, self.lista))
        print(self.lista)

    def std_dev(self): #Obtengo la desviacion estandar de las duraciones de los segmentos
        self.desv = statistics.stdev(self.lista)
        data_file = open("datos.txt", "a")
        data_file.write("Desviacion_estandar: " + str(self.desv) + "\n")
        data_file.close()
    

    def average(self): #Obtengo el promedio de duracion de los segmentos
        self.av = statistics.mean(self.lista)
        data_file = open("datos.txt", "a")
        data_file.write("Duracion_promedio: " + str(self.av) + "\n")
        data_file.close()


    def txt_to_csv(self): # Obtengo un archivo .csv para poder organizar los datos
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


    def plot_durations(self): #Obtengo una grafica que muestra en comparacion todas las duraciones de los segmentos
        values = self.lista
        names = sorted(os.listdir('./splitted'))
        plt.bar(names,values)
        plt.title("Duración de los audios segmentados")
        plt.xlabel("Audio")
        plt.ylabel("Tiempo (s)")
        # plt.show()
        image_name = 'test.png'
        plt.savefig(image_name)
        self.plot_image = image_name

    
    def delete_audio(self):
        os.system("rm ./splitted/*")