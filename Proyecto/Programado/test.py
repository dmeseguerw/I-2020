#!/usr/bin/python

import os
import subprocess
import string
import glob
import statistics #para obtener desv estandar
import csv
import matplotlib.pyplot as plt
from AudiosDD import AudiosDD
from Create import Create
import numpy as np
import time

# Rangos de parametros: inicio y final
def run(file_name, sil_list, sil_step, snd_list, snd_step, th_list, th_step):
    start_time = time.time()


    Test = Create(file_name, sil_list, sil_step, snd_list, snd_step, th_list, th_step)
    print(time.time()-start_time)
    Test.get_parameters()
    # Test.unzip("Audio.zip")

    Test.all_param()
    Test.create_instances()
    Test.plot_av_durations()
    Test.plot_stds()

    print("Programa finalizado")
    
def run_selected_test(file_name, inst_number, sil, snd, th):
    os.system("rm -r Images/*")
    Test = AudiosDD(file_name, inst_number, sil, snd, th)
    Test.segment_audio()


def play_audio(audio_file):
    os.system("vlc splitted/"+audio_file)