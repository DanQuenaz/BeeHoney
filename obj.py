import pygame
import math

from pygame.sprite import Sprite

class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def print(self):
        print(self.x, ', ', self.y)

    @staticmethod
    def add(pos_a, pos_b):
        return Pos(pos_a.x + pos_b.x, pos_a.y + pos_b.y)
    

class Obj(Sprite):

    def __init__(self, image, x, y, *groups):

        super().__init__(*groups)
        
 

        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect[0] = x
        self.rect[1] = y

        self.frame = 1
        self.tick = 0

    def get_pos(self):
        return Pos(self.rect[0], self.rect[1])

    def set_position(self, pos):
        self.rect[0] = pos.x
        self.rect[1] = pos.y

    def move(self, pos):
        pos_aux = Pos.add(self.get_pos, pos)
        self.set_position(pos_aux)

        if self.rect[1] > 640:
            self.kill()
            
    def draw(self, window):
        self.group.draw(window)

    def anim(self, image, tick, frames):
        self.tick += 1

        if self.tick == tick:
            self.tick = 0
            self.frame += 1

        if self.frame == frames:
            self.frame = 1

        self.image = pygame.image.load("assets/" + image + str(self.frame) + ".png")


class Bee(Obj):

    def __init__(self, image, x, y):
        super().__init__(image, x, y)

        pygame.mixer.init()
        self.name = "Bee"
        self.sprite_image = "bee"
        self.sound_pts = pygame.mixer.Sound("assets/sounds/score.ogg")
        self.sound_block = pygame.mixer.Sound("assets/sounds/bateu.ogg")

        self.life = 3
        self.pts = 0
        self.stingers = []

    def move(self, event):
        if event.type == pygame.MOUSEMOTION:
            pos_aux = Pos(pygame.mouse.get_pos()[0] - 35, pygame.mouse.get_pos()[1] - 30)
            self.set_position(pos_aux)
    
    def bee_shot(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.stingers.append(BeeStinger("assets/stinger.png", self.rect[0], self.rect[1]))
    
    def move_bee_shot(self):
        for stinger in self.stingers:
            stinger.rect[1] -= stinger.speed
            if stinger.rect[1] <= 0:
                stinger.kill()
                self.stingers.remove(stinger)

    def colision(self, obj):

        name = obj.name
        colison = pygame.spritecollide(self.sprite, obj.group, True)

        if name == "Flower" and colison:
            self.pts += 1
            self.sound_pts.play()
        elif name == "Spider" and colison:
            self.life -= 1
            self.sound_block.play()

class Spider(Obj):
    def __init__(self, image, x, y, mult_hp):
        super().__init__(image, x, y)
        self.name = "Spider"
        self.sprite_image = "spider"
        self.hp_base = 5
        self.hp = self.hp_base * mult_hp
        self.t = 0.0
    
    def change_hp(self, damage):
        self.hp -= damage
    
    def move(self):
        pos = self.get_pos()
        next_pos = Pos.add(pos, Pos(5 * math.cos(self.t), 5))
        self.set_position(next_pos)

        self.t += 0.1
        if self.t >= 1000.0:
            self.t = 0.0

        if self.rect[1] > 640:
            self.kill()
            return False
        return True

class MoscaPreta(Obj):
    def __init__(self, image, x, y, mult_hp):
        super().__init__(image, x, y)
        self.name = "MoscaPreta"
        self.sprite_image = "mosca_preta"
        self.hp_base = 10
        self.hp = self.hp_base * mult_hp
        self.t = 0.0
    
    def change_hp(self, damage):
        self.hp -= damage
    
    def move(self):
        pos = self.get_pos()
        next_pos = Pos.add(pos, Pos(5 * math.cos(self.t), 5))
        self.set_position(next_pos)

        self.t += 0.1
        if self.t >= 1000.0:
            self.t = 0.0

        if self.rect[1] > 640:
            self.kill()
            return False
        return True

class Flower(Obj):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)
        self.name = "Flower"
        self.sprite_image = "flower"


class BeeStinger(Obj):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)
        self.name = "Stinger"
        self.sprite_image = "stinger"
        self.damage = 1
        self.speed = 5

    def colision(self, obj):
        name = obj.name
        colision = pygame.spritecollide(self.sprite, obj.group, False)

        if colision and name == "Spider":
            self.kill()
            obj.change_hp(self.damage)
            if obj.hp <= 0:
                obj.kill()
            return True


class Text:

    def __init__(self, size, text):

        self.font = pygame.font.SysFont("Arial bold", size)
        self.render = self.font.render(text, False, (255, 255, 255))

    def draw(self, window, x, y):
        window.blit(self.render, (x, y))

    def update_text(self, update):
        self.render = self.font.render(update, False, (255, 255, 255))
