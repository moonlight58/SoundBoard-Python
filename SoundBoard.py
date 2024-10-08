#!/usr/bin/python3
########################################################################################################################
# ScriptName    : SoundBoard.py                                                                                        #
# Description   : Create/Edit/Delete a div that can play/stop a sound from a file                                      #
# Author        : Röthlin Gaël                                                                                         #
# Email         : gael.rothlin@proton.me                                                                               #
# NB            : I'm new to programming so it can be junking. Trying to improve my skills and this code too. It's not #
#                 finished and need to be optimised and less bad x) Have fun trying to read the code and maybe giving  #
#                 advise                                                                                               #
########################################################################################################################

import pygame
import pyaudio
import wave
import subprocess
import os
import time
import json
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo
from mutagen.mp3 import MP3
from pygame import mixer, _sdl2 as devicer

class SoundBoard(Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.sound_divs = []
        self.current_row = 1
        self.current_column = 0
        self.initUI()
        self.sound_file = None
        self.current_sound = None
        self.start_time = None
        self.sounds = []
        pygame.mixer.init()
        print(devicer.audio.get_audio_device_names(True))
        # print("Outputs:", devicer.audio.get_audio_device_names(False))
        mixer.init(devicename='Microphone (USB PnP Sound Device)')


    def initUI(self):
        menubar = Menu(self.master)

        menu1 = Menu(menubar, tearoff=0) # Menu1 "Create"
        menu1.add_command(label="From File", command=self.open_file)
        menubar.add_cascade(label="Create", menu=menu1)

        menu2 = Menu(menubar, tearoff=0) # Menu2 "Edit"
        menu2.add_command(label="Edit", command=self.edit_soundboard)
        menubar.add_cascade(label="Edit", menu=menu2)

        menu3 = Menu(menubar, tearoff=0) # Menu3 "Save/Load"
        menu3.add_command(label="Save Sounds", command=lambda: self.save_sounds('sounds.json'))
        menu3.add_command(label="Load Sounds", command=lambda: self.load_sounds('sounds.json'))
        menubar.add_cascade(label="Save/Load", menu=menu3)


        self.master.config(menu=menubar) # Menu initialization

    def open_file(self):
        file_path = askopenfilename(title="Choose the file to open", filetypes=[("MP3 files", "*.mp3")])
        if file_path:
            self.sound_file = file_path # Store the selected file path
            self.create_sound(self.sound_file)
        else:
            showinfo("Error", "No sound file selected.")

    def save_sounds(self, file_path):
        with open(file_path, 'w') as f:
            print(self.sounds)
            json.dump(self.sounds, f)

    def load_sounds(self, file_path):
        try:
            with open(file_path, 'r') as f:
                self.sounds = json.load(f)
            # After loading the sounds, you can display them in the user interface.
            for sound in self.sounds:
                print(self.sound_divs)
                self.set_sound(sound['name'], sound['file_path'])
        except FileNotFoundError:
            print("File not found.")
        except json.JSONDecodeError:
            print("Error decoding JSON from file.")
 
    def play_sound(self, file_path):
        if self.current_sound:
            self.current_sound.stop()
        try:
            self.current_sound_object = pygame.mixer.Sound(file_path)
            self.current_sound = self.current_sound_object.play()
            self.start_time = time.time()
            self.current_sound_file = file_path  # Store the current sound file path
            self.update_time_label()
        except pygame.error:
            showinfo("Error", "Failed to play the sound file.")

    def get_mp3_duration(self, file_path):
        audio = MP3(file_path)
        return audio.info.length

    def update_time_label(self):
        if self.current_sound and pygame.mixer.get_busy():
            elapsed_time = time.time() - self.start_time
            total_time = self.get_mp3_duration(self.current_sound_file)  # Use the current sound file path
            self.time_label.config(text=f"{elapsed_time:.2f} / {total_time:.2f} s")
            self.after(100, self.update_time_label)  # Update the label every 100 milliseconds
        else:
            total_time = self.get_mp3_duration(self.current_sound_file)  # Use the current sound file path
            self.time_label.config(text=f"0.00 / {total_time:.2f} s")

    def open_input_window(self):
        # Create a new window
        input_window = Toplevel(self.master)
        input_window.title("Enter Sound Name")

        # Create a text field
        input_field = Entry(input_window)
        input_field.pack(padx=10, pady=10)

        # Create a button to submit the input
        submit_button = Button(input_window, text="Submit",
                               command=lambda: self.set_name(input_field.get(), input_window))
        submit_button.pack(padx=10, pady=10)

        # Wait for the window to be closed
        self.master.wait_window(input_window)

    def set_name(self, name, input_window):
        self.name = name
        input_window.destroy()  # Close the input window after submitting the name

    def button_stop(self):
        if self.current_sound:
            self.current_sound.stop() # Stop the currently playing sound
            self.current_sound = None # Reset the sound reference
        else:
            showinfo("Warning", "No sound is currently playing.")

    def edit_soundboard(self):
        print("Editing soundboard...")

    def set_volume(self, volume, sound_object):
        sound_object.set_volume(int(volume) / 100)
        if self.current_sound and pygame.mixer.get_busy() and self.current_sound.get_name() == sound_object.get_name():
            self.current_sound.stop()
            self.current_sound.play()

    def create_sound(self, file_path):
        self.open_input_window()
        sound_object = pygame.mixer.Sound(file_path)
        self.set_sound(self.name, file_path)
        self.sounds.append({'name': self.name, 'file_path': self.sound_file, 'duration': self.get_mp3_duration(self.sound_file), 'sound_object': sound_object})

    def delete_sound(self, div_player):
        if self.current_sound:
            self.current_sound.stop()
        for i, sound_div in enumerate(self.sound_divs):
            if sound_div[0] == div_player:
                print(self.sound_divs)
                self.sound_divs.pop(i)
                break
        div_player.destroy()
        # Find the sound to delete by matching the file_path
        for sound in self.sounds[:]:  # Use a copy of the list to safely iterate and remove
            print(sound['file_path'])
            print(self.current_sound)
            print(sound['file_path'] == self.sound_file)
            if sound['file_path'] == self.sound_file:
                print(self.sounds)
                self.sounds.remove(sound)
                break


    def set_sound(self, name, file_path):
        total_time = self.get_mp3_duration(file_path)  # Use file_path instead of self.sound_file
        row = self.current_row
        column = 0

        Div_player = Frame(self.master, width=200, height=200, borderwidth=2, relief="groove")
        Div_player.grid(row=row, column=column, padx=10, pady=5)

        Label(Div_player, text=name).grid(row=0, column=0, pady=(10,0))

        Inside_Div = Frame(Div_player, width=(Div_player.winfo_reqwidth() * 0.90),
                           height=(Div_player.winfo_reqheight() * 0.5))
        Inside_Div.grid(row=2, column=0, padx=5, pady=5)

        Button_Play_Stop_Div = Frame(Inside_Div, width=Inside_Div.winfo_reqwidth(), height=Inside_Div.winfo_reqheight())
        Button_Play_Stop_Div.grid(row=0, column=0, padx=5)

        Play_Button = Button(Button_Play_Stop_Div, text="Play", command=lambda: self.play_sound(file_path))
        Play_Button.grid(row=0, column=0, padx=5, pady=5)

        Stop_Button = Button(Button_Play_Stop_Div, text="Stop", command=self.button_stop)
        Stop_Button.grid(row=0, column=1, padx=5, pady=5)

        # Create a label to display the time
        self.time_label = Label(Inside_Div, text=f"0.00 / {total_time:.2f} s")
        self.time_label.grid(row=1, column=0, padx=5, pady=5)

        # Create a slider for controlling volume
        sound_object = pygame.mixer.Sound(file_path)
        volume_slider = Scale(Inside_Div, from_=0, to=100, orient=HORIZONTAL, command=lambda volume: self.set_volume(volume, sound_object))
        volume_slider.grid(row=2, column=0, padx=5, pady=5)

        Delete_Button = Button(Inside_Div, text="Delete", command=lambda: self.delete_sound(Div_player))
        Delete_Button.grid(row=3, column=0, padx=5, pady=5)

        self.sound_divs.append(
            (Div_player, Inside_Div, Play_Button, Stop_Button, Button_Play_Stop_Div, Delete_Button, self.time_label, volume_slider))

        self.current_row += 1

def main():
    root = Tk()
    root.geometry("400x400")
    root.minsize(400,400)
    root.title("SoundBoard Test")
    root.resizable(True, True)
    app = SoundBoard(master=root)

    # Load saved sounds on startup
    app.load_sounds('sounds.json')

    root.mainloop()

if __name__ == '__main__':
    main()
