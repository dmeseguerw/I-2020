#!/usr/bin/python

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
import statistics 
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
file = ""
snd_list = []
sil_list = []
th_list = []


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

        tk.Label(self, text="Automatic Audio Segmentation System \n By Daniel Meseguer Wong\n",fg="#293462", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)

        
        self.btn_frame = tk.Frame(self)
        self.btn_frame.pack()
        tk.Button(self.btn_frame, text = "Start process", activebackground = "#2e599b",bg="#293462", activeforeground="white", fg="white",
                  command=lambda: master.switch_frame(Page_Parameter)).pack(side="left")

        

        tk.Button(self.btn_frame, text="Help guide", activeforeground="white", fg="white",bg="#216583",activebackground="#0880af", command=lambda: master.switch_frame(PageHelp)).pack(side="left")

        tk.Button(self.btn_frame, text="Exit", bg="#f76262" , activebackground="#ff8080",activeforeground="white", fg = "white",
                  command=lambda:[quit()]).pack(side="left")

        tk.Label(self, text="\n\n").pack()
        img = ImageTk.PhotoImage(Image.open("silence.png"))
        lab = tk.Label(self, image=img)
        lab.image = img
        lab.pack()


class PageHelp(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Help", fg="#216583", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        self.help_frames = tk.Frame(self)
        self.help_frames.pack()

        tk.Button(self, text="Back", fg="white" , activeforeground="white",bg="#f76262",activebackground="#ff8080",
                  command=lambda: master.switch_frame(StartPage)).pack(side="bottom")


        self.text_frame = tk.Frame(self)
        self.text_frame.pack()



        self.l1=tk.Label(self.text_frame, text="\n", font="bold", fg="#293462")
        self.l1.pack()


        self.l1["text"]="\n\nAudio segmentation is a pre process step involved in speech technology systems, specifically on speech recognition.\n This system provides an automatic and simple way to segment an audio file based on a selection of parameters.\n Once the parameters are saved, you can proceed to segment the audio, which will take some time, and once it's done,\n results will show up both for tests individually and globally, including average durations and standard deviations.\n\n"

        self.b3 = tk.Button(self.help_frames, text = "Audio segmentation",bg="#216583", fg="white", activebackground="#2e599b", activeforeground="white",
                        command=lambda: self.help_params(1))
        self.b3.pack(side="left")

        self.b1 = tk.Button(self.help_frames, text = "Parameter selection",bg="#fff1c1", activebackground="#fcfbdd", fg = "#216583", activeforeground="#216583",
                  command=lambda: self.help_params(2))
        self.b1.pack(side="left")


        self.b2=tk.Button(self.help_frames, text = "Test results", bg = "#fff1c1", activebackground="#fcfbdd", fg = "#216583", activeforeground="#216583",
                  command=lambda: self.help_params(3))
        self.b2.pack(side="left")

        



    def help_params(self, selection):
        if(selection==2):
            self.b1.configure(bg="#216583",fg="white", activebackground="#2e599b", activeforeground="white")
            self.b2.configure(bg="#fff1c1", fg = "#216583", activeforeground="#216583", activebackground="#fcfbdd")
            self.b3.configure(bg="#fff1c1", fg = "#216583", activeforeground="#216583", activebackground="#fcfbdd")
            self.l1["text"] = "\n\nThere are 3 different parameters you must insert. Silence range, Sound range and Threshold range.\n\n" + "Silence range (s): Duration of audio to be detected as silence. Insert initial and final value of range, followed by a step.\n The example means the initial value is 2 seconds, final value is 5 seconds, and step is 1 second. \nFor example: 2.0,5.0,1.0 \n\n Sound range (s): Duration of audio to be detected as a sound. Insert initial and final value of range, followed by a step.\n The example means the initial value is 0.5 seconds, final value is 1 second, and step is 0.1 seconds. \nFor example: 0.5,1.0,0.1\n\n Threshold range (s): Level of audio to be detected as sound if level is higher or as silence if level is lower than threshold.\n Insert initial and final value of range, followed by a step.\n The example means the initial value is 0.5%, final value is 1%, and step is 0.5%.\nFor example: 0.5,1.0,0.5\n\nOnce this is done, click on Save parameters button, and then click on Segment audio to proceed.\n Once the segmentation is done, you will see a notification, and then click on View results to check results of all tests.\n\n"
        if(selection==3):
            self.b1.configure(bg="#fff1c1", fg = "#216583", activeforeground="#216583", activebackground="#fcfbdd")
            self.b2.configure(bg="#216583",fg="white", activebackground="#2e599b", activeforeground="white")
            self.b3.configure(bg="#fff1c1", fg = "#216583", activeforeground="#216583", activebackground="#fcfbdd")
            self.l1["text"] = "\n\n1. You can choose a test by clicking on the dropdown option.\n\n2. You can add a test to favorites by clicking on the button Add to favorites, which will turn its background to green.\n\nEach test will show a plot of all durations of segmented audios, together with average duration and standard deviation data.\n\n3.Choose to view global results and favorite tests by clicking on the View global results and favorites.\n On Global Results two plots will show: average duration of all tests, and standard deviation of all tests, together with the results of favorite tests.\n"
        if(selection==1):
            self.b1.configure(bg="#fff1c1", fg = "#216583", activeforeground="#216583", activebackground="#fcfbdd")
            self.b2.configure(bg="#fff1c1", fg = "#216583", activeforeground="#216583", activebackground="#fcfbdd")
            self.b3.configure(bg="#216583",fg="white", activebackground="#2e599b", activeforeground="white")
            self.l1["text"]="\n\nAudio segmentation is a pre process step involved in speech technology systems, specifically on speech recognition.\n This system provides an automatic and simple way to segment an audio file based on a selection of parameters.\n Once the parameters are saved, you can proceed to segment the audio, which will take some time, and once it's done,\n results will show up both for tests individually and globally, including average durations and standard deviations.\n\n"



class Page_Parameter(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        self.title_frame = tk.Frame(self)
        self.title_frame.pack()
        tk.Button(self.title_frame, text="Back to start page", bg="#f76262", activebackground="#ff8080", activeforeground="white", fg = "white", command=lambda: master.switch_frame(StartPage)).pack(side="left")
        tk.Label(self.title_frame, text="\t\tSelect parameters   \t\t\t", fg="#293462", font=('Helvetica', 18, "bold")).pack(side="left")
        # tk.Button(self.title_frame, text="Help", fg="blue", command=lambda: master.switch_frame(PageHelp)).pack(side="left")

        self.frame1 = tk.Frame(self)
        self.frame1.pack(pady=15)


        btn = tk.Button(self.frame1, text ='Select audio file', fg="white", activeforeground="white", bg="#216583", activebackground="#0880af" , command = lambda:self.open_file()) 
        btn.pack(side="left")

        self.file_label = tk.Label(self.frame1, text="")
        self.file_label.pack(side="right")

        tk.Label(self, text="\nDuration of audio to be detected as silence.", fg="#293462").pack()
        self.sil_frame=tk.Frame(self)
        self.sil_frame.pack()
        tk.Label(self.sil_frame, text="Silence range (s): MIN,MAX,STEP ", fg="#293462", font=("Helvetica", 11, "bold")).pack(side="left")
        self.range_sil = tk.Entry(self.sil_frame, width=10, bg="white")
        self.range_sil.pack(side="right")
        

        tk.Label(self, text="\nDuration of audio to be detected as sound.", fg="#293462").pack()
        self.snd_frame=tk.Frame(self)
        self.snd_frame.pack()
        tk.Label(self.snd_frame, text="Sound range (s): MIN,MAX,STEP", fg="#293462", font=("Helvetica", 11, "bold")).pack(side="left")
        self.range_snd = tk.Entry(self.snd_frame, width=10, bg="white")
        self.range_snd.pack(side="right")


        tk.Label(self, text="\nThreshold of sound. If level is higher than thresold->taken as sound.\n If lower than threshold->taken as silence.", fg="#293462").pack()
        self.th_frame=tk.Frame(self)
        self.th_frame.pack()
        tk.Label(self.th_frame, text="Threshold range (%): MIN,MAX,STEP", fg="#293462", font=("Helvetica", 11, "bold")).pack(side="left")
        self.range_th = tk.Entry(self.th_frame, width=10, bg="white")
        self.range_th.pack(side="right")

        #############################################################################################
        tk.Label(self,text="\n\n").pack()
        frame_btn = tk.Frame(self)
        frame_btn.pack()

        s = ttk.Style()
        s.theme_use('clam')
        s.configure("#0880af.Horizontal.TProgressbar", foreground='#0880af', background='#0880af')
        self.pb = ttk.Progressbar(self, style="#0880af.Horizontal.TProgressbar",length=325)
        self.pb.pack()
        
        self.par_btn = tk.Button(frame_btn, text="Save parameters" , bg = "#216583", activebackground="#0880af", fg="white", activeforeground="white", font=("Helvetica",11,"bold"),
                  command=lambda: self.save_params())
        self.par_btn.pack(pady=15, side="left")


        self.par_label = tk.Label(self, text="\n", fg="#293462")
        self.par_label.pack()

        self.seg_btn = tk.Button(frame_btn, text = "Segment audio", font=("Helvetica",11,"bold"), bg = "#fff1c1", activebackground="#fcfbdd",fg = "#216583", activeforeground="#0880af",
                  command=lambda: [self.on_button()])
        self.seg_btn.pack(side="left")

        self.par_label.pack()
        
        self.res_btn = tk.Button(self, text="View results" , font=("Helvetica",11,"bold"), bg = "#fff1c1", activebackground="#fcfbdd",fg = "#216583", activeforeground="#0880af",
                  command=lambda: master.switch_frame(PageResults))
        self.res_btn.pack(pady=10)


    def open_file(self): 
        global file
        os.system("make clean")
        self.file1 = askopenfile(filetypes=(("MP3 File", "*.mp3"),
                                      ("Wav File", "*.wav")))
        self.file_label["text"]=os.path.basename(self.file1.name)
        self.file_label.configure(fg="white", bg="#216583")
        self.file_label.pack(side="right")
        file = self.file1.name
        print(self.file1.name)

        
    def on_button(self):
        print('Button clicked')
        self.par_label.pack()
        self.par_label.configure(font=("Helvetica", 10, "bold"))
        self.par_label['text'] = 'Loading segmentation...\n'
        self.after(1000, self.run_test)
 
 
    def run_test(self):
        print(sil_list)
        test.run(file, sil_list, self.sil_step, snd_list, self.snd_step, th_list, self.th_step)
        self.par_label['text'] = 'Done! Click on View results\n'
        self.pb.step(347.9999)
        self.seg_btn.configure(bg = "#fff1c1", activebackground="#fcfbdd",fg = "#216583", activeforeground="#0880af")
        self.res_btn.configure(bg = "#216583", activebackground="#0880af", fg="white", activeforeground="white")
    

    def save_params(self):
        self.pb.step(52)
        self.par_label["text"]="Parameters saved!\n"
        self.par_label.configure(font=("Helvetica", 10, "bold"))
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

        self.par_btn.configure(bg = "#fff1c1", activebackground="#fcfbdd",fg = "#216583", activeforeground="#0880af")
        self.seg_btn.configure(bg = "#216583", activebackground="#0880af", fg="white", activeforeground="white")

class PageResults(tk.Frame):

    def __init__(self, master):
        global durations_list
        global std_list
        global favorites_list
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self)
        tk.Label(self, text="Test selection", fg = "#293462",font=('Helvetica', 18, "bold")).pack()
        tk.Label(self, text="\n").pack()
        tk.Button(self, text="View global results and favorites", bg = "#216583", activebackground="#0880af", fg="#fff1c1", activeforeground="#fcfbdd",
                  command=lambda: master.switch_frame(PageGlobRes)).pack()
        tk.Label(self, text="\n").pack()
        tk.Label(self, text="Select test: ", fg="#216583").pack()

        self.a = tk.StringVar(self)
        self.a.set("0")
        self.get_tests()
        self.menu = ttk.Combobox(self, textvariable=self.a, values = self.test_list)
        self.menu.pack()
        self.csv_reader()
        self.data_label = tk.Label(self, text="\n Average duration: "+durations_list[0] + "\n Standard deviation: " + std_list[0], fg="#293462",font=('Helvetica', 12, "bold"))
        self.data_label.pack()

        self.Fav = tk.StringVar(self)
        if(self.a.get() in favorites_list):
            self.Fav.set("Saved in favorites!")
            self.fav_button = tk.Button(self, textvariable=self.Fav, command=lambda: self.favorite())
            self.fav_button.pack()
            self.fav_button.configure(bg="#216583", activebackground="#0880af", fg="white", activeforeground="#fcfbdd")
        else:
            self.Fav.set("Add to favorites")
            self.fav_button = tk.Button(self, textvariable=self.Fav, command=lambda: self.favorite())
            self.fav_button.pack()
            self.fav_button.configure(fg="#216583", activeforeground="#0880af", bg="#fff1c1", activebackground="#fcfbdd")

        self.img = ImageTk.PhotoImage(Image.open("Images/test0.png"))
        self.lab = tk.Label(self, image=self.img)
        self.lab.image = self.img
        self.lab.pack()

        self.a.trace("w", self.callback)

        tk.Label(self, text="\n\n").pack()
        tk.Button(self, text="Go back to parameters selection", bg="#f76262", activebackground="#ff8080", activeforeground="white", fg = "white",
                  command=lambda: master.switch_frame(Page_Parameter)).pack(side="bottom")

    def get_tests(self):
        self.test_count = 0
        self.test_list = []
        for file in os.listdir("Images/"):
            self.test_list.append(str(self.test_count))
            self.test_count = self.test_count+1 

    def callback(self,*args):
        global favorites_list
        self.csv_reader()
        # self.opt.configure(text="{}".format(self.a.get()))
        for i in range(0,self.test_count):

            if(self.a.get()==self.test_list[i]):
                if(self.a.get() in favorites_list):
                    self.Fav.set("Saved in favorites!")
                    self.fav_button.configure(bg="#216583", activebackground="#0880af", fg="white", activeforeground="#fcfbdd")
                else:
                    self.Fav.set("Add to favorites")
                    self.fav_button.configure(state="normal", fg="#216583", activeforeground="#0880af", bg="#fff1c1", activebackground="#fcfbdd")

                self.data_label['text']= "\n Average duration: "+durations_list[i] + "\n Standard deviation: " + std_list[i]
                self.img2 = ImageTk.PhotoImage(Image.open("Images/test"+str(i)+".png"))
                self.lab.configure(image=self.img2)
                self.lab.image = self.img2
        

    def csv_reader(self):
        global durations_list
        global std_list
        with open('CSV_Files/Summary.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if(line_count > 0):
                    durations_list.append(row[1])
                    std_list.append(row[2])
                line_count+=1

    def favorite(self):
        global favorites_list
        if(self.a.get() not in favorites_list):
            favorites_list.append(self.a.get())
            favorites_list.sort()
            self.Fav.set("Saved in favorites!")
            self.fav_button.configure(bg="#216583", activebackground="#0880af", fg="white", activeforeground="#fcfbdd")
        else:
            self.Fav.set("Add to favorites")
            self.fav_button.configure(fg="#216583", activeforeground="#0880af", bg="#fff1c1", activebackground="#fcfbdd")
            favorites_list.remove(self.a.get())
        print(favorites_list)
            

class PageGlobRes(tk.Frame):
    def __init__(self, master):
        self.audio_list=[]
        global file
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self)
        tk.Label(self, text="Global Results",fg = "#293462", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)

        self.back_btn = tk.Button(self, text="Back to test results", bg="#f76262", activebackground="#ff8080", activeforeground="white", fg = "white",
                  command=lambda: master.switch_frame(PageResults))
        self.back_btn.pack()
        
        tk.Label(self, text = "Favorites", fg = "#293462" , font=("Helvetica", 15, "bold")).pack()

        self.fav_frame = tk.Frame(self)
        self.fav_frame.pack()
        self.a = tk.StringVar(self.fav_frame)
        self.a.set(favorites_list[0])
        self.get_tests()
        self.menu = ttk.Combobox(self.fav_frame, textvariable=self.a, values = favorites_list)
        self.menu.pack(side="left")


        tk.Button(self.fav_frame, text = "Final selection", bg="#216583", activebackground="#0880af", fg="white", activeforeground="white", command=lambda: [self.all_param(), self.change_load()]).pack(side="left")

        self.loadfinal=tk.Label(self.fav_frame, text="")
        self.loadfinal.pack(side="left")


        self.fav_label = tk.Label(self, text="Test    |   Average duration   |   Standard deviation\n", fg="#293462")
        self.fav_label.pack()
        self.favorite_data()
        #########################################################################################

        self.frame_final = tk.Frame(self)



        self.final_test = tk.Frame(self)
        self.final_test.pack()
        self.audio_file = tk.StringVar(self.final_test)
        self.audio_file.set("out001.wav")
        self.menu2 = ttk.Combobox(self.final_test, textvariable=self.audio_file, values = self.audio_list)
        self.btn1 = tk.Button(self.frame_final, text="Listen to selected test", bg="#216583", activebackground="#0880af", fg="white", activeforeground="white", command=lambda: test.play_audio(self.audio_file.get()))
        self.btn2 = tk.Button(self.frame_final, text="Exit", bg="#f76262", activebackground="#ff8080", activeforeground="white", fg = "white", command=lambda: quit())


        self.img_frame = tk.Frame(self)
        self.img_frame.pack(side="bottom")
        self.img = ImageTk.PhotoImage(Image.open("Images_Global/Plot_Av_Dur.png"))
        self.lab = tk.Label(self.img_frame, image=self.img)
        self.lab.image = self.img
        self.lab.pack(side="left")


        self.img2 = ImageTk.PhotoImage(Image.open("Images_Global/STD.png"))
        self.lab2 = tk.Label(self.img_frame, image=self.img2)
        self.lab2.image = self.img2
        self.lab2.pack(side="right")

        
    def read_files(self):
        self.audio_list=[]
        for filename in os.listdir("splitted/"):
            self.audio_list.append(filename)
        self.audio_list.sort()
        self.show_final_buttons()


    def show_final_buttons(self):
        self.menu2.pack(side="left")
        self.menu2.configure(values=self.audio_list)
        self.back_btn.pack_forget()
        self.frame_final.pack()
        self.btn1.pack(side="left")
        self.btn2.pack(side="right")


    def get_tests(self):
        self.test_count = 0
        self.test_list = []
        for file in os.listdir("Images/"):
            self.test_list.append(str(self.test_count))
            self.test_count = self.test_count+1

    def favorite_data(self):
        for i in favorites_list:
            self.fav_label["text"] += i + "                   " + durations_list[int(i)] + "                     " + std_list[int(i)] + "      \n"

    def change_load(self):
        self.loadfinal["text"]="Loading segmentation..."
        self.after(1000, self.run)
    
    def run(self):
        test.run_selected_test(file, int(self.a.get()), self.final_sil, self.final_snd, self.final_th)
        self.loadfinal["text"]="Final segmentation done!"
        self.read_files()


    def all_param(self): 
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



class ListenFinal(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self)
        self.read_files()
        tk.Label(self, text="Test listening\n\n",fg = "#293462", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)

        self.fav_frame = tk.Frame(self)
        self.fav_frame.pack()
        self.a = tk.StringVar(self.fav_frame)
        self.a.set("out001.wav")
        self.menu = ttk.Combobox(self.fav_frame, textvariable=self.a, values = self.audio_list)
        self.menu.pack(side="left")

        tk.Button(self.fav_frame, text = "Play audio file", bg="#216583", activebackground="#0880af", fg="white", activeforeground="white", command=lambda: [test.play_audio(self.a.get())]).pack(side="right")
    
    def read_files(self):
        self.audio_list=[]
        for filename in os.listdir("splitted/"):
            self.audio_list.append(filename)
        self.audio_list.sort()
            

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()

