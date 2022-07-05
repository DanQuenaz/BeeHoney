from obj import Obj, Bee, Text, Spider, MoscaPreta, Flower, Pos
from functions import Functions
import random
import pygame


class Game:

    def __init__(self):

        self.bg = Obj("assets/bg.png", 0, 0)
        self.bg2 = Obj("assets/bg.png", 0, -640)

        self.enemy_mult_hp = 1.0
        self.enemies = []
        
        self.flower = Flower("assets/flower1.png", random.randrange(0, 320), 200)
        self.bee = Bee("assets/bee1.png", 150, 600)

        self.change_scene = False

        self.score = Text(120, "0")
        self.lifes = Text(60, "3")

        self.enemies_group = pygame.sprite.Group()

    def draw(self, window):

        self.bg.draw(window)
        self.bg2.draw(window)
        self.bee.draw(window)
        
        self.flower.draw(window)

        for stinger in self.bee.stingers:
            stinger.draw(window)
        
        for enemy in self.enemies:
            enemy.draw(window)

        self.score.draw(window, 160, 50)
        self.lifes.draw(window, 50, 50)

    def update(self):

        self.move_bg()
        self.flower.anim(self.flower.sprite_image, 8, 3)
        self.bee.anim(self.bee.sprite_image, 2, 5)
        self.bee.move_bee_shot()
        # self.move_flower()

        self.generate_enemies()
        
        self.move_enemies()
        self.anim_enemies()

        self.colisions()
        
        self.gameover()
        self.score.update_text(str(self.bee.pts))
        self.lifes.update_text(str(self.bee.life))

    def move_bg(self):
        self.bg.sprite.rect[1] += 10
        self.bg2.sprite.rect[1] += 10

        if self.bg.sprite.rect[1] > 640:
            self.bg.sprite.rect[1] = 0

        if self.bg2.sprite.rect[1] > 0:
            self.bg2.sprite.rect[1] = -640

        

    def gameover(self):
        if self.bee.life <= 0:
            self.change_scene = True
    
    def generate_enemies(self):
        # if len(self.enemies) <= 0:
        # if Functions.prob(3.0):
        #     self.enemies.append(Spider("assets/spider1.png", random.randrange(0, 320), -50, self.enemy_mult_hp))
        if Functions.prob(3.0):
            self.enemies.append(MoscaPreta("assets/mosca_preta1.png", random.randrange(0, 320), -50, self.enemy_mult_hp))

    def colisions(self):
        
        self.bee.colision(self.flower)

        for enemy in self.enemies:
            self.bee.colision(enemy)

        for stinger in self.bee.stingers:
            for enemy in self.enemies:
                if stinger.colision(enemy):
                    try:
                        self.bee.stingers.remove(stinger)
                    except:
                        pass
                        
    def move_enemies(self):
        for enemy in self.enemies:
            if not enemy.move():
                self.enemies.remove(enemy)
    
    def anim_enemies(self):
        for enemy in self.enemies:
            enemy.anim(enemy.sprite_image, 2, 5)