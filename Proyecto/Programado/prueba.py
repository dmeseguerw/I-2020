import os
import subprocess
import string
import glob
import re

######################### PARAMETERS ############################

silence_long = ' 5.0 '
sound_long = ' 0.5 '
thresold = ' 1% '
silence_or_sound = ' 1 '

#################################################################

#########################FUNCTIONS###############################

def get_durations():
    all_files = glob.glob("./splitted/out*")
    qty = 0
    for file in all_files:
        qty = qty + 1
        outputs = subprocess.getoutput('soxi ' + file)

        data_file = open("datos.txt", "a")
        data_file.write(outputs)
        data_file.close()


        #Agregar solo la duracion, lo demas no me interesa por ahora
    new_file = open("new.txt", "a")
    with open("datos.txt") as f:
        line = f.readlines()
        for i in line: 
            if "Duration" in i: new_file.write(i)

    new_file.close()
    os.system('rm datos.txt')

    return qtyq

########################################################################

##########################MAIN############################################


os.system('sox aura.wav out.wav silence' + silence_or_sound + sound_long + thresold + silence_or_sound + silence_long + thresold + ': newfile : restart')
os.system('mv out* ./splitted')
qty = get_durations()

print (qty)

