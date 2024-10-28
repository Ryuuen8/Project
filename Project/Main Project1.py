from tkinter import *
from tkinter import filedialog
import pygame
import os
from PIL import Image, ImageTk
from ttkbootstrap.constants import *
import customtkinter as ctk
import random


class SharedData:
    def __init__(self):
        self.songs = self.load_songs()
        self.ringtones = [os.path.basename(song) for song in self.songs]
        self.current_ringtone_index = 0
        self.current_song = None

    def load_songs(self):
        try:
            with open("songs.txt", "r", encoding="utf-8") as file:
                songs = file.read().splitlines()
                return songs
        except FileNotFoundError:
            return [] 


class IntroWindow:
    def __init__(self, root, shared_data):
        self.icon = PhotoImage(file=r'Images\eye.png')

        self.img = Image.open(r'Images\eye.png')
        self.resized_image = self.img.resize((70, 50))
        self.image = ImageTk.PhotoImage(self.resized_image)

        self.root = root
        self.shared_data = shared_data
        self.root.configure(bg="#e6c9f5")
        self.root.iconphoto(False,self.icon)
        self.root.title("EyeEase")
        self.root.geometry("640x480")
        self.center_window(640, 480)

        self.frame = Frame(root, bg="#e6c9f5")
        self.frame.place(relx=0.5, rely=0.5, anchor="s")

        self.main_label = Label(self.frame, text="Welcome to EyeEase", font=("Playfair", 24), bg="#e6c9f5")
        self.main_label.grid(row=0, column=0, pady=20)

        self.main_image = Label(self.root, image=self.image, text=None)
        self.main_image.place(relx=0.25, rely=0.28, anchor='e')

        self.next_button = Button(self.frame, text="Proceed", command=self.intro, bg="#2F3C7E", borderwidth=0)
        self.next_button.grid(row=1, column=0, pady=20)
        self.style_button(self.next_button)

    def style_button(self, button):
        button.config(relief="flat", bg="#FFB3C1")
        button.bind("<Enter>", lambda e: button.config(bg="#FF9AAB"))
        button.bind("<Leave>", lambda e: button.config(bg="#FFB3C1"))

    def intro(self):
        paragraph_text = (
            """Thank you for taking better care of your eyes right now!
            
            Avoid eyestrains and lessen the risk of developing eye illnesses by following the simple 20-20-20 rule!"""
        )

        self.intro_label = Label(self.frame, text=paragraph_text, wraplength=350, justify="left", bg="#e6c9f5", font=("Playfair", 15))
        self.intro_label.grid(pady=20)

        self.hide_widgets([self.main_image,self.main_label, self.next_button])

        self.main_button_frame1 = Frame(self.root, bg="#56a1cc")
        self.main_button_frame1.grid(pady=10)

        self.next_button1 = Button(self.frame, text="Proceed", command=self.next_window, bg="#2F3C7E", borderwidth=0)
        self.next_button1.grid(padx=5)
        self.style_button(self.next_button1)

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def hide_widgets(self, widgets):
        for widget in widgets:
            widget.pack_forget()
            widget.grid_forget()
            widget.place_forget()

    def next_window(self):
        self.timer_window = TimerWindow(self.root, self.shared_data)
        self.timer_window.reset_buttons()
        self.hide_widgets([self.intro_label, self.main_button_frame1, self.next_button1])

class TimerWindow:
    def __init__(self, root, shared_data):
        self.root = root
        self.shared_data = shared_data
        self.root.geometry("380x200")
        self.center_window(380, 200)
        self.root.resizable(False, False) 

        pygame.init()

        self.timer_running = False
        self.paused = False      
        
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=0)

        self.label_frame = ctk.CTkFrame(self.root, height=70, width=230, border_width=2, fg_color='#e6c9f5',border_color="#000000")
        self.label_frame.grid(row=0, column=0, sticky=N, padx=50, pady=10)

        self.question_label = ctk.CTkButton(self.root, text="?", font=("Arial", 30, "bold"), corner_radius=100, height=40, width=40, fg_color="#000000")
        self.question_label.place(relx=0.02, rely=0.19, anchor="w")

        self.main_label = ctk.CTkButton(
            self.root, 
            text="Are You\nReady?", 
            font=("Arial", 26), 
            corner_radius=0, 
            height=100, 
            width=300,
            fg_color="#FFFFFF",
            text_color="#000000",
            border_color="#000000",
            border_width=2,
        )
        self.main_label.place(relx=0.5, rely=0.7, anchor="center")

        self.yes_button = ctk.CTkButton(
            self.root, 
            text="Yes", 
            font=("Arial", 26), 
            corner_radius=0, 
            fg_color="#FFFFFF",
            text_color="#000000",
            border_color="#000000",
            height=100, 
            width=150,
            border_width=2,
            command=self.start_timer
        )
        self.no_button = ctk.CTkButton(
            self.root, 
            text="No", 
            font=("Arial", 26), 
            corner_radius=0,
            fg_color="#FFFFFF",
            text_color="#000000",
            border_color="#000000",
            height=100, 
            width=150,
            border_width=2,
            command=self.reset_buttons
        )

        '''self.reset_button = ctk.CTkButton(self.root, text="Reset", font=("Arial", 14),command=self.reset_timer, 
                                          width=6, fg_color="#2F3C7E")
        self.reset_button.place(relx=0.64, rely=0.55, anchor="center")'''

        '''self.pause_button = ctk.CTkButton(self.root, text="Pause", font=("Arial",14), width=5, command=self.pause_timer, fg_color="#2F3C7E")
        self.pause_button.place(relx=0.36, rely=0.55, anchor="center")'''

        self.next_button = ctk.CTkButton(self.root, text="►", font=("Arial", 18), width=10, height=10, fg_color="#000000", command=self.next_window1)
        self.next_button.place(relx=0.99,rely=0.5, anchor="e")

        self.main_label.bind("<Enter>", self.on_enter)

        self.yes_button.bind("<Leave>", self.on_leave)
        self.no_button.bind("<Leave>", self.on_leave)

        self.running = False
        self.elapsed_time = 10
        self.current_song = None

    def style_button(self, button):

        button.bind("<Enter>", lambda e: button.configure())
        button.bind("<Leave>", lambda e: button.configure())

    def on_enter(self, event):
        if not self.timer_running:
            self.yes_button.place(relx=0.45, rely=0.7, anchor="e")
            self.no_button.place(relx=0.9, rely=0.7, anchor="e")
            self.main_label.place_forget()

    def reset_buttons(self):
        self.yes_button.place_forget()
        self.no_button.place_forget()
        self.main_label.place(relx=0.5, rely=0.7, anchor="center")
        self.style_button(self.yes_button)
        self.style_button(self.no_button)

    def on_leave(self, event):
        self.reset_buttons()

    def update_timer(self):
        if self.running and self.elapsed_time > 0:
            self.elapsed_time -= 1
            self.main_label.configure(text=self.format_time(self.elapsed_time))
            self.root.after(1000, self.update_timer)
        elif self.elapsed_time <= 0:
            self.main_label.configure(text="Time's Up")
            self.pop_up_window = TimeUp(self.root, self.shared_data)
            self.root.withdraw()
            if self.shared_data.current_song and os.path.exists(self.shared_data.current_song):
                pygame.mixer.music.load(self.shared_data.current_song)
                pygame.mixer.music.play()
            else:
                print(f"File not found: {self.shared_data.current_song}")
                self.running = False

    def start_timer(self):
        if not self.running:
            self.timer_running = True
            if self.elapsed_time <= 0:
                return
            self.running = True
            self.update_timer()

    def pause_timer(self):
        if self.paused:
            self.paused = False
            self.start_timer()
            self.pause_button.configure(text="Pause")
        else:
            self.paused = True
            self.running = False
            self.pause_button.configure(text="Resume")

    def reset_timer(self):
        self.running = False
        self.elapsed_time = 10
        self.main_label.configure(text="Are You Ready?")
        self.timer_running = False 
        pygame.mixer.music.stop()

    def format_time(self, elapsed_time):
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    
    def play_ringtone(self):
        if self.shared_data.current_song and os.path.exists(self.shared_data.current_song):
            pygame.mixer.music.load(self.shared_data.current_song)
            pygame.mixer.music.play()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def volume_adjust(self):
        pass

    def hide_widget1(self,widgets):
        for widget in widgets:
            widget.place_forget()
            widget.grid_forget()
            widget.pack_forget()

    def next_window1(self):
        self.hide_widget1([self.question_label, self.main_label, self.yes_button, self.no_button, self.next_button, self.label_frame])
        self.timer_window = Ringtone(self.root, self.shared_data)
        self.root.withdraw()


class TimeUp:
    def __init__(self, root, shared_data):
        self.root = Toplevel(root)
        self.shared_data = shared_data
        self.root.geometry("400x250")
        self.center_window(400, 250)       
        self.root.configure(bg="#d9a7e0")
        self.root.attributes("-topmost", True)
        pygame.init()

        self.tu_frame = ctk.CTkFrame(self.root, fg_color="#e6c9f5", height=150, width=300)
        self.tu_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        self.tu_label = ctk.CTkLabel(self.tu_frame, text=r"TIME'S UP", text_color="#000000", font=("Arial", 40, "bold"))
        self.tu_label.place(relx=0.5, rely=0.5, anchor="center")
        
        self.tu_dismiss = ctk.CTkButton(self.tu_frame, fg_color="#e6c9f5", text="Dismiss", text_color="#000000", font=("Arial", 14), border_width=1, border_color="#000000",
                                        command=self.dismiss)
        self.tu_dismiss.place(relx=0.5, rely=0.8, anchor="center")
        
        self.skip_button = ctk.CTkButton(self.root, text="Skip", fg_color="#e6c9f5", text_color="#000000", font=("Arial", 16))
        self.skip_button.place(relx=0.7, rely=0.9, anchor="center")
        
    def dismiss(self):
        self.hide_widgets([self.tu_frame, self.skip_button])
        pygame.mixer.music.stop()
        self.close_eye = ClosEye(self.root, self.shared_data)
        self.root.withdraw()
        
    def hide_widgets(self, widgets):
        for widget in widgets:
            widget.place_forget()
            
    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.root.geometry(f"{width}x{height}+{x}+{y}")
            
class ClosEye:
    def __init__(self, root, shared_data):
        self.root = Toplevel(root)
        self.root.geometry("400x250")
        self.shared_data = shared_data
        self.center_window(400, 250)
        self.root.configure(bg="#d9a7e0")
        
        self.running = False
        self.elapsed_time = 20
        self.timer_running = False
        
        pygame.init()
        
        self.ce_frame = ctk.CTkFrame(self.root, fg_color="#e6c9f5", height=150, width=300)
        self.ce_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        self.ce_label = ctk.CTkLabel(self.ce_frame, text="CLOSE YOUR EYES", text_color="#000000", font=("Arial", 25, "bold"))
        self.ce_label.place(relx=0.5, rely=0.4, anchor="center")
        
        self.ce_timer = ctk.CTkButton(self.ce_frame, text="00:00:20", fg_color="#e6c9f5", text_color="#000000", font=("Arial", 20, "bold"),command=self.ce_start, height=50)
        self.ce_timer.place(relx=0.5, rely=0.7, anchor="center")
        
        self.skip_button = ctk.CTkButton(self.root, text="Skip", fg_color="#e6c9f5", text_color="#000000", font=("Arial", 16), command=self.skip)
        self.skip_button.place(relx=0.7, rely=0.9, anchor="center")
        
    def skip(self):
        self.hide_widgets = ([self.ce_frame, self.skip_button])
        self.la_window = LookAway(self.root, self.shared_data)
        self.root.withdraw()
        
    def hide_widgets(self, widgets):
        for widget in widgets:
            widget.place_forget()
        
    def ce_start(self):
        if not self.running:
            self.timer_running = True
            if self.elapsed_time <= 0:
                return
            self.running = True
            self.update_timer()
                
    def update_timer(self):
        if self.running and self.elapsed_time > 0:
            self.elapsed_time -= 1
            self.ce_timer.configure(text=self.format_time(self.elapsed_time))
            self.root.after(1000, self.update_timer)
        elif self.elapsed_time <= 0:
            self.ce_timer.configure(text="Time's Up!!!!")
            self.ce_label.configure(text="OPEN YOUR EYES NOW!!", font=("Arial", 20, "bold"))
            pygame.mixer.music.load("Musics/telolet_rem_truk_bus.mp3")
            pygame.mixer.music.play()
        else:
            self.running = False
                
    def format_time(self, elapsed_time):
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    
    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
class LookAway:
    def __init__(self,root, shared_data):
        self.root = Toplevel(root)
        self.shared_data = shared_data
        self.root.geometry("400x250")
        self.center_window(400, 250)
        self.root.configure(bg="#d9a7e0")
        
        self.running = False
        self.elapsed_time = 20
        self.timer_running = False
        
        self.la_frame = ctk.CTkFrame(self.root, fg_color="#e6c9f5", height=150, width=300)
        self.la_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        self.la_label = ctk.CTkLabel(self.la_frame, text="LOOK 20FT AWAY", text_color="#000000", font=("Arial", 25, "bold"), fg_color="#e6c9f5")
        self.la_label.place(relx=0.5, rely=0.4, anchor="center")
        
        
        self.la_timer = ctk.CTkButton(self.la_frame, text="00:00:20", fg_color="#e6c9f5", text_color="#000000", font=("Arial", 20, "bold"),command=self.la_start, height=50)
        self.la_timer.place(relx=0.5, rely=0.7, anchor="center")
        
        self.skip_button = ctk.CTkButton(self.root, text="Skip", fg_color="#e6c9f5", text_color="#000000", font=("Arial", 16), command=self.skip)
        self.skip_button.place(relx=0.7, rely=0.9, anchor="center")
        
    def skip(self):
        self.hide_widgets = ([self.la_frame, self.skip_button])
        self.r_window = Recommendation(self.root, self.shared_data)
        self.root.withdraw()
        
    def hide_widgets(self, widgets):
        for widget in widgets:
            widget.place_forget()
        
    def la_start(self):
        if not self.running:
            self.timer_running = True
            if self.elapsed_time <= 0:
                return
            self.running = True
            self.update_timer()
                
    def update_timer(self):
        if self.running and self.elapsed_time > 0:
            self.elapsed_time -= 1
            self.la_timer.configure(text=self.format_time(self.elapsed_time))
            self.root.after(1000, self.update_timer)
        elif self.elapsed_time <= 0:
            self.la_timer.configure(text=r"TIME'S UP!")
            pygame.mixer.music.load("Musics/telolet_rem_truk_bus.mp3")
            pygame.mixer.music.play()
        else:
            self.running = False
            
    def format_time(self, elapsed_time):
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    
    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    
    
class Recommendation:
    def __init__(self, root, shared_data):
        self.root = Toplevel(root)
        self.shared_data = shared_data
        self.root.geometry("500x350")
        self.center_window(500, 350)
        self.root.configure(bg="#d9a7e0")
        
        self.running = False
        self.elapsed_time = 20
        self.timer_running = False
        
        self.r_frame = ctk.CTkFrame(self.root, height=250, width=350, fg_color="#e6c9f5")
        self.r_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        self.r_label = ctk.CTkLabel(self.r_frame, text="We Recommend Resting Away \nFrom Gadgets For:\n", font=("Arial", 20,"bold"))
        self.r_label.place(relx=0.5, rely=0.2, anchor="center")
        
        self.r_recommend = ctk.CTkLabel(self.r_frame,text="• Zero Eye Stain\n• Better Focus\n• Better Productivity", font=("Arial", 20), justify="left")
        self.r_recommend.place(relx=0.3, rely=0.4, anchor="center")
        
        self.r_timer = ctk.CTkButton(self.r_frame, text="00:00:20", fg_color="#e6c9f5", text_color="#000000", font=("Arial", 20, "bold"),command=self.r_start, height=50)
        self.r_timer.place(relx=0.5, rely=0.7, anchor="center")
        
        self.skip_button = ctk.CTkButton(self.root, text="Skip", fg_color="#e6c9f5", text_color="#000000", font=("Arial", 16), command=self.skip)
        self.skip_button.place(relx=0.7, rely=0.93, anchor="center")
        
    def skip(self):
        self.hide_widgets = ([self.r_frame, self.skip_button])
        self.o_window = Option(self.root, self.shared_data)
        self.root.withdraw()
        
    def hide_widgets(self, widgets):
        for widget in widgets:
            widget.place_forget()
        
    def r_start(self):
        if not self.running:
            self.timer_running = True
            if self.elapsed_time <= 0:
                return
            self.running = True
            self.update_timer()
                
    def update_timer(self):
        if self.running and self.elapsed_time > 0:
            self.elapsed_time -= 1
            self.r_timer.configure(text=self.format_time(self.elapsed_time))
            self.root.after(1000, self.update_timer)
        elif self.elapsed_time <= 0:
            self.r_timer.configure(text=r"TIME'S UP!")
            pygame.mixer.music.load("Musics/telolet_rem_truk_bus.mp3")
            pygame.mixer.music.play()
        else:
            self.running = False
            
    def format_time(self, elapsed_time):
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    
    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
class Option:
    def __init__(self,root, shared_data):
        self.root = Toplevel(root)
        self.shared_data = shared_data
        self.root.geometry("500x300")
        self.center_window(500, 300)
        self.root.configure(bg="#d9a7e0")
        
        self.o_frame = ctk.CTkFrame(self.root, height=200, width=400,  fg_color="#e6c9f5")
        self.o_frame.place(rely=0.5, relx=0.5, anchor="center")
        
        self.o_label = ctk.CTkLabel(self.o_frame, text=r"Let's take care of your eyes again!", font=("Arial", 24, "bold"))
        self.o_label.place(relx=0.5, rely=0.1, anchor="center")
        
        self.o_yes = ctk.CTkButton(self.o_frame, text="Yes", fg_color="#e6c9f5", text_color="#000000", font=("Arial", 18, "bold"),width=70, height=70, 
                                   border_width=2, border_color="#000000", command=self.yes_button)
        self.o_yes.place(rely=0.4, relx=0.2, anchor="center")
            
        self.yes_label = ctk.CTkLabel(self.o_frame, text="Let's take care \nof my eyes", text_color="#000000")
        self.yes_label.place(rely=0.65, relx=0.2, anchor="center")
        
        self.o_no = ctk.CTkButton(self.o_frame, text="No", fg_color="#e6c9f5", text_color="#000000", font=("Arial", 18, "bold"),width=70, height=70, 
                                  border_width=2, border_color="#000000", command=self.no_button)
        self.o_no.place(rely=0.4, relx=0.8, anchor="center")
        
        self.no_label = ctk.CTkLabel(self.o_frame, text="I don't want reminders \nto take care of my eyes", text_color="#000000")
        self.no_label.place(rely=0.65, relx=0.8, anchor="center")
        
    def yes_button(self):
        self.timer_window = TimerWindow(self.root, self.shared_data)
        self.timer_window.reset_buttons()
        self.hide_widgets([self.o_frame])
        
    def hide_widgets(self, widgets):
        for widget in widgets:
            widget.place_forget()
            
    def no_button(self):
        self.hide_widgets([self.o_frame])
        self.o1_window = Option1(self.root, self.shared_data)
        self.root.withdraw()
        
    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
class Option1:
    def __init__(self, root, shared_data):
        self.root = Toplevel(root)
        self.shared_data = shared_data
        self.root.geometry("500x300")
        self.center_window(500, 300)
        self.root.configure(bg="#d9a7e0")
        
        self.o1_frame = ctk.CTkFrame(self.root, height=240, width=400,  fg_color="#e6c9f5")
        self.o1_frame.place(rely=0.5, relx=0.5, anchor="center")
        
        self.o1_label = ctk.CTkLabel(self.o1_frame, text="Are You Sure You Don't Want To \nTake Care of Your Eyes?", text_color="#FF0000", font=("Arial", 24,"bold"))
        self.o1_label.place(rely=0.1, relx=0.5, anchor="center")
        
        self.o1_yes = ctk.CTkButton(self.o1_frame, text="Yes", fg_color="#e6c9f5", text_color="#000000", font=("Arial", 18, "bold"),width=70, height=70, 
                                   border_width=2, border_color="#000000", command=self.yes_button)
        self.o1_yes.place(rely=0.4, relx=0.8, anchor="center")
        
        self.yes_label = ctk.CTkLabel(self.o1_frame, text="I changed my mind. Let's \ntake care of my eyes", text_color="#000000")
        self.yes_label.place(rely=0.65, relx=0.2, anchor="center")
        
        self.o1_no = ctk.CTkButton(self.o1_frame, text="No", fg_color="#e6c9f5", text_color="#000000", font=("A ", 18, "bold"),width=70, height=70, 
                                  border_width=2, border_color="#000000", command=self.no_button)
        self.o1_no.place(rely=0.4, relx=0.2, anchor="center")
        
        self.no_label = ctk.CTkLabel(self.o1_frame, text="I don't want to take \ncare of my eyes", text_color="#000000")
        self.no_label.place(rely=0.65, relx=0.8, anchor="center")
        
    def yes_button(self):
        self.hide_widgets([self.o1_frame])
        self.fo_window = FOption(self.root, self.shared_data)
        self.root.withdraw()
    
    def no_button(self):
        self.hide_widgets([self.o1_frame])
        self.timer_window = TimerWindow(self.root, self.shared_data)
        self.timer_window.reset_buttons()
    
    def hide_widgets(self, widgets):
        for widget in widgets:
            widget.place_forget()
        
    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
class FOption:
    def __init__(self,root, shared_data):
        self.root = Toplevel(root)
        self.shared_data = shared_data
        self.root.geometry("500x300")
        self.center_window(500, 300)
        self.root.configure(bg="#d9a7e0")
        
        self.fo_frame = ctk.CTkFrame(self.root, height=240, width=400,  fg_color="#e6c9f5")
        self.fo_frame.place(rely=0.5, relx=0.5, anchor="center")
        
        self.fo_label = ctk.CTkLabel(self.fo_frame, text="You Might Develop One Of The Following: ", text_color="#000000", font=("Arial", 20,"bold"))
        self.fo_label.place(rely=0.1, relx=0.5, anchor="center")
        
        self.fo_d = ctk.CTkLabel(self.fo_frame, text="Eye Strains|Dry Eyes|Eye Fatigue|Blurred Vision", text_color="#FF0000", font=("Arial", 15, "bold"))
        self.fo_d.place(rely=0.2, relx=0.5, anchor="center")
        
        self.fo_yes = ctk.CTkButton(self.fo_frame, text="Yes", fg_color="#e6c9f5", text_color="#000000", font=("Arial", 18, "bold"),width=70, height=70, 
                                   border_width=2, border_color="#000000",)
        self.fo_yes.place(rely=0.4, relx=0.8, anchor="center")
        
        self.yes_label = ctk.CTkLabel(self.fo_frame, text="I changed my mind. Let's \ntake care of my eyes", text_color="#000000")
        self.yes_label.place(rely=0.65, relx=0.2, anchor="center")
        
        self.fo_no = ctk.CTkButton(self.fo_frame, text="No", fg_color="#e6c9f5", text_color="#000000", font=("A ", 18, "bold"),width=70, height=70, 
                                  border_width=2, border_color="#000000",)
        self.fo_no.place(rely=0.4, relx=0.2, anchor="center")
        
        self.no_label = ctk.CTkLabel(self.fo_frame, text="I don't want to take \ncare of my eyes", text_color="#000000")
        self.no_label.place(rely=0.65, relx=0.8, anchor="center")
        
        
    def yes_button(self):
        self.root.destroy()
        
    def no_button(self):
        self.hide_widgets([self.fo_frame])
        self.timer_window = TimerWindow(self.root, self.shared_data)
        self.timer_window.reset_buttons()
        
    def hide_widgets(self, widgets):
        for widget in widgets:
            widget.place_forget()
        
    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        
class Ringtone:
    def __init__(self, root, shared_data):
        self.root = Toplevel(root)
        self.shared_data = shared_data
        self.root.config(background="#e6c9f5")
        self.root.title("EyeEase")
        self.root.geometry("400x250")
        self.root.resizable(False, False) 
        self.center_window(400, 250)
        
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=0)

        self.add_image = ctk.CTkImage(Image.open(r'Images\Add.png'), size=(50,50))
        self.random_icon = ctk.CTkImage(Image.open(r'Images\pngegg.png'), size=(50,50))
        
        self.question_label = ctk.CTkButton(self.root, text="?", font=("Arial", 30, "bold"), corner_radius=100, height=40, width=40, fg_color="#000000")
        self.question_label.place(relx=0.05, rely=0.15, anchor="w")
        
        self.label_frame = ctk.CTkFrame(self.root, height=50, width=280, border_width=2, fg_color='#e6c9f5',border_color="#000000")
        self.label_frame.place(relx=0.6, rely=0.15, anchor="center")

        self.frame = ctk.CTkFrame(self.root, border_width=3, height=50, fg_color="#FFFFFF", width=170, border_color="#000000")
        self.frame.place(relx=0.5, rely=0.4, anchor="center")
        
        self.ringtone_label = ctk.CTkLabel(
            self.frame,
            text=f"",
            font=("Arial", 10, "bold"),
        )
        self.ringtone_label.place(relx=0.5, rely=0.5, anchor="center")

        self.next_button1 = ctk.CTkButton(self.root, text=">", font=("Arial", 20, "bold"), width=25, command=self.next_ringtone, height=50, text_color="#000000",
                                           fg_color="#e6c9f5")
        self.next_button1.place(relx=0.744, rely=0.4, anchor="center")

        self.prev_button = ctk.CTkButton(self.root, text="<", font=("Arial", 20, "bold"), width=25, command=self.prev_ringtone, height=50, text_color="#000000",
                                          fg_color="#e6c9f5")
        self.prev_button.place(relx=0.256, rely=0.4, anchor="center")

        self.play_button = ctk.CTkButton(self.root, text="Play", command=self.play, width=3, text_color="#000000",
                                          fg_color="#e6c9f5", border_color="#000000", border_width=2)
        self.play_button.place(relx=0.3, rely=0.57, anchor="center")

        self.stop_button = ctk.CTkButton(self.root, text="Stop", command=self.stop, width=3, text_color="#000000",
                                          fg_color="#e6c9f5", border_color="#000000", border_width=2)
        self.stop_button.place(relx=0.7, rely=0.57, anchor="center")

        self.select_button = ctk.CTkButton(self.root, text="Select", command=self.select_song, width=3, text_color="#000000",
                                            fg_color="#e6c9f5", border_color="#000000", border_width=2)
        self.select_button.place(relx=0.5, rely=0.57, anchor="center")

        self.next_button = ctk.CTkButton(self.root, text="◄", font=("Arial", 18), width=10, height=10, fg_color="#2F3C7E", command=self.prev_window)
        self.next_button.place(relx=0.01, rely=0.5, anchor="w")

        self.add_button = ctk.CTkButton(self.root, image=self.add_image, text=None, command=self.add_song, height=80, width=80, fg_color="#FFFFFF",
                                         border_width=2, border_color="#000000")
        self.add_button.place(relx=0.88, rely=0.8, anchor="center")

        self.random_button = ctk.CTkButton(self.root, image=self.random_icon, text=None, command=self.random_song, height=80, width=80, fg_color="#FFFFFF",
                                             border_color="#000000", border_width=2)
        self.random_button.place(relx=0.88, rely=0.45, anchor="center")
        
        self.vl_frame = ctk.CTkFrame(self.root, width=250, height=40, border_width=2, border_color="#000000", corner_radius=10)
        self.vl_frame.place(relx=0.5, rely=0.8, anchor="center")
        
        self.volume = ctk.CTkLabel(self.root, text="🔊", font=("Arial", 40))
        self.volume.place(relx=0.18, rely=0.77, anchor="center")
        
        self.volume_slider = ctk.CTkSlider(self.vl_frame, orientation="horizontal", from_=0, to=100, command=self.volume_adjust)
        self.volume_slider.pack(pady=10, padx=5)
        
    def volume_adjust(self, event=None):
        self.volume_level = self.volume_slider.get() / 100
        pygame.mixer.music.set_volume(self.volume_level)

    def next_ringtone(self):
        if self.shared_data.ringtones:
            self.shared_data.current_ringtone_index = (self.shared_data.current_ringtone_index + 1) % len(self.shared_data.ringtones)
            self.update_ringtone()
        else:
            print("No Ringtone Available")

    def prev_ringtone(self):
        if self.shared_data.ringtones:
            self.shared_data.current_ringtone_index = (self.shared_data.current_ringtone_index - 1) % len(self.shared_data.ringtones)
            self.update_ringtone()
        else:
            print("No Ringtone Available")

    def update_ringtone(self):
        if not self.shared_data.ringtones:
            self.ringtone_label.configure(text="No Available Ringtone", font=("Playfair", 15))
        else:
            current_ringtone_name = self.shared_data.ringtones[self.shared_data.current_ringtone_index]

            if isinstance(current_ringtone_name, tuple):
                current_ringtone_name = current_ringtone_name[0]

            current_ringtone_name = os.path.splitext(current_ringtone_name)[0]
            self.ringtone_label.configure(text=current_ringtone_name, font=("Segoe UI", 15))


    def select_song(self):
        self.shared_data.current_song = self.shared_data.songs[self.shared_data.current_ringtone_index]
        print(f"{self.shared_data.current_song} Selected.")

    def random_song(self):
        if self.shared_data.ringtones:
            self.shared_data.current_ringtone_index = random.randint(0, len(self.shared_data.ringtones) - 1)
            self.update_ringtone()
            print(f"Randomly selected: {self.shared_data.ringtones[self.shared_data.current_ringtone_index]}")
        else:
            print("No ringtones available to select.")


    def prev_window(self):
        self.timer_window = TimerWindow(self.root, self.shared_data)
        self.timer_window.reset_buttons()
        self.hide_widget1([self.label_frame, self.question_label, self.random_button, self.ringtone_label, 
                           self.next_button1, self.prev_button, self.play_button, self.stop_button, 
                           self.select_button, self.next_button, self.frame, self.add_button, self.vl_frame,
                           self.volume])

    def hide_widget1(self,widgets):
        for widget in widgets:
            widget.place_forget()
            widget.pack_forget()
            widget.grid_forget()

    def play(self):
        current_song = self.shared_data.songs[self.shared_data.current_ringtone_index]
        print(f"Attempting to play: {current_song}")
        if os.path.exists(current_song):
            print(f"Loading song: {current_song}")
            pygame.mixer.music.load(current_song)
            pygame.mixer.music.play()
        else:
         print(f"File not found: {current_song}")
        
    def stop(self):
        pygame.mixer.music.stop()


    def save_song(self, song_path):
        with open("songs.txt", "a", encoding="utf-8") as file:
            file.write(song_path + "\n") 

    def update_songs_file(self):
        with open("songs.txt", "w", encoding="utf-8") as file:
            for song in self.songs:
                file.write(song + "\n")

    def add_song(self):
        song_path = filedialog.askopenfilename(title="Select a Song", filetypes=(("MP3 Files", "*.mp3"), ("All Files", "*.*")))
        if song_path:
            print(f"Selected song path: {song_path}")
            song_name = os.path.basename(song_path)
            self.shared_data.songs.append(song_path)
            self.shared_data.ringtones.append(os.path.splitext(os.path.basename(song_path)))
            self.save_song(song_path)


    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        

if __name__ == "__main__":
    root = Tk()
    root.resizable(False,False)
    shared_data = SharedData()
    timer_app = IntroWindow(root,shared_data)
    root.mainloop()
