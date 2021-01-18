from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from pygame import mixer
from PIL import Image, ImageTk
from random import randint
from game import *
import os, pickle, shutil

# Objeto Pilot
# atributos: name(str), image(str), hs(int)
class Pilot:
    name = ""
    image = ""
    hs = 0

    def __init__(self, name, image):
        self.name = name
        self.image = image

# Objeto MainWindow
# atributos: pilots(list), selected(int), widgets(tk)
# metodos:
# loadImage: carga imagenes
# E: nombre de la imagen(str)
# S: imagen
# R: /
# playMusic: reanuda la musica
# stopMusic: pausa la musica
# createPilots: crea los pilotos si no existen
# E: /
# S: lista de pilotos
# R: /
# loadPilots: carga los pilotos de un txt
# E: /
# S: lista de pilotos
# R: /
# openGame: abre la ventana del juego
# E: click de boton
# S: ventana del juego
# R: /
# openAbout: abre la ventana de informacion
# E: click de boton
# S: ventana de informacion
# R: /
# openHighScores: abre la ventana de puntajes
# E: click de boton
# S: ventana de puntajes
# R: /
# openSettings: abre la ventana de configuracion
# E: click de boton
# S: ventana de configuracion
# R: /
class MainWindow:
    pilots = []
    selected = 0

    def __init__(self, master):
        self.master = master
        self.canvas = Canvas(self.master, width = 500, height = 500)
        self.canvas.pack()
        self.bg = self.loadImage("bg.png")
        self.canvas.create_image(0, 0, anchor = NW, image = self.bg)
        self.title = self.loadImage("title.png")
        self.canvas.create_image(100, 50, anchor = NW, image = self.title)

        mixer.init()
        mixer.music.load("sound/Title.mp3")
        mixer.music.play(loops = -1)

        try:
            self.loadPilots()
        except:
            print("no pilots found")
            self.createPilots()
            self.savePilots()

        self.playImg = self.loadImage("play.jpg")
        self.PlayButton = Button(self.canvas, image = self.playImg, bg = "#306098", command = self.openGame)
        self.PlayButton.place(x = 220, y = 220)
        self.aboutImg = self.loadImage("about.jpg")
        self.AboutButton = Button(self.canvas, image = self.aboutImg, bg = "#185838", command = self.openAbout)
        self.AboutButton.place(x = 450, y = 450)
        self.hsImg = self.loadImage("hs.jpg")
        self.HighScoresButton = Button(self.canvas, image = self.hsImg, bg = "#185838", command = self.openHighScores)
        self.HighScoresButton.place(x = 410, y = 450)
        self.selectedImg = self.loadImage(self.pilots[self.selected].image)
        self.SettingsButton = Button(self.canvas, image = self.selectedImg, bg = "#185838", command = self.openSettings)
        self.SettingsButton.place(x = 10, y = 390)

    def loadImage(self, name):
        path = os.path.join('img', name)
        image = Image.open(path)
        return ImageTk.PhotoImage(image)

    def playMusic(self):
        mixer.music.unpause()

    def stopMusic(self):
        mixer.music.pause()

    def createPilots(self):
        names = ["Fox", "Falco", "Peppy", "Slippy", "Fay", "Miyu", "Wolf", "Pigma", "Andrew", "Leon"]
        images = ["fox.jpg", "falco.jpg", "peppy.jpg", "slippy.jpg", "fay.jpg", "miyu.jpg", "wolf.jpg", "pigma.jpg", "andrew.jpg", "leon.jpg"]
        for i in range(0, 10):
            self.pilots.append(Pilot(names[i], images[i]))
            self.pilots[i].hs = randint(0, 10) * 100
        print("pilots created")

    def loadPilots(self):
        file = open("pilots.txt", "rb")
        self.pilots.extend(pickle.load(file))
        file.close()
        print("pilots loaded")

    def savePilots(self):
        file = open("pilots.txt", "wb")
        pickle.dump(self.pilots, file)
        file.close()
        print("pilots saved")

    def openGame(self):
        self.stopMusic()
        self.master.withdraw()
        game = Game(self)

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

# Objeto AboutWindow
# atributos: text(str), widgets(tk)
# metodos:
# back: vuelve a la ventana principal
# E: click de boton
# S: ventana de principal
# R: /
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
               Version: 1.4"""

    def __init__(self, master):
        self.master = master
        self.canvas = Canvas(self.master, width = 500, height = 400)
        self.canvas.pack()
        self.bg = main.loadImage("bg2.png")
        self.canvas.create_image(0, 0, anchor = NW, image = self.bg)

        self.canvas.create_text(100, 5, anchor = NW, text = self.text, font = ('Arial', 15), fill = "#ffffff")

        self.backImg = main.loadImage("back.jpg")
        self.BackButton = Button(self.canvas, image = self.backImg, bg = "#784800", command = self.back)
        self.BackButton.place(x = 460, y = 360)

    def back(self):
        self.master.destroy()
        root.deiconify()

# Objeto HighScoresWindow
# atributos: pilots(list), widgets(tk)
# metodos:
# sortPilots: ordenamiento rapido de la lista de pilotos
# E: extremos d la lista(int)
# S: lista ordenada segun puntajes
# R: /
# partition: ordenamiento rapido de la lista de pilotos
# E: extremos de la lista(int)
# S: indice para ordenar(int)
# R: /
# back: vuelve a la ventana principal
# E: click de boton
# S: ventana de principal
# R: /
class HighScoresWindow:
    pilots = []

    def __init__(self, master):
        self.master = master
        self.pilots.extend(main.pilots)
        self.canvas = Canvas(self.master, width = 500, height = 400)
        self.canvas.pack()
        self.bg = main.loadImage("bg2.png")
        self.canvas.create_image(0, 0, anchor = NW, image = self.bg)

        self.canvas.create_text(70, 10, anchor = NW, text = 'Mejores Puntajes', font = ("Consolas", 30), fill = "#ffffff")
        self.sortPilots(0, len(self.pilots) - 1)
        y = 60
        for i in range(0, 7):
            try:
                self.canvas.create_text(130, y, anchor = NW, text = f"{i + 1}) {self.pilots[i].name}: {self.pilots[i].hs}", font = ("Consolas", 20), fill = "#ffffff")
            except:
                self.canvas.create_text(130, y, anchor = NW, text = f"{i + 1}) -----: ---", font = ("Consolas", 20), fill = "#ffffff")
            y += 30

        self.backImg = main.loadImage("back.jpg")
        self.BackButton = Button(self.canvas, image = self.backImg, bg = "#784800", command = self.back)
        self.BackButton.place(x = 460, y = 360)

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

# Objeto SettingsWindow
# atributos: img(str), path(str), savePath(str), widgets(tk)
# metodos:
# updateSelection: muestra el piloto seleccionado
# E: /
# S: muestra la imagen y nombre del piloto seleccionado
# R: /
# changeName: cambia el nombre de un piloto
# E: nombre escrito en Entry(str)
# S: cambia el nombre del piloto
# R: debe haber un piloto seleccionado en la lista y el entry no puede estar vacio
# getImage: obtiene una imagen para el piloto
# E: direccion preguntada al usuario
# S: imagen
# R: se debe seleccionar una imagen png o jpg
# addPilot: agrega un piloto
# E: nombre escrito en Entry(str)
# S: piloto nuevo
# R: el entry no puede estar vacio
# selectPilot: cambia el piloto seleccionado
# E: click de boton
# S: cambia el piloto seleccionado
# R: debe haber un piloto seleccionado en la lista
# deletePilot: elimina un piloto
# E: click de boton
# S: elimina un piloto
# R: debe haber un piloto seleccionado en la lista, si solo queda un piloto no se puede eliminar
# on: reanuda la musica
# E: click de boton
# S: musica continua
# R: /
# off: pausa la musica
# E: click de boton
# S: musica se pausa
# R: /
# back: vuelve a la ventana principal
# E: click de boton
# S: ventana de principal
# R: /
class SettingsWindow:
    img = "noImg.jpg"
    path = ""
    savePath = os.getcwd() + os.sep + 'img'

    def __init__(self, master):
        self.master = master
        self.canvas = Canvas(self.master, width = 500, height = 400)
        self.canvas.pack()
        self.bg = main.loadImage("bg2.png")
        self.canvas.create_image(0, 0, anchor = NW, image = self.bg)

        self.canvas.create_text(15, 5, anchor = NW, text = "Lista de Pilotos", font = ("Consolas", 20), fill = "#ffffff")
        self.scroll = Scrollbar(self.canvas, bg = "#9194A7")
        self.scroll.place(height = 352, x = 275, y = 50)
        self.listbox = Listbox(self.canvas, height = 18, width = 30, font = ("Consolas", 12), fg = "#ffffff", bg = "#901800", selectbackground = "#D05020", yscrollcommand = self.scroll.set)
        self.listbox.place(x = 1, y = 50)
        self.scroll.config(command = self.listbox.yview)
        for i in main.pilots:
            self.listbox.insert(END, i.name)

        self.canvas.create_text(310, 5, anchor = NW, text = "Seleccionado", font = ("Consolas", 20), fill = "#ffffff")
        self.selectedImg = main.loadImage(main.pilots[main.selected].image)
        self.canvas.create_image(350, 50, anchor = NW, image = self.selectedImg, tags = "pilotimage")
        self.canvas.create_text(350, 150, anchor = NW, text = main.pilots[main.selected].name, font = ("Consolas", 12), fill = "#ffffff", tags = "pilotname")

        self.canvas.create_text(290, 195, anchor = NW, text = "Editar Pilotos", font = ("Consolas", 20), fill = "#ffffff")
        self.canvas.create_text(350, 220, anchor = NW, text = "Nombre nuevo", font = ("Consolas", 12), fill = "#ffffff")
        self.NameEntry = Entry(self.canvas, font = ("Consolas", 12), fg = "#ffffff", bg = "#901800", width = 10)
        self.NameEntry.place(x = 350, y = 240)

        self.selimgImg = main.loadImage("addImg.jpg")
        self.SelectImgButton = Button(self.canvas, image = self.selimgImg, bg = "#D05020", command = self.getImage)
        self.SelectImgButton.place(x = 300, y = 280)
        self.addImg = main.loadImage("add.jpg")
        self.AddButton = Button(self.canvas,image = self.addImg, bg = "#D05020", command = self.addPilot)
        self.AddButton.place(x = 350, y = 280)
        self.changeImg = main.loadImage("change.jpg")
        self.ChangeButton = Button(self.canvas, image = self.changeImg, bg = "#D05020", command = self.changeName)
        self.ChangeButton.place(x = 400, y = 280)
        self.selImg = main.loadImage("select.jpg")
        self.SelectButton = Button(self.canvas, image = self.selImg, bg = "#700000", command = self.selectPilot)
        self.SelectButton.place(x = 380, y = 165)
        self.deleteImg = main.loadImage("delete.jpg")
        self.DeleteButton = Button(self.canvas, image = self.deleteImg, bg = "#D05020", command = self.deletePilot)
        self.DeleteButton.place(x = 450, y = 280)
        self.backImg = main.loadImage("back.jpg")
        self.OnButton = Button(self.canvas, text = "on", bg = "#784800", command = self.on, state = DISABLED)
        self.OnButton.place(x = 380, y = 360)
        self.OffButton = Button(self.canvas, text = "off", bg = "#784800", command = self.off)
        self.OffButton.place(x = 420, y = 360)
        self.BackButton = Button(self.canvas, image = self.backImg, bg = "#784800", command = self.back)
        self.BackButton.place(x = 460, y = 360)

    def updateSelection(self):
        self.selectedImg = main.loadImage(main.pilots[main.selected].image)
        self.canvas.itemconfig("pilotimage", image = self.selectedImg)
        self.canvas.itemconfig("pilotname", text = main.pilots[main.selected].name)

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
        if self.path[-4:].lower() == ".png" or self.path[-4:].lower() == ".jpg":
            i = -1
            while self.path[i] != "/":
                i -= 1
            self.img = self.path[i + 1:]
            img = Image.open(self.path)
            if img.size[0] > 100 or img.size[0] > 100:
                self.path = ""
                self.img = "noImg.jpg"
                messagebox.showerror("Error", "Imagen demasiado grande")
            else:
                messagebox.showinfo("Exito", "Imagen cargada")
        else:
            self.path = ""
            messagebox.showerror("Error", "Seleccione una imagen (png o jpg)")

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

    def on(self):
        main.playMusic()
        self.OnButton["state"] = DISABLED
        self.OffButton["state"] = NORMAL

    def off(self):
        main.stopMusic()
        self.OffButton["state"] = DISABLED
        self.OnButton["state"] = NORMAL

    def back(self):
        self.master.destroy()
        main.savePilots()
        main.selectedImg = main.loadImage(main.pilots[main.selected].image)
        main.SettingsButton.config(image = main.selectedImg)
        root.deiconify()

if __name__ == "__main__":
    root = Tk()
    root.title("Star Force")
    root.resizable(width = NO, height = NO)
    main = MainWindow(root)
    root.mainloop()
