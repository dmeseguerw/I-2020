import os
import subprocess
import string
import glob
import statistics #para obtener desv estandar
import csv
import matplotlib.pyplot as plt

class AudiosDD:

    def __init__(self, inst_number, sil, snd, thd):
        print("Creando instancias...")
        self.inst_number = inst_number
        self.lista = []
        self.plot_image = ''
        self.desv = 0.0
        self.av = 0.0
        self.sors = ' 1 '
        self.si = sil
        self.sn = snd
        self.th = thd
        print("Instancias creadas!\n")

    def segment_audio(self):
        print("     Comenzando segmentación de audios...")
        os.system('sox aura.wav out.wav silence' + self.sors + self.sn + self.th + self.sors + self.si + self.th + ': newfile : restart')
        
        if(os.path.exists('./splitted' == False)):
            os.system("mkdir splitted")
            
        os.system('mv out* ./splitted')

        AudiosDD.get_durations(self)
        print("     Proceso finalizado!\n")


    def get_durations(self): #Obtener las duraciones de los segmentos, se guardan en datos.txt y se retorna una lista con las duraciones en orden
        print("         Obteniendo duración de los audios...")
        all_files = sorted(glob.glob("./splitted/out*"))
        self.lista = []
        data_file = open("datos.txt", "a")
        data_file.write("Prueba" + str(self.inst_number)+ "\n")
        for file in all_files:
            outputs = subprocess.getoutput('soxi -D ' + file)
            self.lista.append(float(outputs))
            data_file.write(file[11:] + " " + outputs + '\n')
        data_file.close()
        print("         Duraciones obtenidas y guardadas!\n")

        sum_file = open("summary.txt", "a")
        AudiosDD.std_dev(self)
        AudiosDD.average(self)
        qty = os.popen('ls -1 | wc -l').read()
        sum_file.write("  Prueba " + str(self.inst_number)+": " + str(self.desv) + " " + str(self.av) + " " + qty + "\n")
        sum_file.close()
        AudiosDD.plot_durations(self)
        AudiosDD.delete_audio(self)


    def std_dev(self): #Obtengo la desviacion estandar de las duraciones de los segmentos
        print("         Obteniendo desviación estándar...")
        self.desv = statistics.stdev(self.lista)
        data_file = open("datos.txt", "a")
        data_file.write("Desviacion_estandar: " + str(self.desv) + "\n")
        data_file.close()
        print("         Desviación estándar obtenida y guardada!\n")
    

    def average(self): #Obtengo el promedio de duracion de los segmentos
        print("         Obteniendo duración promedio...")
        self.av = statistics.mean(self.lista)
        data_file = open("datos.txt", "a")
        data_file.write("Duracion_promedio: " + str(self.av) + "\n\n")
        data_file.close()
        print("         Duración promedio obtenida y guardada!\n")


    def plot_durations(self): #Obtengo una grafica que muestra en comparacion todas las duraciones de los segmentos
        print("         Obteniendo gráfica...")
        values = self.lista
        names = sorted(os.listdir('./splitted'))
        plt.bar(names,values)
        plt.title("Duración de los audios segmentados")
        plt.xlabel("Audio")
        plt.ylabel("Tiempo (s)")
        # plt.show()
        image_name = 'test' + str(self.inst_number) + '.png'
        if (os.path.exists("./Images")):
            plt.savefig("./Images/"+image_name)
        else:
            os.system("mkdir Images")
            plt.savefig("./Images/"+image_name)
        self.plot_image = image_name
        plt.clf()
        print("         Gráfica obtenida y guardada!\n")

    
    def delete_audio(self):
        print("         Eliminando audios...")
        os.system("rm ./splitted/*")
        print("         Audios eliminados!\n")