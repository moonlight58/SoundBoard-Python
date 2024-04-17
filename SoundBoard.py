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
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo

class Example(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.sound_divs = [] # Liste pour stocker les références des divs de son
        self.current_row = 1  # Pour suivre la ligne actuelle
        self.current_column = 0 # Pour échanger de colonnes
        self.initUI()
        self.sound_file = None  # Variable pour stocker le chemin du fichier MP3
        self.current_sound = None  # Variable pour stocker le son actuellement joué


    def initUI(self):
            menubar = Menu(self.master)

            menu1 = Menu(menubar, tearoff=0) # Menu1 "Create"
            menu1.add_command(label="From File", command=self.open_file)
            menubar.add_cascade(label="Create", menu=menu1)

            menu2 = Menu(menubar, tearoff=0) # Menu2 "Edit"
            menu2.add_command(label="Edit", command=self.edit_soundboard)
            menubar.add_cascade(label="Edit", menu=menu2)

            self.master.config(menu=menubar) # Initialisation du menu

    # Fonction test
    def alert(self):
        showinfo("Alert", "Bravo!")

    # Ouvre les mp3 files
    def open_file(self):
        file_path = askopenfilename(title="Choose the file to open", filetypes=[("MP3 files", "*.mp3")])
        if file_path:
            self.sound_file = file_path # Stocker le chemin du fichier sélectionné
            print(self.sound_file)
            self.create_sound()
        else:
            showinfo("Error", "No sound file selected.")

    # Sound player button
    def button_sound(self):
        if self.sound_file:
            pygame.mixer.init() # Initialiser le mixeur Pygame
            self.current_sound = pygame.mixer.Sound(self.sound_file) # Charger le fichier MP3
            self.current_sound.play() # Jouer le fichier MP3
        else:
            showinfo("Error", "No sound file selected.")

    def button_stop(self):
        if self.current_sound:
            self.current_sound.stop() # Arrêter le son actuellement joué
            self.current_sound = None # Réinitialiser la référence au son
        else:
            showinfo("Error", "No sound is currently playing.")

    # Show edit button to change the sound player
    def edit_soundboard(self):
        print("Editing soundboard...")
        # Ici, vous pouvez ajouter la logique pour éditer le tableau de sons

    # Create sound player div
    # Need to make the changeable name
    #              the time change
    def create_sound(self):

        # Calculer la position en fonction de la colonne actuelle et de la ligne actuelle
        row = self.current_row
        column = 0

        # Création de la Div_player pour un son spécifique
        Div_player = Frame(self.master, width=200, height=200, borderwidth=2, relief="raised")
        Div_player.grid(row=row, column=column, padx=10, pady=5)

        Label(Div_player, text="Name of the sound").grid(row=0, column=0, padx=5, pady=5)

        # Création de Inside_Div
        Inside_Div = Frame(Div_player, width=(Div_player.winfo_reqwidth() * 0.90), height=(Div_player.winfo_reqheight() * 0.5), bg="purple")
        Inside_Div.grid(row=2, column=0, padx=5, pady=5)

        Button_Play_Stop_Div = Frame(Inside_Div, width=Inside_Div.winfo_reqwidth(), height=Inside_Div.winfo_reqheight(),
                                     bg="lightblue")
        Button_Play_Stop_Div.grid(row=0, column=0, padx=5, pady=5)

        # Création du bouton de lecture
        Play_Button = Button(Button_Play_Stop_Div, text="Play", command=self.button_sound)
        Play_Button.grid(row=0, column=0, padx=5, pady=5)

        # Création du bouton stop de la lecture que si elle est lancée
        Stop_Button = Button(Button_Play_Stop_Div, text="Stop", command=self.button_stop)
        Stop_Button.grid(row=0, column=1, padx=5, pady=5)

        # Création du label pour le temps du son
        Label(Inside_Div, text="Time of the sound").grid(row=1, column=0, padx=5, pady=5)

        Delete_Button = Button(Inside_Div, text="Delete", command=lambda: self.delete_sound(Div_player))
        Delete_Button.grid(row=2, column=0, padx=5, pady=5)

        # Stockage des références pour une utilisation ultérieure
        self.sound_divs.append((Div_player, Inside_Div, Play_Button, Stop_Button, Button_Play_Stop_Div, Delete_Button))

        # Mettre à jour la ligne actuelle pour le prochain son
        self.current_row += 1

    # Delete Sound player div
    def delete_sound(self, div_player):
        # Supprimer la Div_player et tous ses enfants
        div_player.destroy()
        # Supprimer la référence de la liste des divs de son
        self.sound_divs.remove(div_player)

    # Reset to placeholder the name, time, sound (have to finish it)
    def reset_sound_div(self, index):
        # Réinitialiser ou modifier un div de son spécifique
        if index < len(self.sound_divs):
            Div_player, Inside_Div, Inside_Div2, Play_Button = self.sound_divs[index]
            # Ici, vous pouvez réinitialiser ou modifier les éléments comme vous le souhaitez
            # Par exemple, changer le texte du bouton de lecture
            Play_Button.config(text="New Play Text")

def main():
    root = Tk()
    root.geometry("400x400")
    root.title("SoundBoard Test")
    root.resizable(True, True)
    app = Example(master=root)
    root.mainloop()

if __name__ == '__main__':
    main()
