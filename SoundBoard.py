from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo

class Example(Frame):

    def alert(self):
        showinfo("Alert", "Bravo!")

    def open_file(self):
        askopenfilename(title="Choose the file to open")  # Need to make the sound player

    def edit_soundboard(self):
        print("Editing soundboard...")
        # make a button on each soundboard (change the name/time duration/file path/or delete it)

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.initUI()

    def initUI(self):
        menubar = Menu(self.master)

        menu1 = Menu(menubar, tearoff=0)
        menu1.add_command(label="From File", command=self.open_file)
        menubar.add_cascade(label="Create", menu=menu1)

        menu2 = Menu(menubar, tearoff=0)
        menu2.add_command(label="Edit", command=self.alert)
        menubar.add_cascade(label="Edit", menu=menu2)

        self.master.config(menu=menubar)

        #TODO : - Make a layout for the soundboard button (Name, duration, button to play it)
        #       - Sound Player
        #       - Save the changes made in whatever hellish way (need to search)
        #       - Add edit button to change (name, time duration(linked to the time duration of the sound/not really changeable), filepath)

def main():
    root = Tk()
    root.geometry("300x280+300+300")
    root.resizable(False, False)
    app = Example(master=root)
    root.mainloop()

if __name__ == '__main__':
    main()
