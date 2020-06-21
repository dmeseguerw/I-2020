try:
    import Tkinter as tk
except:
    import tkinter as tk

from tkinter import ttk

import itertools
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
from tkinter.filedialog import askopenfile 


favorites_list = []
durations_list = []
std_list = []

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.pack_forget()
        self._frame = new_frame
        self._frame.pack()
    



class StartPage(tk.Frame):
    def clean(self):
        os.system("make clean")

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Automatic Audio Segmentation System \n By Daniel Meseguer Wong", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)

        
        tk.Button(self, text = "Start process", foreground="green",
                  command=lambda: master.switch_frame(Page_Parameter)).pack()

        tk.Button(self, text="Help guide", activeforeground="blue", command=lambda: master.switch_frame(PageHelp)).pack()

        tk.Button(self, text="Exit", foreground="red" ,
                  command=lambda:[quit()]).pack()


        img = ImageTk.PhotoImage(Image.open("silence.png"))
        lab = tk.Label(self, image=img)
        lab.image = img
        lab.pack()


class PageHelp(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Help", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        self.help_frames = tk.Frame(self)
        self.help_frames.pack()

        tk.Button(self, text="Back", activeforeground="red" ,
                  command=lambda: master.switch_frame(StartPage)).pack(side="bottom")


        self.text_frame = tk.Frame(self)
        self.text_frame.pack()



        self.l1=tk.Label(self.text_frame, text="\n", font="bold")
        self.l1.pack()


        self.l1["text"]="\n\nAudio segmentation is a pre process step involved in speech technology systems, specifically on speech recognition.\n This system provides an automatic and simple way to segment an audio file based on a selection of parameters.\n Once the parameters are saved, you can proceed to segment the audio, which will take some time, and once it's done,\n results will show up both for tests individually and globally, including average durations and standard deviations.\n\n"

        self.b3 = tk.Button(self.help_frames, text = "Audio segmentation",bg="light green",
                        command=lambda: self.help_params(1))
        self.b3.pack(side="left")

        self.b1 = tk.Button(self.help_frames, text = "Parameter selection",bg="white",
                  command=lambda: self.help_params(2))
        self.b1.pack(side="left")


        self.b2=tk.Button(self.help_frames, text = "Test results", bg = "white",
                  command=lambda: self.help_params(3))
        self.b2.pack(side="left")

        



    def help_params(self, selection):
        if(selection==2):
            self.b1.configure(bg="light green")
            self.b2.configure(bg="white")
            self.b3.configure(bg="white")
            self.l1["text"] = "\n\nThere are 3 different parameters you must insert. Silence range, Sound range and Threshold range.\n\n" + "Silence range (s): Duration of audio to be detected as silence. Insert initial and final value of range, followed by a step.\n The example means the initial value is 2 seconds, final value is 5 seconds, and step is 1 second. \nFor example: 2.0,5.0,1.0 \n\n Sound range (s): Duration of audio to be detected as a sound. Insert initial and final value of range, followed by a step.\n The example means the initial value is 0.5 seconds, final value is 1 second, and step is 0.1 seconds. \nFor example: 0.5,1.0,0.1\n\n Threshold range (s): Level of audio to be detected as sound if level is higher or as silence if level is lower than threshold.\n Insert initial and final value of range, followed by a step.\n The example means the initial value is 0.5%, final value is 1%, and step is 0.5%.\nFor example: 0.5,1.0,0.5\n\nOnce this is done, click on Save parameters button, and then click on Segment audio to proceed.\n Once the segmentation is done, you will see a notification, and then click on View results to check results of all tests.\n\n"
        if(selection==3):
            self.b1.configure(bg="white")
            self.b2.configure(bg="light green")
            self.b3.configure(bg="white")
            self.l1["text"] = "\n\n1. You can choose a test by clicking on the dropdown option.\n\n2. You can add a test to favorites by clicking on the button Add to favorites, which will turn its background to green.\n\nEach test will show a plot of all durations of segmented audios, together with average duration and standard deviation data.\n\n3.Choose to view global results and favorite tests by clicking on the View global results and favorites.\n On Global Results two plots will show: average duration of all tests, and standard deviation of all tests, together with the results of favorite tests."
        if(selection==1):
            self.b1.configure(bg="white")
            self.b2.configure(bg="white")
            self.b3.configure(bg="light green")
            self.l1["text"]="\n\nAudio segmentation is a pre process step involved in speech technology systems, specifically on speech recognition.\n This system provides an automatic and simple way to segment an audio file based on a selection of parameters.\n Once the parameters are saved, you can proceed to segment the audio, which will take some time, and once it's done,\n results will show up both for tests individually and globally, including average durations and standard deviations.\n\n"


file = ""
snd_list = []
sil_list = []
th_list = []
class Page_Parameter(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self)
        

        tk.Label(self, text="\t Select parameters \t", font=('Helvetica', 18, "bold")).pack()

        self.frame1 = tk.Frame(self)
        self.frame1.pack(pady=15)


        btn = tk.Button(self.frame1, text ='Select audio file', activeforeground="blue" , command = lambda:self.open_file()) 
        btn.pack(side="left")

        self.file_label = tk.Label(self.frame1, text="")
        self.file_label.pack(side="right")

        tk.Label(self, text="Silence range (s): MIN,MAX,STEP \nDuration of audio to be detected as silence.").pack()
        self.range_sil = tk.Entry(self, width=10)
        self.range_sil.pack()
        
        tk.Label(self, text="Sound range (s): MIN,MAX,STEP \nDuration of audio to be detected as sound.").pack()
        self.range_snd = tk.Entry(self, width=10)
        self.range_snd.pack()
        tk.Label(self, text="Threshold range (%): MIN,MAX,STEP \nThreshold of sound. If level is higher than thresold->taken as sound. If lower than threshold->taken as silence.").pack()
        self.range_th = tk.Entry(self, width=10)
        self.range_th.pack()

        #############################################################################################

        
        tk.Button(self, text="Save parameters" , activeforeground="blue",
                  command=lambda: self.save_params()).pack(pady=15)
        tk.Label(self,text="\n").pack()

        tk.Button(self, text = "Segment audio" , activeforeground="blue",
                  command=lambda: [self.on_button()]).pack()
        self.lab1 = tk.Label(self, text="")
        tk.Button(self, text="View results" , activeforeground="blue",
                  command=lambda: master.switch_frame(PageResults)).pack()

    def open_file(self): 
        global file
        os.system("make clean")
        self.file1 = askopenfile(filetypes=(("MP3 File", "*.mp3"),
                                      ("Wav File", "*.wav")))
        self.file_label["text"]=os.path.basename(self.file1.name)
        self.file_label.configure(fg="blue", bg="light blue")
        self.file_label.pack(side="right")
        file = self.file1.name
        print(self.file1.name)

        
    def on_button(self):
        print('Button clicked')
        self.lab1.pack()
        self.lab1['text'] = 'Loading segmentation...'
        self.after(5000, self.run_test)
 
 
    def run_test(self):
        print(sil_list)
        test.run(file, sil_list, self.sil_step, snd_list, self.snd_step, th_list, self.th_step)
        self.lab1['text'] = 'Done! Click on View results'
    

    def save_params(self):
        global sil_list
        global snd_list
        global th_list
        sil = self.range_sil.get()
        snd = self.range_snd.get()
        th = self.range_th.get()
        sil_list = [float(i) for i in sil.split(',')]
        self.sil_step = sil_list[2]
        sil_list.pop(2)


        snd_list = [float(i) for i in snd.split(',')]
        self.snd_step = snd_list[2]
        snd_list.pop(2)

        th_list = [float(i) for i in th.split(',')]
        self.th_step = th_list[2]
        th_list.pop(2)

        print(sil_list)
        print(snd_list)
        print(th_list)

class PageResults(tk.Frame):

    def __init__(self, master):
        self.condition=False
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self)
        tk.Label(self, text="Test selection", font=('Helvetica', 18, "bold")).pack()
        tk.Label(self, text="\n").pack()
        tk.Button(self, text="View global results and favorites",
                  command=lambda: master.switch_frame(PageThree)).pack()
        tk.Label(self, text="\n").pack()
        tk.Label(self, text="Select test: ").pack()
        self.a = tk.StringVar(self)
        self.a.set("0")
        self.get_tests()
        self.menu = ttk.Combobox(self, textvariable=self.a, values = self.test_list)
        self.menu.pack()
    
        self.data_label = tk.Label(self, text="", font=('Helvetica', 12, "bold"))
        self.data_label.pack()

        self.img = ImageTk.PhotoImage(Image.open("silence.png"))
        self.lab = tk.Label(self, image=self.img)
        self.lab.image = self.img

        self.Fav = tk.StringVar(self)
        self.Fav.set("Add to favorites")
        self.fav_button = tk.Button(self, textvariable=self.Fav, command=lambda: self.favorite())
        self.fav_button.pack()

        # self.opt = tk.Label(self, text=self.a.get())
        # self.opt.pack()
        self.a.trace("w", self.callback)


        
        tk.Label(self, text="\n\n").pack()
        tk.Button(self, text="Go back to main menu",
                  command=lambda: master.switch_frame(StartPage)).pack(side="bottom")

    def get_tests(self):
        self.test_count = 0
        self.test_list = []
        for file in os.listdir("Images/"):
            self.test_list.append(str(self.test_count))
            self.test_count = self.test_count+1 

    def callback(self,*args):
        self.csv_reader()
        # self.opt.configure(text="{}".format(self.a.get()))
        for i in range(0,self.test_count):

            if(self.a.get()==self.test_list[i]):
                if(self.a.get() in favorites_list):
                    self.Fav.set("Saved in favorites!")
                    self.fav_button.configure(bg="green")
                else:
                    self.Fav.set("Add to favorites")
                    self.fav_button.configure(state="normal", bg="white")

                self.data_label['text']= "\n Average duration: "+durations_list[i] + "\n Standard deviation: " + std_list[i]
                self.img2 = ImageTk.PhotoImage(Image.open("Images/test"+str(i)+".png"))
                self.lab.configure(image=self.img2)
                self.lab.image = self.img2
        self.lab.pack(side='right')
        self.data_label.pack()

    def csv_reader(self):
        # global durations_list = []
        # global std_list=[]
        with open('CSV_Files/Summary.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if(line_count > 0):
                    durations_list.append(row[1])
                    std_list.append(row[2])
                line_count+=1

    def favorite(self):
        if(self.a.get() not in favorites_list):
            favorites_list.append(self.a.get())
            favorites_list.sort()
            self.Fav.set("Saved in favorites!")
            self.fav_button.configure(bg="green")
        else:
            self.Fav.set("Add to favorites")
            self.fav_button.configure(bg="white")
            favorites_list.remove(self.a.get())
        print(favorites_list)
            

class PageThree(tk.Frame):
    def __init__(self, master):
        global file
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self)
        tk.Label(self, text="Global Results", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)

        tk.Button(self, text="Back to test results",
                  command=lambda: master.switch_frame(PageResults)).pack()
        
        tk.Label(self, text = "Favorites", font=("Helvetica", 15, "bold")).pack()

        self.fav_frame = tk.Frame(self)
        self.fav_frame.pack()
        self.a = tk.StringVar(self.fav_frame)
        self.a.set("0")
        self.get_tests()
        self.menu = ttk.Combobox(self.fav_frame, textvariable=self.a, values = favorites_list)
        self.menu.pack(side="left")

        self.all_param()

        tk.Button(self.fav_frame, text = "Final selection", command=lambda: test.run_selected_test(file, int(self.a.get()), self.final_sil, self.final_snd, self.final_th)).pack(side="right")


        
        
        self.fav_label = tk.Label(self, text="Test    |   Average duration   |   Standard deviation\n")
        self.fav_label.pack()
        self.favorite_data()
        #########################################################################################

        self.img = ImageTk.PhotoImage(Image.open("Images_Global/Plot_Av_Dur.png"))
        self.lab = tk.Label(self, image=self.img)
        self.lab.image = self.img
        self.lab.pack(side="left")


        self.img2 = ImageTk.PhotoImage(Image.open("Images_Global/STD.png"))
        self.lab2 = tk.Label(self, image=self.img2)
        self.lab2.image = self.img2
        self.lab2.pack(side="right")

    def get_tests(self):
        self.test_count = 0
        self.test_list = []
        for file in os.listdir("Images/"):
            self.test_list.append(str(self.test_count))
            self.test_count = self.test_count+1

    def favorite_data(self):
        for i in favorites_list:
            self.fav_label["text"] += i + "                   " + durations_list[int(i)] + "                     " + std_list[int(i)] + "      \n"

    def all_param(self): #Crea una lista con todas las posibles combinaciones entre los parámetros adjuntos en las listas sil, snd y th
        print("Obteniendo todas las posibles combinaciones de parámetros...")
        new_list = [sil_list, snd_list, th_list]
        self.param_list = list(itertools.product(*new_list))
        print(str(len(self.param_list)) + " combinaciones obtenidas!\n")
        self.final_sil = str(self.param_list[int(self.a.get())][0])
        self.final_snd = str(self.param_list[int(self.a.get())][1])
        self.final_th = str(self.param_list[int(self.a.get())][2])
        print(type(self.final_sil))
        print(type(self.final_snd))
        print(type(self.final_th))

class PageFour(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self)
        tk.Label(self, text="Global Results CHANGE PAGE", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)

        tk.Button(self, text="Volver a gráficas globales",
                  command=lambda: master.switch_frame(PageThree)).pack()

        tk.Button(self, text="Volver a inicio",
                  command=lambda: master.switch_frame(StartPage)).pack()

    

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()

