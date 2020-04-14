import os
import subprocess
import string
import glob
import statistics #para obtener desv estandar
import csv
import matplotlib.pyplot as plt
from AudiosDD import AudiosDD

new_one = AudiosDD(1)
new_one.segment_audio(' 5.0 ', ' 0.5 ', ' 1% ', ' 1 ')
new_one.std_dev()
new_one.average()
new_one.txt_to_csv()
new_one.plot_durations()
new_one.delete_audio()