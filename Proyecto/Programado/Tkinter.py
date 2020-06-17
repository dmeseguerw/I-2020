try:
    import Tkinter as tk
except:
    import tkinter as tk

from test import run
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
        tk.Label(self, text="Start page", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Go to page one",
                  command=lambda: master.switch_frame(PageOne)).pack()
        tk.Button(self, text="Go to page two",
                  command=run())

class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='blue')
        tk.Label(self, text="Page one", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Go back to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()

class PageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='red')
        tk.Label(self, text="Page two", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Go back to start page",
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
