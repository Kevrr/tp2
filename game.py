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
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/fuel.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = randint(50, 950)
        self.rect.centery = randint(150,550)

    def advance(self):
        if self.rect.size[0] != 120:
            self.rect.size = (self.rect.size[0] + 2, self.rect.size[1] + 2)
            self.image = pygame.transform.scale(self.image, self.rect.size)
        else:
            self.delete()

    def collision(self, sprite):
        if self.rect.size[0] == 100:
            if self.rect.colliderect(sprite.rect):
                sprite.energy += 200
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
        self.image = pygame.image.load("img/asteroid.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = randint(0, 884)
        self.rect.centery = randint(50,950)

    def advance(self):
        if self.rect.size != (240, 240):
            self.rect.size = (self.rect.size[0] + 2, self.rect.size[1] + 2)
            self.image = pygame.transform.scale(self.image, self.rect.size)
        else:
            self.delete()

    def collision(self, sprite):
        if self.rect.size == (200, 200) and not sprite.shooting:
            if self.rect.colliderect(sprite.rect):
                sprite.energy -= 30
                self.delete()
        elif sprite.shooting:
            if self.rect.colliderect(sprite.ammoRect):
                self.master.left -= 1
                self.master.pts += 100
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
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/ring.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = randint(0,700)
        self.rect.centery = randint(50,950)

        self.innerRect = self.image.get_rect()
        self.innerRect.centerx = self.rect.centerx
        self.innerRect.centery = self.rect.centery
        self.innerRect.size = ((self.rect.size[0] - 5, self.rect.size[1] - 5))

    def advance(self):
        if self.rect.size != (240, 240):
            self.rect.size = (self.rect.size[0] + 2, self.rect.size[1] + 2)
            self.innerRect.size = (self.innerRect.size[0] + 2, self.innerRect.size[1] + 2)
            self.image = pygame.transform.scale(self.image, self.rect.size)
        else:
            print(self.rect.size, self.innerRect.size)
            self.delete()

    def collision(self, sprite):
        if self.rect.size == (200, 200):
            if self.innerRect.colliderect(sprite.rect):
                if not self.rect.colliderect(sprite.ammoRect):
                    self.master.left -= 1
                    self.master.pts += 100
                    self.delete()
                else:
                    sprite.energy -= 30
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
    level = 0
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

        self.bg = pygame.image.load("img\gamebg.png")
        self.textFont = pygame.font.Font(None, 20)
        self.titleFont = pygame.font.Font(None, 100)

        self.player = Ship()

        pygame.key.set_repeat(1, 20)
        pygame.mouse.set_visible(False)

        self.clock = pygame.time.Clock()

        while self.execute:
            self.clock.tick(60)

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
                    object = randint(0, 2)
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
        leftText = self.textFont.render(f"Restantes = {self.left}", 1, (255, 255, 255))
        energyText = self.textFont.render(f"Combustible = {self.player.energy}", 1, (255, 255, 255))
        finalText = self.titleFont.render(f"{self.endText}", 1, (255, 255, 255))
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(ptsText, (1, 1))
        self.screen.blit(leftText, (1, 12))
        self.screen.blit(energyText, (1, 23))
        for i in self.entities:
            self.screen.blit(i.image, i.rect)
        self.screen.blit(self.player.sightImg, self.player.sightRect)
        self.screen.blit(self.player.ammoImg, self.player.ammoRect)
        self.screen.blit(self.player.image, self.player.rect)
        self.screen.blit(finalText, (200, 300))
        if self.endText != "":
            self.endText = ""

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
            self.endText = "GAME OVER"
            self.finish = True

    def quit(self):
        pygame.quit()
        if self.window != None:
            if self.finish:
                if self.window.pilots[self.window.slected].hs < self.pts:
                    self.window.pilots[self.window.slected].hs = self.pts
                window.savePilots()
            self.window.master.deiconify()

if __name__ == "__main__":
    game = Game(None)
