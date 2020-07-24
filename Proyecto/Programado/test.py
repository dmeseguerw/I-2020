#!/usr/bin/python

import os
import subprocess
import string
import time

from Segmentation import Segmentation
from Automatic import Automatic
from Results import Results

# Rangos de parametros: inicio y final
def run(file_name, sil_list, snd_list, th_list):
    start_time = time.time()


    Test = Automatic(file_name, sil_list, snd_list, th_list)
    
    Test.get_parameters()
    Test.all_param()
    Test.create_instances()
    
    Results().plot_av_durations(Test.inst_list, Test.Summary_DF)
    Results().plot_stds(Test.inst_list, Test.Summary_DF)

    print("Programa finalizado")
    
def run_selected_test(file_name, inst_number, sil, snd, th):
    os.system("rm -r Images/*")
    Test = Segmentation(inst_number, sil, snd, th)
    Test.segment_audio(file_name)
    Test.get_durations()

    Test.std_dev = Results().std_dev(Test.durations_list)
    Test.average = Results().average(Test.durations_list)

    Results().plot_durations(Test.durations_list, Test.inst_number)


def play_audio(audio_file):
    os.system("vlc splitted/"+audio_file)

# run("aura.wav", ['4.0','4.0','4.0'], ['0.5','0.5','0.5'], ['0.5','0.5','0.5'])
# run("aura.wav", ['4.0','5.0','1.0'], ['0.5','0.5','0.5'], ['0.5','0.5','0.5'])