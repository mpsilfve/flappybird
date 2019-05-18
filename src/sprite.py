import os
import pygame
from random import randint

from constants import RESOURCE_DIR, RED, BLACK, SPAWNINTERVAL, GREEN, FLAP, VX, G, PUSH

class Sprite:
    def __init__(self,pos,v,sprite,screen,color=None):
        self.pos = list(pos)
        self.v = list(v)
        self.acc = [0,0]
        self.sprite = sprite
        self.screen = screen
        self.screen_dim = (screen.get_width(),
                           screen.get_height())
        self.dim = (sprite.get_width(),
                    sprite.get_height())
        if color:
            self.sprite.fill(color)

    def update(self):
        self.v[0] += self.acc[0]
        self.v[1] += self.acc[1]
        self.pos[0] += self.v[0]
        self.pos[1] += self.v[1]
        self.pos[1] = max(0,min(self.pos[1],500-self.dim[1]))
        
        self.acc = [0,0]
        self.screen.blit(self.sprite,self.pos)        

    def get_rect(self):
        return self.sprite.get_rect().move(self.pos)


class FlappyBird(Sprite):
    def __init__(self,pos,screen):
        super().__init__(pos,
                         [0,0],
                         pygame.image.load(os.path.join(RESOURCE_DIR,
                                                        "bird.png")),
                         screen)
        self.alive = 1
        self.score = 0

    def update(self):
        if self.alive:
            self.acc[1] += G
        super().update()

    def handle(self,key):
        if key == FLAP:
            self.acc[1] += -PUSH
            self.v[1] = 0

class Gate:
    def __init__(self,screen):
        opos = randint(30,500-220-30)
        self.obstacle = Sprite((600,0),[VX,0],pygame.Surface((100,500)),screen,RED)
        self.opening = Sprite((600,opos),[VX,0],pygame.Surface((100,220)),screen,BLACK)
        self.scored = 0

    def update(self,bird):
        bird_rect = bird.get_rect()
        opening_rect = self.opening.get_rect()
        obst_rect = self.obstacle.get_rect()
        clip_rect = bird_rect.clip(obst_rect)

        if opening_rect.colliderect(bird_rect):
            bird.score += (1 - self.scored)
            self.scored = 1
        if clip_rect.size != (0,0) and not opening_rect.contains(clip_rect):
            bird.alive = 0

        self.obstacle.update()
        self.opening.update()

    def out_of_screen(self):
        return self.obstacle.pos[0] < -self.obstacle.dim[0]

class GateSpawner:
    def __init__(self,screen):
        self.screen = screen
        self.gates = []
        self.t = 0
    
    def update(self,bird):
        while self.gates and self.gates[0].out_of_screen():
            self.gates.pop(0)
        if self.t % SPAWNINTERVAL == 0:
            self.gates.append(Gate(self.screen))
        for g in self.gates:
            g.update(bird)
        self.t += 1

class ScoreBoard:
    def __init__(self,screen):
        self.screen = screen
        self.font = pygame.font.SysFont("courier",50)
        
    def update(self,bird):
        score = ("000" + str(bird.score))[-3:]
        self.screen.blit(self.font.render(score,1,GREEN),(500,50))
