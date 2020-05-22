import os
import subprocess
import string
import glob
import statistics #para obtener desv estandar
import csv
import matplotlib.pyplot as plt
from AudiosDD import AudiosDD
from Create import Create
from scipy.io import wavfile as wav
from scipy.fftpack import fft
import numpy as np
from scipy.fftpack import fft,fftfreq

# Rangos de parametros: inicio y final
sil = ['3.0','5.0']
snd = ['0.1','0.5']
th = ['0.5', '1.5']

Test = Create(sil, snd, th)
Test.get_parameters()
Test.unzip("Audio.zip")
Test.all_param()
Test.create_instances()

print("Programa finalizado")

