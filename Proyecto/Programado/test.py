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

# Rangos de parametros: inicio y final
def run():
    sil = ['3.0','5.0']
    snd = ['0.1','0.3']
    th = ['0.5', '1.5']

    Test = Create(sil, snd, th)
    Test.get_parameters()
    Test.unzip("Audio.zip")
    Test.all_param()
    Test.create_instances()
    Test.plot_av_durations()
    Test.plot_stds()

    print("Programa finalizado")
