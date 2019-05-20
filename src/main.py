# import the pygame module, so you can use it
import pygame
import time
import os

from sprite import FlappyBird, GateSpawner, ScoreBoard
from constants import BLACK, GREEN, RED, DARKRED, DARKGREEN, QUIT, SCREENDIM, RESOURCE_DIR

DELAY=0.01 

def getkey(event):
    if 'unicode' in event.__dict__:
        return event.__dict__['unicode']
    else:
        return None

if __name__=="__main__":
    pygame.init()
    pygame.display.set_caption("Flappy bird")
    screen = pygame.display.set_mode(SCREENDIM)
    bg = pygame.image.load(os.path.join(RESOURCE_DIR,"background.jpg"))

#    game_over = pygame.font.SysFont("courier",70).render("Game over!!!",1,DARKRED,DARKGREEN)
    game_over = pygame.image.load(os.path.join(RESOURCE_DIR,"game over01.jpg"))

    bird = FlappyBird((200,200),screen)
    gates = GateSpawner(screen)
    score_board = ScoreBoard(screen)

    pygame.mixer.music.load(os.path.join(RESOURCE_DIR,"background_music.wav"))
    pygame.mixer.music.play(loops=-1)

    # main loop
    while 1:
        for event in pygame.event.get():
            key = getkey(event)
            if key == QUIT:
                exit(0)
            bird.handle(key)
        if bird.alive:
            screen.blit(bg,(0,-700))
            gates.update(bird)
            bird.update()
            score_board.update(bird)
        else:
            screen.blit(game_over,(50,200))
            pygame.mixer.music.stop()
        pygame.display.flip()
        time.sleep(DELAY)

