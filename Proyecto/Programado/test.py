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

Test = Create()

Test.unzip("Audio.zip")
Test.all_param()
Test.create_instances()
Test.txt_to_csv()
print("Programa finalizado")

# fs, data = wav.read('new.wav')
# L = len(data)
# c = np.fft.fft(data) # create a list of complex number
# freq = np.fft.fftfreq(L)
# print (freq)
# freq_in_hertz = abs(freq * fs)
# print(max(freq_in_hertz))
# plt.plot(freq_in_hertz, abs(c))
# plt.xlabel("Audio")
# plt.ylabel("Tiempo (s)")
# plt.show()