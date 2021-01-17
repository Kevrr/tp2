import pygame, time
from pygame.locals import *
from random import randint

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
        self.sightRect.centerx = 500
        self.sightRect.centery = 96

        self.ammoImg = pygame.image.load("img\laser.png")
        self.ammoRect = self.ammoImg.get_rect()
        self.ammoRect.centerx = 500
        self.ammoRect.centery = 350

    def borders(self):
        if self.rect.top <= 0:
            self.rect.top = 0
            self.sightRect.top = -250
            self.ammoRect.top = 20
        if self.rect.left <= 0:
            self.rect.left = 0
            self.sightRect.left = 80
            self.ammoRect.left = 85
        if self.rect.bottom >= 700:
            self.rect.bottom = 700
            self.sightRect.bottom = 430
            self.ammoRect.bottom = 680
        if self.rect.right >= 1000:
            self.rect.right = 1000
            self.sightRect.right = 920
            self.ammoRect.right = 915

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

class Fuel(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/fuel.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(50, 950)
        self.rect.centery = random.randint(150,550)

    def advance(self):
        if self.rect.size[0] != 50:
            x = self.rect.size[0] + 2
            y = self.rect.size[1] + 2
            self.rect.size = (x, y)
        else:
            time.sleep(0.01)
            self.delete()

    def collision(self, sprite):
        if self.rect.size[0] == 50:
            if self.rect.colliderect(sprite.rect):
                sprite.energy += 200
                self.delete()

    def delete(self):
        i = 0
        while i < len(self.master.obstacles):
            if self.master.obstacles[i] == self:
                self.master.obstacles.pop(i)
                break

class Asteroid(pygame.sprite.Sprite):

    def __init__(self, master):
        self.master = master
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/asteroid.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = randint(0, 884)
        self.rect.centery = randint(50,950)

    def advance(self):
        if self.rect.size != (100, 100):
            x = self.rect.size[0] + 1
            y = self.rect.size[1] + 1
            self.rect.size = (x, y)
        else:
            time.sleep(0.01)
            self.delete()

    def collision(self, sprite):
        if self.rect.size == (100, 100):
            if self.rect.colliderect(sprite.rect):
                sprite.energy -= 30
                self.delete()
        if self.rect.colliderect(sprite.ammoRect):
            if not self.rect.colliderect(sprite.rect):
                self.master.left -= 1
                self.master.pts += 100
                self.delete()

    def delete(self):
        i = 0
        while i < len(self.master.obstacles):
            if self.master.obstacles[i] == self:
                self.master.obstacles.pop(i)
                break

class Ring(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/ring.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = randint(0,700)
        self.rect.centery = randint(50,950)

    def advance(self):
        if self.rect.size != (100, 100):
            x = self.rect.size[0] + 2
            y = self.rect.size[1] + 2
            self.rect.size = (x, y)
        else:
            time.sleep(0.01)
            self.delete()

    def collision(self, sprite):
        if self.rect.size == (100, 100):
            if self.rect.colliderect(sprite.rect):
                self.master.left -= 1
                self.master.pts += 100
                self.delete()

    def delete(self):
        i = 0
        while i < len(self.master.obstacles):
            if self.master.obstacles[i] == self:
                self.master.obstacles.pop(i)
                break

class Game:
    level = 0
    pts = 0
    left = 10
    execute = True
    finish = False
    obstacles = []
    endText = ""

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((1000, 700))
        pygame.display.set_caption("Star Force")
        pygame.display.init()

        fondo = pygame.image.load("img\gamebg.png")
        self.textFont = pygame.font.Font(None, 20)
        self.titleFont = pygame.font.Font(None, 100)

        self.player = Ship()

        pygame.key.set_repeat(1, 20)
        pygame.mouse.set_visible(False)

        self.clock = pygame.time.Clock()

        while self.execute:
            self.clock.tick(60)

            self.player.borders()
            self.player.shoot(self.obstacles)

            self.spawnObstacles()
            self.spawnFuel()
            for i in self.obstacles:
                i.advance()
                i.collision(self.player)

            if self.player.energy <= 0:
                self.endText = "GAME OVER"
                self.finish = True

            if self.left == 0:
                if self.level < 2:
                    self.level += 1
                else:
                    self.endText = "MISION CUMPLIDA"
                    self.finish = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.left = 0
                    self.player.energy = 0
                    self.execute = False
                if not self.player.shooting:
                    if event.type == pygame.KEYDOWN:
                        if event.key == K_ESCAPE:
                            self.execute = False
                            pygame.quit()
                            self.left = 0
                            self.player.energy = 0
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
                                self.player.shooting = True

            ptsText = self.textFont.render(f"Puntos = {self.pts}", 1, (255, 255, 255))
            leftText = self.textFont.render(f"Restantes = {self.left}", 1, (255, 255, 255))
            energyText = self.textFont.render(f"Combustible = {self.player.energy}", 1, (255, 255, 255))
            finalText = self.titleFont.render(f"{self.endText}", 1, (255, 255, 255))
            self.screen.blit(fondo, (0, 0))
            self.screen.blit(ptsText, (1, 1))
            self.screen.blit(leftText, (1, 12))
            self.screen.blit(energyText, (1, 23))
            for i in self.obstacles:
                self.screen.blit(i.image, i.rect)
            self.screen.blit(self.player.sightImg, self.player.sightRect)
            self.screen.blit(self.player.ammoImg, self.player.ammoRect)
            self.screen.blit(self.player.image, self.player.rect)
            self.screen.blit(finalText, (300, 300))
            self.player.energy -= 0.1
            pygame.display.flip()

            if self.finish:
                time.sleep(2)
                self.execute = False
                pygame.quit()
                self.left = 0
                self.pts += self.player.energy//100
                #actualizar_pts()
                self.player.energy = 0

    def spawnObstacles(self):
        if len(self.obstacles) < 5:
            spawn = randint(0, 127)
            if spawn == 0:
                if self.level == 0:
                    self.obstacles.append(Asteroid(self))
                elif self.level == 1:
                    self.obstacles.append(Ring(self))
                elif self.level == 3:
                    object = randint(0, 2)
                    if object == 0:
                        self.obstacles.append(Asteroid())
                    elif object == 1:
                        self.obstacles.append(Ring())

    def spawnFuel(self):
        if self.player.energy <= 700:
            spawn = randint(0, self.player.energy // 100)
            if spawn == 0:
                self.obstacles.append(Fuel(self))

    def movePlayer(self, movement, distance):
        if movement == "y":
            self.player.rect.centery += distance
            self.player.sightRect.centery += distance
            self.player.ammoRect.centery += distance
        elif movement == "x":
            self.player.rect.centerx += distance
            self.player.sightRect.centerx += distance
            self.player.ammoRect.centerx += distance

    def quit(self):
        self.execute = False
        pygame.quit()
        if self.finish:
            main.pilots[main.slected].pts = self.pts
        root.deiconify()

if __name__ == "__main__":
    game = Game()
