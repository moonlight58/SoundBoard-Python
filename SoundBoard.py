#!/usr/bin/python3
########################################################################################################################
# ScriptName    : SoundBoard.py                                                                                        #
# Description   : Create/Edit/Delete a div that can play/stop a sound from a file path                                 #
# Author        : Röthlin Gaël                                                                                         #
# Email         : gael.rothlin@proton.me                                                                               #
# NB            : I'm new to programming so it can be junking. Trying to improve my skills and this code too. It's not #
#                 finished and need to be optimised and less bad x) Have fun trying to read the code and maybe giving  #
#                 advise                                                                                               #
########################################################################################################################

import pygame
import time
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo
from mutagen.mp3 import MP3

class Example(Frame):

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
        pygame.mixer.init()

    def initUI(self):
        menubar = Menu(self.master)

        menu1 = Menu(menubar, tearoff=0) # Menu1 "Create"
        menu1.add_command(label="From File", command=self.open_file)
        menubar.add_cascade(label="Create", menu=menu1)

        menu2 = Menu(menubar, tearoff=0) # Menu2 "Edit"
        menu2.add_command(label="Edit", command=self.edit_soundboard)
        menubar.add_cascade(label="Edit", menu=menu2)

        self.master.config(menu=menubar) # Initialisation du menu

    def open_file(self):
        file_path = askopenfilename(title="Choose the file to open", filetypes=[("MP3 files", "*.mp3")])
        if file_path:
            self.sound_file = file_path # Stocker le chemin du fichier sélectionné
            self.create_sound()
        else:
            showinfo("Error", "No sound file selected.")


    def button_sound(self):
        if self.current_sound:
            self.current_sound.stop()
            self.current_sound = None
            pygame.mixer.init()
            self.current_sound = pygame.mixer.Sound(self.sound_file)
            self.current_sound.play()
            self.start_time = time.time() # Enregistrer le moment où le son commence à jouer
            self.update_time_label() # Commencer à mettre à jour le label de temps
        else:
            if self.sound_file:
                try:
                    self.current_sound = pygame.mixer.Sound(self.sound_file)
                    self.current_sound.play()
                    self.start_time = time.time()
                    self.update_time_label()
                except pygame.error:
                    showinfo("Error", "Failed to play the sound file.")
            else:
                showinfo("Error", "No sound file selected.")

    def get_mp3_duration(self, file_path):
        audio = MP3(file_path)
        return audio.info.length

    def update_time_label(self):
        if self.current_sound and pygame.mixer.get_busy():
            elapsed_time = time.time() - self.start_time
            total_time = self.get_mp3_duration(self.sound_file)
            self.time_label.config(text=f"{elapsed_time:.2f} / {total_time:.2f} seconds")
            self.after(100, self.update_time_label)  # Mettre à jour le label toutes les 100 millisecondes
        else:
            total_time = self.get_mp3_duration(self.sound_file)
            self.time_label.config(text=f"{total_time:.2f} seconds")

    def open_input_window(self):
        # Créer une nouvelle fenêtre
        input_window = Toplevel(self.master)
        input_window.title("Enter Sound Name")

        # Créer un champ de texte
        input_field = Entry(input_window)
        input_field.pack(padx=10, pady=10)

        # Créer un bouton pour soumettre la saisie
        submit_button = Button(input_window, text="Submit",
                               command=lambda: self.set_name(input_field.get(), input_window))
        submit_button.pack(padx=10, pady=10)

        # Attendre que la fenêtre soit fermée
        self.master.wait_window(input_window)

    def set_name(self, name, input_window):
        self.name = name
        input_window.destroy()  # Fermer la fenêtre d'entrée après la soumission du nom

    def button_stop(self):
        if self.current_sound:
            self.current_sound.stop() # Arrêter le son actuellement joué
            self.current_sound = None # Réinitialiser la référence au son
        else:
            showinfo("Warning", "No sound is currently playing.")

    def edit_soundboard(self):
        print("Editing soundboard...")

    def create_sound(self):
        self.open_input_window()
        self.set_sound(self.name)

    def set_sound(self, name):
        total_time = self.get_mp3_duration(self.sound_file)
        row = self.current_row
        column = 0

        Div_player = Frame(self.master, width=200, height=200, borderwidth=2, relief="raised")
        Div_player.grid(row=row, column=column, padx=10, pady=5)

        Label(Div_player, text=name).grid(row=0, column=0, padx=5, pady=5)

        Inside_Div = Frame(Div_player, width=(Div_player.winfo_reqwidth() * 0.90),
                           height=(Div_player.winfo_reqheight() * 0.5), bg="purple")
        Inside_Div.grid(row=2, column=0, padx=5, pady=5)

        Button_Play_Stop_Div = Frame(Inside_Div, width=Inside_Div.winfo_reqwidth(), height=Inside_Div.winfo_reqheight(),
                                     bg="lightblue")
        Button_Play_Stop_Div.grid(row=0, column=0, padx=5, pady=5)

        Play_Button = Button(Button_Play_Stop_Div, text="Play", command=self.button_sound)
        Play_Button.grid(row=0, column=0, padx=5, pady=5)

        Stop_Button = Button(Button_Play_Stop_Div, text="Stop", command=self.button_stop)
        Stop_Button.grid(row=0, column=1, padx=5, pady=5)

        # Créer un label pour afficher le temps
        self.time_label = Label(Inside_Div, text=f"{total_time:.2f} seconds")
        self.time_label.grid(row=1, column=0, padx=5, pady=5)

        Delete_Button = Button(Inside_Div, text="Delete", command=lambda: self.delete_sound(Div_player))
        Delete_Button.grid(row=2, column=0, padx=5, pady=5)

        self.sound_divs.append((Div_player, Inside_Div, Play_Button, Stop_Button, Button_Play_Stop_Div, Delete_Button, self.time_label))

        self.current_row += 1

    def delete_sound(self, div_player):
        div_player.destroy()
        self.sound_divs.remove(div_player)

    def reset_sound_div(self, index):
        if index < len(self.sound_divs):
            Div_player, Inside_Div, Play_Button, Stop_Button, Button_Play_Stop_Div, Delete_Button = self.sound_divs[index]
            Play_Button.config(text="New Play Text")

def main():
    root = Tk()
    root.geometry("400x400")
    root.minsize(400,400)
    root.title("SoundBoard Test")
    root.resizable(True, True)
    app = Example(master=root)
    root.mainloop()

if __name__ == '__main__':
    main()