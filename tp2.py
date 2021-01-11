from tkinter import *
from PIL import Image, ImageTk
from random import randint as randint
import pickle

class Pilot:
    name = ""
    img = ""
    hs = 0

    def __init__(self, name, img):
        self.name = name
        self.img = img

class MainWindow:
    pilots = []

    def __init__(self, master):
        self.master = master
        self.canvas = Canvas(self.master, width = 100, height = 100)
        self.canvas.pack()

        try:
            self.loadPilots()
        except:
            print("no pilots found")
            self.createPilots()

        self.bAbout = Button(self.canvas, text = "Info", command = self.openAbout)
        self.bAbout.pack()
        self.bHighScores = Button(self.canvas, text = "Puntajes", command = self.openHighScores)
        self.bHighScores.pack()
        self.bSettings = Button(self.canvas, text = "Ajustes", command = self.openSettings)
        self.bSettings.pack()

    def loadImg(self, name):
        path = os.path.join('img', name)
        img = Image.open(path)
        return ImageTk.PhotoImage(img)

    def createPilots(self):
        names = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        imgs = ["noImg.jpg", "noImg.jpg", "noImg.jpg", "noImg.jpg", "noImg.jpg", "noImg.jpg", "noImg.jpg", "noImg.jpg", "noImg.jpg", "noImg.jpg"]
        for i in range(0, 10):
            self.pilots.append(Pilot(names[i], imgs[i]))
            self.pilots[i].hs = randint(0, 334)
        print("pilots created")

    def loadPilots(self):
        file = open("pilots.txt", "rb")
        self.pilots.extend(pickle.load(file))
        file.close()
        print("pilots loaded")

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
    pilots = []

    def __init__(self, master):
        self.master = master
        self.pilots.extend(main.pilots)
        self.canvas = Canvas(self.master, width = 100, height = 100)
        self.canvas.pack()

        self.sortPilots(0, len(self.pilots) - 1)
        y = 50
        for i in range(0, 6):
            self.canvas.create_text(230, y, text = self.pilots[i].name + str(self.pilots[i].hs), anchor = NW)
            y += 10

        self.bBack = Button(self.canvas, text = "atras", command = self.back)
        self.bBack.pack()

    def sortPilots(self, low, high):
        if low < high:
            index = self.partition(low, high)
            self.sortPilots(low, index)
            self.sortPilots(index + 1, high)

    def partition(self, low, high):
        pivot = self.pilots[low]
        while True:
            while self.pilots[low].hs < pivot.hs:
                low += 1
            while self.pilots[high].hs > pivot.hs:
                high -= 1
            if low >= high:
                return high
            else:
                self.pilots[low], self.pilots[high] = self.pilots[high], self.pilots[low]
                low += 1
                high -= 1

    def back(self):
        self.master.destroy()
        root.deiconify()

class SettingsWindow:

    def __init__(self, master):
        self.master = master
        self.canvas = Canvas(self.master, width = 100, height = 100)
        self.canvas.pack()

        for i in main.pilots:
            img = loadImage(i.img)
            self.canvas.create_image(x, y, anchor = NW)
            self.canvas.create_text(x, y + 50, anchor = NW)
            x += 50
            if x == 300:
                x = 0
                y += 50

        self.bBack = Button(self.canvas, text = "atras", command = self.back)
        self.bBack.pack()

    def back(self):
        file = open("pilots.txt", "wb")
        pickle.dump(main.pilots, file)
        file.close()
        self.master.destroy()
        root.deiconify()

if __name__ == "__main__":
    root = Tk()
    root.title("Star Force")
    root.resizable(width = NO, height = NO)
    main = MainWindow(root)
    root.mainloop()
