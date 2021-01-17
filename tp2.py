from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
from random import randint
from game import *
import os, pickle, shutil

class Pilot:
    name = ""
    img = ""
    hs = 0

    def __init__(self, name, img):
        self.name = name
        self.img = img

class MainWindow:
    pilots = []
    selected = 0

    def __init__(self, master):
        self.master = master
        self.canvas = Canvas(self.master, width = 100, height = 100)
        self.canvas.pack()

        try:
            self.loadPilots()
        except:
            print("no pilots found")
            self.createPilots()

        self.PlayButton = Button(self.canvas, text = "Jugar", command = self.openGame)
        self.PlayButton.pack()
        self.AboutButton = Button(self.canvas, text = "Info", command = self.openAbout)
        self.AboutButton.pack()
        self.HighScoresButton = Button(self.canvas, text = "Puntajes", command = self.openHighScores)
        self.HighScoresButton.pack()
        self.SettingsButton = Button(self.canvas, text = "Ajustes", command = self.openSettings)
        self.SettingsButton.pack()

    def loadImage(self, name):
        path = os.path.join('img', name)
        image = Image.open(path)
        return ImageTk.PhotoImage(image)

    def createPilots(self):
        names = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        images = ["noImg.jpg", "noImg.jpg", "noImg.jpg", "noImg.jpg", "noImg.jpg", "noImg.jpg", "noImg.jpg", "noImg.jpg", "noImg.jpg", "noImg.jpg"]
        for i in range(0, 10):
            self.pilots.append(Pilot(names[i], images[i]))
            self.pilots[i].hs = randint(0, 1001)
        print("pilots created")

    def loadPilots(self):
        file = open("pilots.txt", "rb")
        self.pilots.extend(pickle.load(file))
        file.close()
        print("pilots loaded")

    def openGame(self):
        self.master.withdraw()
        game = Game()

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
        highscores = HighScoresWindow(wHighScores)
        wHighScores.mainloop()

    def openSettings(self):
        self.master.withdraw()
        wSettings = Toplevel()
        wSettings.title("Ajustes")
        wSettings.resizable(width = NO, height = NO)
        settings = SettingsWindow(wSettings)
        wSettings.mainloop()

class AboutWindow:
    text = """Instituto Tecnologico de Costa Rica
Computer Engineering
Proyecto 2
Profesor:
    Jeff Schmidt Peralta
Autores:
    Anthony Acuña Carvajal 2018145084
    Kevin Ruiz Rodríguez 2018170538
Fecha de emision:
       18/01/2021
Version: 0.3"""

    def __init__(self, master):
        self.master = master
        self.canvas = Canvas(self.master, width = 600, height = 400)
        self.canvas.pack()

        self.canvas.create_text(5, 0, anchor = NW, text = self.text, font = ('Arial', 15))

        self.BackButton = Button(self.canvas, text = "atras", command = self.back)
        self.BackButton.place(x = 560, y = 370)

    def back(self):
        self.master.destroy()
        root.deiconify()

class HighScoresWindow:
    pilots = []

    def __init__(self, master):
        self.master = master
        self.pilots.extend(main.pilots)
        self.canvas = Canvas(self.master, width = 400, height = 200)
        self.canvas.pack()

        self.canvas.create_text(100, 10, anchor = NW, text = 'Mejores Puntajes', font = (40))
        self.sortPilots(0, len(self.pilots) - 1)
        y = 40
        for i in range(0, 7):
            try:
                self.canvas.create_text(130, y, anchor = NW, text = f"{i + 1}) {self.pilots[i].name} Puntos: {self.pilots[i].hs}", font = (20))
            except:
                self.canvas.create_text(130, y, anchor = NW, text = f"{i + 1}) ----- Puntos: ---", font = (20))
            y += 20

        self.BackButton = Button(self.canvas, text = "atras", command = self.back)
        self.BackButton.place(x = 360, y = 170)

    def sortPilots(self, low, high):
        if low < high:
            index = self.partition(low, high)
            self.sortPilots(low, index)
            self.sortPilots(index + 1, high)

    def partition(self, low, high):
        pivot = self.pilots[low]
        while True:
            while self.pilots[low].hs > pivot.hs:
                low += 1
            while self.pilots[high].hs < pivot.hs:
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
    img = "noImg.jpg"
    path = ""
    savePath = os.getcwd() + os.sep + 'img'

    def __init__(self, master):
        self.master = master
        self.canvas = Canvas(self.master, width = 600, height = 400)
        self.canvas.pack()

        self.scroll = Scrollbar(self.canvas)
        self.scroll.place(x = 275, y = 50)
        self.listbox = Listbox(self.canvas, height = 18, width = 30, font = (20) , yscrollcommand = self.scroll.set)
        self.listbox.place(x = 1, y = 50)
        self.scroll.config(command = self.listbox.yview)
        for i in main.pilots:
            self.listbox.insert(END, i.name)

        self.selectedImg = main.loadImage(main.pilots[main.selected].img)
        self.canvas.create_image(400, 200, anchor = NW, image = self.selectedImg, tags = "selected image")
        self.canvas.create_text(400, 250, anchor = NW, text = main.pilots[main.selected].name, tags = "selected name")

        self.NameEntry = Entry(self.canvas, font = (18), width = 10)
        self.NameEntry.place(x = 450, y = 50)

        self.SelectImgButton = Button(self.canvas, text = "seleccionar imagen", command = self.getImage)
        self.SelectImgButton.place(x = 400, y = 100)
        self.AddButton = Button(self.canvas, text = "agregar", command = self.addPilot)
        self.AddButton.place(x = 450, y = 130)
        self.ChangeButton = Button(self.canvas, text = "cambiar nombre", command = self.changeName)
        self.ChangeButton.place(x = 500, y = 130)
        self.SelectButton = Button(self.canvas, text = "seleccionar piloto", command = self.selectPilot)
        self.SelectButton.place(x = 450, y = 340)
        self.DeleteButton = Button(self.canvas, text = "eliminar", command = self.deletePilot)
        self.DeleteButton.place(x = 450, y = 370)
        self.BackButton = Button(self.canvas, text = "atras", command = self.back)
        self.BackButton.place(x = 560, y = 370)

    def updateSelection(self):
        self.selectedImg = main.loadImage(main.pilots[main.selected].img)
        self.canvas.itemconfig("selected image", image = self.selectedImg)
        self.canvas.itemconfig("selected name", text = main.pilots[main.selected].name)

    def changeName(self):
        try:
            i = self.listbox.curselection()[0]
            name = self.NameEntry.get()
            self.NameEntry.delete(0, END)
            main.pilots[i].name = name
            self.listbox.delete(i)
            self.listbox.insert(i, name)
            self.updateSelection()
            messagebox.showinfo("Exito", "Nombre cambiado")
        except:
            messagebox.showerror("Error", "Seleccione el piloto al que desea cambiar")

    def getImage(self):
        self.path = filedialog.askopenfilename()
        if self.path[-4:].lower() == ".png":
            i = -1
            while self.path[i] != "/":
                i -= 1
            self.img = self.path[i + 1:]
        else:
            self.path = ""
            messagebox.showerror("Error", "Seleccione una imagen")

    def addPilot(self):
        name = self.NameEntry.get()
        if name != "":
            main.pilots.append(Pilot(name, self.img))
            self.NameEntry.delete(0, END)
            if self.img != "noImg.jpg":
                shutil.copy(self.path, self.savePath)
                self.img = "noImg.jpg"
                self.path = ""
            self.listbox.insert(END, name)
            messagebox.showinfo("Exito", f"Piloto {name} agregado")
        else:
            messagebox.showerror("Error", "Ingrese un nombre para el piloto")

    def selectPilot(self):
        try:
            main.selected = self.listbox.curselection()[0]
            self.updateSelection()
        except:
            messagebox.showerror("Error", "Seleccione un piloto")

    def deletePilot(self):
        try:
            i = self.listbox.curselection()[0]
            if len(main.pilots) > 1:
                name = main.pilots[i].name
                main.pilots.pop(i)
                if main.selected >= i:
                    if i > 0:
                        main.selected -= 1
                    else:
                        main.selected = 0
                    self.updateSelection()
                self.listbox.delete(i)
                messagebox.showinfo("Exito", f"Piloto {name} eliminado")
            else:
                messagebox.showerror("Error", "Unico piloto disponible")
        except:
            messagebox.showerror("Error", "Seleccione el piloto que desea eliminar")

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
