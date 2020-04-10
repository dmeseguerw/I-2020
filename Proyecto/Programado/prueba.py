import os
import subprocess
import string
import glob
import statistics #para obtener desv estandar

######################### PARAMETERS ############################

silence_long = ' 5.0 '
sound_long = ' 0.5 '
thresold = ' 1% '
silence_or_sound = ' 1 '

#################################################################

#########################FUNCTIONS###############################

def get_durations():
    all_files = glob.glob("./splitted/out*")
    lista = []
    for file in all_files:
        outputs = subprocess.getoutput('soxi -D ' + file)
        lista.append(outputs)
        data_file = open("datos.txt", "a")
        data_file.write(file[11:] + " " + outputs + '\n')
        data_file.close()

    lista = list(map(float, lista))

    return lista

def std_dev(lista):
    desv = statistics.stdev(lista)
    data_file = open("datos.txt", "a")
    data_file.write("Desviacion estandar: " + str(desv) + "\n")
    data_file.close()

def average(lista):
    av = statistics.mean(lista)
    data_file = open("datos.txt", "a")
    data_file.write("Duracion promedio: " + str(av) + "\n")
    data_file.close()
    
########################################################################

##########################MAIN############################################


os.system('sox aura.wav out.wav silence' + silence_or_sound + sound_long + thresold + silence_or_sound + silence_long + thresold + ': newfile : restart')
os.system('mv out* ./splitted')
lista = get_durations()
std_dev(lista)
average(lista)

