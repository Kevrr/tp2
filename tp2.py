from tkinter import *

class MainWindow:

    def __init__(self, master):
        self.master = master
        self.canvas = Canvas(self.master, width = 100, height = 100)
        self.canvas.pack()

        self.bAbout = Button(self.canvas, text = "Info", command = self.openAbout)
        self.bAbout.pack()
        self.bHighScores = Button(self.canvas, text = "Puntajes", command = self.openHighScores)
        self.bHighScores.pack()
        self.bSettings = Button(self.canvas, text = "Ajustes", command = self.openSettings)
        self.bSettings.pack()

    def openAbout(self):
        self.master.withdraw()
        wAbout = Toplevel()
        wAbout.title("Informacion Complementaria")
        wAbout.resizable(width = NO, height = NO)
        about = AboutWindow(wAbout)
        wAbout.mainloop()

    def openHighScores(self):
        self.master.withdraw()
        wHighScores = Toplevel()
        wHighScores.title("Mejores Puntajes")
        wHighScores.resizable(width = NO, height = NO)
        about = AboutWindow(wHighScores)
        wHighScores.mainloop()

    def openSettings(self):
        self.master.withdraw()
        wSettings = Toplevel()
        wSettings.title("Ajustes")
        wSettings.resizable(width = NO, height = NO)
        about = AboutWindow(wSettings)
        wSettings.mainloop()

class AboutWindow:

    def __init__(self, master):
        self.master = master
        self.canvas = Canvas(self.master, width = 100, height = 100)
        self.canvas.pack()

        self.bBack = Button(self.canvas, text = "atras", command = self.back)
        self.bBack.pack()

    def back(self):
        self.master.destroy()
        root.deiconify()

class HighScoresWindow:

    def __init__(self, master):
        self.master = master
        self.canvas = Canvas(self.master, width = 100, height = 100)
        self.canvas.pack()

        self.bBack = Button(self.canvas, text = "atras", command = self.back)
        self.bBack.pack()

    def back(self):
        self.master.destroy()
        root.deiconify()

class SettingsWindow:

    def __init__(self, master):
        self.master = master
        self.canvas = Canvas(self.master, width = 100, height = 100)
        self.canvas.pack()

        self.bBack = Button(self.canvas, text = "atras", command = self.back)
        self.bBack.pack()

    def back(self):
        self.master.destroy()
        root.deiconify()

if __name__ == "__main__":
    root = Tk()
    root.title("Star Force")
    root.resizable(width = NO, height = NO)
    main = MainWindow(root)
    root.mainloop()
