import os
import pygame
from random import randint

from constants import RESOURCE_DIR, RED, BLACK, SPAWNINTERVAL, GREEN, FLAP, VX, G, PUSH, GAP, BLUE

pygame.mixer.init()
tweet = pygame.mixer.Sound(os.path.join(RESOURCE_DIR,"bird_chirp.wav"))

class Sprite:
    def __init__(self,pos,v,sprites,screen,color=None):
        self.t = 0
        self.pos = list(pos)
        self.v = list(v)
        self.acc = [0,0]
        self.sprites = sprites
        self.screen = screen
        self.screen_dim = (screen.get_width(),
                           screen.get_height())
        if color:
            self.sprites[0].fill(color)

    def update(self,limit_y=0):
        self.v[0] += self.acc[0]
        self.v[1] += self.acc[1]
        self.pos[0] += self.v[0]
        self.pos[1] += self.v[1]
        if limit_y:
            self.pos[1] = max(0,min(self.pos[1],500-self.get_dim()[1]))
        
        self.acc = [0,0]
        self.screen.blit(self.sprites[self.get_t()],self.pos)        
        self.t += 1

    def get_dim(self):
        return (self.sprites[self.get_t()].get_width(),
                self.sprites[self.get_t()].get_height())

    def get_rect(self):
        return self.sprites[self.get_t()].get_rect().move(self.pos)

    def get_t(self):
        return self.t % len(self.sprites)

    def transparent(self):
        for s in self.sprites:
            s.set_alpha(0)

class FlappyBird(Sprite):
    def __init__(self,pos,screen):
        animation = [pygame.image.load(os.path.join(RESOURCE_DIR,
                                                    "bird_animation%u.png" 
                                                    % i)) for i in range(1,7)]
        animation = [pygame.transform.scale(pic,(int(pic.get_width()/1.8),int(pic.get_height()/1.8))) for pic in animation]
        animation += reversed(animation)
        super().__init__(pos,
                         [0,0],
#                         [pygame.image.load(os.path.join(RESOURCE_DIR,
#                                                        "bird.png"))],
                         animation,
                         screen)
        self.alive = 1
        self.score = 0

    def update(self):
        if self.alive:
            self.acc[1] += G
        super().update(limit_y=1)
        
    def handle(self,key):
        if key == FLAP:
            self.acc[1] += -PUSH
            self.v[1] = 0
            if not pygame.mixer.get_busy():
                tweet.play()

    def get_bird_rect(self):
        rect = self.get_rect()
        rect.width = int(0.75*rect.width)
        rect.height = int(0.75*rect.height)
        rect.center = (rect.center[0]+20,rect.center[1]+10)
        return rect

class Gate:
    def __init__(self,screen):
        opos = randint(80,500-GAP-80)
        # PRELOAD!!
#        pillar = pygame.image.load(os.path.join(RESOURCE_DIR, "column.png"))
        pillar = pygame.image.load(os.path.join(RESOURCE_DIR, "chopped_log.png"))
        scale = 130/pillar.get_width()
        pillar = pygame.transform.scale(pillar,(int(pillar.get_width()*scale),
                                                int(pillar.get_height()*scale)))
        self.upper_obstacle = Sprite((600,opos-pillar.get_height()),[VX,0],[pillar],screen)
        self.opening = Sprite((600,opos),[VX,0],[pygame.Surface((100,GAP))],screen)
        self.opening.transparent()
        self.lower_obstacle = Sprite((600,opos+GAP),[VX,0],[pillar],screen)

        self.scored = 0

    def update(self,bird):
        bird_rect = bird.get_bird_rect()
        opening_rect = self.opening.get_rect()
        upper_obst_rect = self.upper_obstacle.get_rect()
        lower_obst_rect = self.lower_obstacle.get_rect()

        if opening_rect.colliderect(bird_rect):
            bird.score += (1 - self.scored)
            self.scored = 1
        if upper_obst_rect.colliderect(bird_rect) or lower_obst_rect.colliderect(bird_rect):
            bird.alive = 0

        self.upper_obstacle.update()
        self.opening.update()
        self.lower_obstacle.update()

    def out_of_screen(self):
        return self.upper_obstacle.pos[0] < -self.upper_obstacle.get_dim()[0]

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
        self.font = pygame.font.SysFont("chalkboard",70)
        
    def update(self,bird):
        score = ("000" + str(bird.score))[-3:]
        self.screen.blit(self.font.render(score,1,BLUE),(450,30))
