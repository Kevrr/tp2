import pygame, time
from pygame.locals import *
from random import randint

# Objeto Ship
# atributos: energy(int), shooting(bool)
# metodos:
# borders: mantiene al objeto en pantalla
# shoot: disparo de la nave
# E: preionar una tecla
# S: disparo
# R: /
class Ship(pygame.sprite.Sprite):
    energy = 1000
    shooting = False

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img\ship.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = 500
        self.rect.centery = 350

        self.sightImg = pygame.image.load("img\sight.png")
        self.sightRect = self.sightImg.get_rect()
        self.sightRect.centerx = self.rect.centerx
        self.sightRect.centery = self.rect.centery - 254

        self.ammoImg = pygame.image.load("img\laser.png")
        self.ammoRect = self.ammoImg.get_rect()
        self.ammoRect.centerx = self.rect.centerx
        self.ammoRect.centery = self.rect.centery

        self.energyImg = pygame.image.load("img\energy.png")
        self.energyRect = self.energyImg.get_rect()

    def borders(self):
        if self.rect.top <= 0:
            self.rect.top = 0
            self.sightRect.centery = self.rect.centery - 254
        if self.rect.left <= 0:
            self.rect.left = 0
            self.sightRect.centerx = self.rect.centerx
        if self.rect.bottom >= 700:
            self.rect.bottom = 700
            self.sightRect.centery = self.rect.centery - 254
        if self.rect.right >= 1000:
            self.rect.right = 1000
            self.sightRect.centerx = self.rect.centerx

        self.energyRect.size = (0.137 * max(0, self.energy), self.energyRect.size[1])
        self.energyImg = pygame.transform.scale(self.energyImg, self.energyRect.size)

    def shoot(self, sprites):
        if self.shooting:
            collision = False
            for i in sprites:
                if self.ammoRect.colliderect(i.rect):
                    collission = True
            if not self.ammoRect.colliderect(self.sightRect) and not collision:
                self.ammoRect.top -= 30
            else:
                self.ammoRect.centerx = self.rect.centerx
                self.ammoRect.centery = self.rect.centery
                self.shooting = False
        else:
            self.ammoRect.centerx = self.rect.centerx
            self.ammoRect.centery = self.rect.centery

# Objeto Fuel
# metodos:
# advance: acerca el objeto
# collision: comprueba colisiones
# E: objeto contra el que se va a compobar(Ship)
# S: aumenta la energia
# R: /
# delete: borra el objeto del juego
# E: /
# S: elimina el objeto
# R: /
class Fuel(pygame.sprite.Sprite):

    def __init__(self, master):
        self.master = master
        self.originalImg = pygame.image.load("img/fuel.png")
        self.rect = self.originalImg.get_rect()
        self.rect.size = (16, 16)
        self.image = pygame.transform.scale(self.originalImg, self.rect.size)
        self.rect.centerx = randint(50, 880)
        self.rect.centery = randint(150, 580)

    def advance(self):
        if self.rect.size[0] != 128:
            self.rect.size = (self.rect.size[0] + 1, self.rect.size[1] + 1)
            self.image = pygame.transform.scale(self.originalImg, self.rect.size)
        else:
            self.delete()

    def collision(self, sprite):
        if self.rect.size[0] >= 80:
            if self.rect.colliderect(sprite.rect):
                sprite.energy += 100
                pygame.mixer.Sound("sound/pickup.mp3").play()
                self.delete()

    def delete(self):
        i = 0
        while i < len(self.master.entities):
            if self.master.entities[i] == self:
                self.master.entities.pop(i)
                break
            i += 1

# Objeto Asteroid
# metodos:
# advance: acerca el objeto
# collision: comprueba colisiones
# E: objeto contra el que se va a compobar(Ship)
# S: disminuye la energia, o aumenta los puntos
# R: /
# delete: borra el objeto del juego
# E: /
# S: elimina el objeto
# R: /
class Asteroid(pygame.sprite.Sprite):

    def __init__(self, master):
        self.master = master
        pygame.sprite.Sprite.__init__(self)
        self.originalImg = pygame.image.load("img/asteroid.png")
        self.rect = self.originalImg.get_rect()
        self.rect.size = (32, 32)
        self.image = pygame.transform.scale(self.originalImg, self.rect.size)
        self.rect.centerx = randint(50, 760)
        self.rect.centery = randint(50, 460)

    def advance(self):
        if self.rect.size != (256, 256):
            self.rect.size = (self.rect.size[0] + 1, self.rect.size[1] + 1)
            self.image = pygame.transform.scale(self.originalImg, self.rect.size)
        else:
            self.delete()

    def collision(self, sprite):
        if self.rect.size[0] >= 200 and not sprite.shooting:
            if self.rect.colliderect(sprite.rect):
                sprite.energy -= 50
                pygame.mixer.Sound("sound/hit.mp3").play()
                self.delete()
        elif sprite.shooting:
            if self.rect.colliderect(sprite.ammoRect):
                self.master.left -= 1
                self.master.pts += 100
                pygame.mixer.Sound("sound/destroy.mp3").play()
                self.delete()

    def delete(self):
        i = 0
        while i < len(self.master.entities):
            if self.master.entities[i] == self:
                self.master.entities.pop(i)
                break
            i += 1

# Objeto Ring
# metodos:
# advance: acerca el objeto
# collision: comprueba colisiones
# E: objeto contra el que se va a compobar(Ship)
# S: disminuye la energia, o aumenta los puntos
# R: /
# delete: borra el objeto del juego
# E: /
# S: elimina el objeto
# R: /
class Ring(pygame.sprite.Sprite):

    def __init__(self, master):
        self.master = master
        self.originalImg = pygame.image.load("img/ring.png")
        self.rect = self.originalImg.get_rect()
        self.rect.size = (32, 32)
        self.image = pygame.transform.scale(self.originalImg, self.rect.size)
        self.rect.centerx = randint(50, 760)
        self.rect.centery = randint(50, 460)

    def advance(self):
        if self.rect.size != (256, 256):
            self.rect.size = (self.rect.size[0] + 1, self.rect.size[1] + 1)
            self.image = pygame.transform.scale(self.originalImg, self.rect.size)
        else:
            self.delete()

    def collision(self, sprite):
        if self.rect.size[0] >= 200:
            if self.rect.colliderect(sprite.rect):
                if self.rect.centerx + 32 > sprite.rect.centerx > self.rect.centerx - 32 and self.rect.centery + 32 > sprite.rect.centery > self.rect.centery - 32:
                    self.master.left -= 1
                    self.master.pts += 100
                    pygame.mixer.Sound("sound/pass.mp3").play()
                    self.delete()
                else:
                    sprite.energy -= 50
                    pygame.mixer.Sound("sound/hit.mp3").play()
                    self.delete()

    def delete(self):
        i = 0
        while i < len(self.master.entities):
            if self.master.entities[i] == self:
                self.master.entities.pop(i)
                break
            i += 1

# Objeto Game
# atributos = level(int), pts(int), left(int), execute(bool), finish(bool), entities(list), endText(str)
# metodos:
# spawnObstacles: genera asteroides o anillos
# E: /
# S: asteroide o anillo
# R: /
# getInput: obtiene las entradas
# E: click de teclas o del mouse
# S: movimiento del jugador o cerrar el juego
# R: teclas de las flechas, espacio, escape y click para cerrar ventana
# spawnFuel: genera combustible
# E: /
# S: combustible
# R: /
# movePlayer: mueve la nave del jugador
# E: movimiento(str, int)
# S: mueve la nave
# R: /
# updateScreen: actualiza los elementos de la pantalla
# E: /
# S: elementos en posicion nueva
# R: /
# checkLevel: verifica si se puede avanzar el nivel o terminar el juego
# E: /
# S: nuevo nivel o finalizacion del juego
# R: /
# checkDeath: verifica muerte del jugador
# E: /
# S: finalizacion del juego
# R: /
# quit: termina el juego
# E: /
# S: vuelve a la pantalla principal
# R: /
class Game:
    level = 1
    pts = 0
    left = 10
    execute = True
    finish = False
    entities = []
    endText = ""

    def __init__(self, window):
        self.window = window

        pygame.init()

        self.screen = pygame.display.set_mode((1000, 700))
        pygame.display.set_caption("Star Force")
        pygame.display.init()

        pygame.mixer.init()
        pygame.mixer.music.load("sound/Meteo.mp3")
        pygame.mixer.music.play(loops = -1)

        if window != None:
            self.playerImg = pygame.image.load(f"img\{window.pilots[window.selected].image}")
        else:
            self.playerImg = pygame.image.load("img/noImg.jpg")

        self.bg = pygame.image.load("img\gamebg.png")
        self.energybar = pygame.image.load("img\energybar.png")
        self.textFont = pygame.font.Font(None, 25)
        self.titleFont = pygame.font.Font(None, 100)

        self.player = Ship()

        pygame.key.set_repeat(1, 20)
        pygame.mouse.set_visible(False)

        while self.execute:
            pygame.time.wait(1)

            self.checkDeath()
            self.checkLevel()

            if self.finish:
                self.execute = False

            self.player.borders()
            self.player.shoot(self.entities)

            self.spawnObstacles()
            self.spawnFuel()
            for i in self.entities:
                i.advance()
                i.collision(self.player)

            self.getInput()

            self.updateScreen()
            self.player.energy -= 0.1
            pygame.display.flip()
            if self.endText != "":
                pygame.mixer.Sound("sound/next.mp3").play()
                pygame.time.wait(3000)
                self.endText = ""

        self.quit()

    def getInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.execute = False
            if not self.player.shooting:
                if event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.execute = False
                    else:
                        if event.key == K_UP:
                            self.movePlayer("y", -10)
                        if event.key == K_LEFT:
                            self.movePlayer("x", -10)
                        if event.key == K_DOWN:
                            self.movePlayer("y", 10)
                        if event.key == K_RIGHT:
                            self.movePlayer("x", 10)
                        if event.key == K_SPACE:
                            if not self.player.shooting:
                                pygame.mixer.Sound("sound/laser.mp3").play()
                                self.player.shooting = True
                            else:
                                self.player.shooting = False

    def spawnObstacles(self):
        if len(self.entities) < 5:
            spawn = randint(0, 127)
            if spawn == 0:
                if self.level == 0:
                    self.entities.append(Asteroid(self))
                elif self.level == 1:
                    self.entities.append(Ring(self))
                elif self.level == 2:
                    object = randint(0, 1)
                    if object == 0:
                        self.entities.append(Asteroid(self))
                    elif object == 1:
                        self.entities.append(Ring(self))

    def spawnFuel(self):
        if len(self.entities) < 5:
            present = False
            entity = Fuel(self)
            for i in self.entities:
                if type(i) == type(entity):
                    present = True
            if self.player.energy <= 700 and not present:
                spawn = randint(0, 127)
                if spawn == 0:
                    self.entities.append(entity)

    def movePlayer(self, movement, distance):
        if movement == "y":
            self.player.rect.centery += distance
            self.player.sightRect.centery += distance
            self.player.ammoRect.centery += distance
        elif movement == "x":
            self.player.rect.centerx += distance
            self.player.sightRect.centerx += distance
            self.player.ammoRect.centerx += distance

    def updateScreen(self):
        ptsText = self.textFont.render(f"Puntos = {self.pts}", 1, (255, 255, 255))
        finalText = self.titleFont.render(f"{self.endText}", 1, (255, 255, 255))
        self.screen.blit(self.bg, (0, 0))
        for i in self.entities:
            self.screen.blit(i.image, i.rect)
        self.screen.blit(self.player.sightImg, self.player.sightRect)
        if self.player.shooting:
            self.screen.blit(self.player.ammoImg, self.player.ammoRect)
        self.screen.blit(self.player.image, self.player.rect)
        self.screen.blit(ptsText, (100, 30))
        self.screen.blit(self.playerImg, (0, 0))
        self.screen.blit(self.energybar, (100, 0))
        self.screen.blit(self.player.energyImg, (108, 6))
        self.screen.blit(finalText, (200, 300))

    def checkLevel(self):
        if self.left == 0:
            if self.level < 2:
                self.endText = "NIVEL SUPERADO"
                self.level += 1
                self.entities =  []
                self.left = 10
            else:
                self.endText = "MISION CUMPLIDA"
                self.finish = True

    def checkDeath(self):
        if self.player.energy <= 0:
            pygame.mixer.Sound("sound/hit.mp3").play()
            self.endText = "GAME OVER"
            self.finish = True

    def quit(self):
        pygame.quit()
        if self.window != None:
            if self.finish:
                if self.window.pilots[self.window.slected].hs < self.pts:
                    self.window.pilots[self.window.slected].hs = self.pts
                window.savePilots()
            self.window.openHighScores()

if __name__ == "__main__":
    game = Game(None)
