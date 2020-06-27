#!/usr/bin/python
import os
import subprocess
import string
import glob
from Results import Results

class Segmentation:

    def __init__(self, inst_number, sil, snd, thd):
        print("Creando instancias...")
        self.inst_number = inst_number
        self.durations_list = []
        self.std_dev = 0.0
        self.average = 0.0
        self.silence = sil
        self.sound = snd
        self.threshold = thd
        self.durations_dict = {}
        print("Instancias creadas!\n")

    def segment_audio(self, file_name):
        print("     Comenzando segmentación de audios...")
        os.system('sox ' + file_name +   ' out.wav silence ' + '1' + ' ' + self.sound + ' ' + self.threshold + ' ' + '1' + ' ' + self.silence + ' ' + self.threshold + ' : newfile : restart')
        
        if(os.path.exists('./splitted')==False):
            os.system("mkdir splitted")
            
        os.system('mv out* ./splitted')

        print("     Proceso finalizado!\n")

    def get_durations(self): #Obtener las duraciones de los segmentos, se guardan en datos.txt y se retorna una lista con las duraciones en orden
        print("         Obteniendo duración de los audios...")
        all_files = sorted(glob.glob("./splitted/out*"))
        self.durations_list = []

        for file in all_files:
            duration = subprocess.getoutput('soxi -D ' + file)
            self.durations_dict[file[11:]] = duration
            self.durations_list.append(round(float(duration),2))

        print(self.durations_list)
        print("         Duraciones obtenidas y guardadas!\n")

    def delete_audio(self):
        print("         Eliminando audios...")
        os.system("rm ./splitted/*")
        print("         Audios eliminados!\n")