import os
import subprocess
import string
import glob
import statistics #para obtener desv estandar
import csv
import matplotlib.pyplot as plt
from AudiosDD import AudiosDD
from Create import Create

Test = Create()

Test.unzip("Audio.zip")
Test.all_param()
Test.create_instances()
Test.txt_to_csv()
print("Programa finalizado")