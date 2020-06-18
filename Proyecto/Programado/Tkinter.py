try:
    import Tkinter as tk
except:
    import tkinter as tk

from tkinter import ttk

import test
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
from PIL import Image
from PIL import ImageTk



class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
    



class StartPage(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Sistema de segmentacion automática de audios \n Elaborado por Daniel Meseguer Wong", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)

        # self.button1 = tk.Button(self, text = "Realizar segmentacion",
        #           command=lambda: [self.on_button()]).pack()
        
        self.button1 = tk.Button(self, text = "Realizar segmentacion",
                  command=lambda: master.switch_frame(PageOne)).pack()

        # tk.Button(self, text="Visualizar resultados",
        #           command=lambda: master.switch_frame(PageResults)).pack()

        tk.Button(self, text="Salir",
                  command=lambda: quit()).pack()

        tk.Text(self, height=1, width=10).pack()

        img = ImageTk.PhotoImage(Image.open("silence.png"))
        lab = tk.Label(self, image=img)
        lab.image = img
        lab.pack()

    

class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self)
        self.text = tk.StringVar()
        self.text.set("Original Text")
        tk.Label(self, text="\t Seleccionar parámetros \t", font=('Helvetica', 18, "bold")).pack()

        self.button1 = tk.Button(self, text = "Realizar segmentacion",
                  command=lambda: [self.on_button()]).pack()
        self.lab1 = tk.Label(self, text="Cargando...")
        tk.Button(self, text="Visualizar resultados",
                  command=lambda: master.switch_frame(PageResults)).pack()
        
    def on_button(self):
        print('Button clicked')
        self.lab1.pack()
        self.lab1['text'] = 'Cargando segmentacion...'
        self.after(5000, self.run_test)
 
 
    def run_test(self):
        test.run()
        self.lab1['text'] = 'Segmentacion lista! Presiona click en Visualizar resultados.'
    

class PageResults(tk.Frame):
    def get_tests(self):
        self.test_count = 0
        self.test_list = []
        for file in os.listdir("Images/"):
            self.test_list.append(str(self.test_count))
            self.test_count = self.test_count+1
        return 

    def callback(self,*args):
        self.csv_reader()
        # self.opt.configure(text="{}".format(self.a.get()))
        for i in range(0,self.test_count):

            if(self.a.get()==self.test_list[i]):
                self.data_label['text']= "\n Duración promedio: "+self.durations_list[i] + "\n Desviación estándar: " + self.std_list[i]
                self.img2 = ImageTk.PhotoImage(Image.open("Images/test"+str(i)+".png"))
                self.lab.configure(image=self.img2)
                self.lab.image = self.img2
        self.lab.pack(side='right')
        self.data_label.pack()

    def csv_reader(self):
        self.durations_list = []
        self.std_list=[]
        with open('CSV_Files/Summary.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if(line_count > 0):
                    self.durations_list.append(row[1])
                    self.std_list.append(row[2])
                line_count+=1

        
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self)
        tk.Label(self, text="Selección de prueba", font=('Helvetica', 18, "bold")).pack()
        tk.Label(self, text="\n").pack()
        tk.Button(self, text="Ver comparacion de pruebas",
                  command=lambda: master.switch_frame(PageThree)).pack()
        tk.Label(self, text="\n").pack()
        tk.Label(self, text="Seleccionar prueba: ").pack()
        self.a = tk.StringVar(self)
        self.a.set("0")
        self.get_tests()
        self.menu = ttk.Combobox(self, textvariable=self.a, values = self.test_list)
        self.menu.pack()
    
        self.data_label = tk.Label(self, text="Duracion promedio: \nDesviación estándar:", font=('Helvetica', 12, "bold"))
        self.data_label.pack()

        self.img = ImageTk.PhotoImage(Image.open("silence.png"))
        self.lab = tk.Label(self, image=self.img)
        self.lab.image = self.img

        # self.opt = tk.Label(self, text=self.a.get())
        # self.opt.pack()
        self.a.trace("w", self.callback)


        
        tk.Label(self, text="\n\n").pack()
        tk.Button(self, text="Go back to start page",
                  command=lambda: master.switch_frame(StartPage)).pack(side="bottom")



class PageThree(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self)
        tk.Label(self, text="Resultados globales", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)

        self.img = ImageTk.PhotoImage(Image.open("Images_Global/Plot_Av_Dur.png"))
        self.lab = tk.Label(self, image=self.img)
        self.lab.image = self.img
        self.lab.pack(side="left")


        self.img2 = ImageTk.PhotoImage(Image.open("Images_Global/STD.png"))
        self.lab2 = tk.Label(self, image=self.img2)
        self.lab2.image = self.img2
        self.lab2.pack(side="right")

        tk.Button(self, text="Volver a resultados individuales",
                  command=lambda: master.switch_frame(PageResults)).pack()

        tk.Button(self, text="Ver datos",
                  command=lambda: master.switch_frame(PageFour)).pack()

    

class PageFour(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self)
        tk.Label(self, text="Datos Globales", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)

        tk.Button(self, text="Volver a gráficas globales",
                  command=lambda: master.switch_frame(PageThree)).pack()

        tk.Button(self, text="Volver a inicio",
                  command=lambda: master.switch_frame(StartPage)).pack()

    

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()








































# # import ttk

# window = tk.Tk()
# window.title("Proyecto Eléctrico") #nombre de la ventana
# # window.geometry('720x420')
# window.geometry("")
# frame = tk.Frame()
# frame.pack()
# # frame.config(bg = "light green")
# frame.config(width="150", height="150")
# title_label = tk.Label(master = frame, text = "   Sistema de segmentación automática de audios   ")
# title_label.config(font=('Arial Bold', 20))
# title_label.pack()



# emptyframe = tk.Frame()
# emptyframe.pack()
# ch1_label = tk.Label(emptyframe, text = "MENU")
# ch1_label.pack(side = tk.LEFT)

# ch1_label.config(width="50", height="15")
# frame2 = tk.Frame()

# # frame2.config(bg = "light green")
# frame2.config(width="150", height="150")
# btn1 = tk.Button(master = frame2, text = "Comenzar segmentación")
# btn1.config(font=('Arial Bold', 15), bg = "light blue")
# btn1.pack(side = "right")
# frame2.pack(side = "right")


# window.mainloop() #Dejar la ventana abierta hasta que el usuario interactue
