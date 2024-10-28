import tkinter as tk
from tkinter import ttk
import customtkinter
import pygame
pygame.mixer.init()

class App():

    def __init__(self):

        customtkinter.set_appearance_mode("System")
        customtkinter.set_default_color_theme("blue")

        self.root = tk.Tk()
        self.root.geometry('650x200')
        self.root.title('Eye Ease App')
        self.mainframe = tk.Frame(self.root, background='light blue')
        self.mainframe.pack(fill='both', expand=True)

        titletxt = customtkinter.CTkLabel(self.mainframe, text="WELCOME TO EYE EASE", font=("Bahnschrift SemiBold", 25), text_color="black")
        titletxt.place(anchor="center", relx=0.25, rely=0.2)

        settingbtn = customtkinter.CTkButton(self.mainframe, text="Settings", width=10, command=self.setting_page)
        settingbtn.place(relx=0.55, rely=0.13)
        aboutbtn = customtkinter.CTkButton(self.mainframe, text="About", width=10)
        aboutbtn.place(relx=0.69, rely=0.13)

        self.sound_options_dict = {
            "Ringtone 1": "C:\\Users\\NEP\\Documents\\COLLEGE FILES\\2ND YEAR\\PROJECT PROPOSAL PYTHON\\HOW TO MAKE APP\\ringtones\\kawaii ringtone 1.mp3",
            "Ringtone 2": "C:\\Users\\NEP\\Documents\\COLLEGE FILES\\2ND YEAR\\PROJECT PROPOSAL PYTHON\\HOW TO MAKE APP\\ringtones\\kawaii ringtone 2.mp3"
        }
        self.setcolor = customtkinter.CTkComboBox(self.mainframe, values=list(self.sound_options_dict.keys()))
        self.setcolor.place(relx=0.04, rely=0.4)
        soundbtn = customtkinter.CTkButton(self.mainframe, text="Play Sound", width=15, command=self.playsound)
        soundbtn.place(relx=0.3, rely=0.4)

        self.time_option = {"2 secs" : 2,
                            "5 secs" : 5,
                            "20 mins": 1200,
                            "30 mins": 1800,
                            "40 mins": 2400,
                            "50 mins": 3000 }
        self.settime = customtkinter.CTkComboBox(self.mainframe, values=list(self.time_option.keys()))
        self.settime.place(relx=0.55, rely=0.4)
        timerbtn = customtkinter.CTkButton(self.mainframe, text="Start Timer", width=15, command=self.start_time)
        timerbtn.place(relx=0.8, rely=0.4)

        

        

        self.remaining_seconds = 5

        self.root.mainloop()


    def playsound(self):
        selected_friendly_name = self.setcolor.get()

        if selected_friendly_name in self.sound_options_dict:
            sound_path = self.sound_options_dict[selected_friendly_name]
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play(loops=2)
        else:
            print("Invalid selection")

    def start_time(self):
        newtime = self.settime.get()
        try:
            self.remaining_seconds = self.time_option[newtime]
            self.update_timer()
        except ValueError:
            print("Invalid input")

    def update_timer(self):
        selected_friendly_name = self.setcolor.get()
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.root.after(1000, self.update_timer)
        elif selected_friendly_name in self.sound_options_dict:
            sound_path = self.sound_options_dict[selected_friendly_name]
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play(loops=1)
        else:
            print("Invalid Sound")

    def setting_page(self):
        
        self.setting_frame = customtkinter.CTkFrame(self.mainframe, fg_color="#7FA1C3", border_color="#6482AD", border_width=4)
        self.setting_frame.pack(fill='both', expand=True)

        backhomebtn = customtkinter.CTkButton(self.setting_frame, text="Back", width=15, bg_color="#7FA1C3", fg_color="#6482AD",command=self.homebtn)
        backhomebtn.place(relx=0.03, rely=0.1)

        slb = customtkinter.CTkLabel(self.setting_frame, text=  "Settings", font=("Bahnschrift SemiBold", 20))
        slb.place(relx=0.45, rely=0.1)

        voltxt = customtkinter.CTkLabel(self.setting_frame, text="Volume", font=("Bahnschrift SemiBold", 15))
        voltxt.place(relx=0.27, rely=0.25)
        self.volume_adjust = customtkinter.CTkSlider(self.setting_frame, from_=1, to=0, command=self.vladjust)
        self.volume_adjust.place(relx=0.35, rely=0.3)

        self.setting_frame.pack(pady=20)

    def homebtn(self):
        self.setting_frame.pack_forget()
        self.mainframe.pack(fill='both', expand=True)

    def vladjust(self, event=None):
        volume_level = self.volume_adjust.get() / 100  
        pygame.mixer.music.set_volume(volume_level)

    

if __name__ == '__main__':
    App()