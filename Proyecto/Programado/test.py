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
def run():
    start_time = time.time()
    sil = ['3.0','3.0']
    snd = ['0.1','0.2']
    th = ['0.5', '1.0']

    Test = Create(sil, snd, th)
    print(time.time()-start_time)
    Test.get_parameters()
    Test.unzip("Audio.zip")
    Test.all_param()
    Test.create_instances()
    Test.plot_av_durations()
    Test.plot_stds()

    print("Programa finalizado")
    
    return

