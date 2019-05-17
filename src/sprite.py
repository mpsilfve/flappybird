import os

SRC_DIR=os.path.dirname(os.path.abspath(__file__))
RESOURCE_DIR=os.path.join(os.path.split(SRC_DIR)[0],"resources")

import pygame

G=0.1
VX=-1
RED=(255,0,0)
FLAP='f'

class Sprite:
    def __init__(self,pos,sprite,screen):
        self.pos = list(pos)
        self.sprite = sprite
        self.screen = screen
        self.screen_dim = (screen.get_width(),
                           screen.get_height())
        self.dim = (sprite.get_width(),
                    sprite.get_height())
        self.acc = 0

    def get_rect(self):
        return self.sprite.get_rect().move(self.pos)

    def blit(self):        
        self.screen.blit(self.sprite,self.pos)        

class FlappyBird(Sprite):
    def __init__(self,pos,screen):
        super().__init__(pos,
                         pygame.image.load(os.path.join(RESOURCE_DIR,
                                                        "bird.png")),
                         screen)
        self.v = 0
        self.acc = 0

    def update(self):
        self.v += G + self.acc
        self.pos[1] += self.v 
        if self.pos[1] <= 0:
            self.pos[1] = 0
            self.v = 0
        if self.pos[1] + self.dim[1] >= self.screen_dim[1]:
            self.pos[1] = self.screen_dim[1] - self.dim[1]
            self.v = 0
        self.acc = min(0,self.acc+1.5)
        self.blit()

    def handle(self,event):
        if ('unicode' in event.__dict__ and 
            event.__dict__['unicode'] == FLAP):
            self.acc = -3
            self.v = 0

class Obstacle(Sprite):
    def __init__(self,pos,screen):
        super().__init__(pos,pygame.Surface((100,200)),screen)
        self.sprite.fill(RED)

    def update(self,bird):
        if not self.collided(bird):
            self.pos[0] += VX
        self.blit()

    def collided(self,bird):
        return self.get_rect().colliderect(bird.get_rect())
            
