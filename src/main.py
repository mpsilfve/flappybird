# import the pygame module, so you can use it
import pygame
import time

from sprite import FlappyBird, GateSpawner, ScoreBoard
from constants import BLACK, GREEN, RED, DARKRED, DARKGREEN, QUIT

DELAY=0.01 

def getkey(event):
    if 'unicode' in event.__dict__:
        return event.__dict__['unicode']
    else:
        return None

if __name__=="__main__":
    pygame.init()
    pygame.display.set_caption("Flappy bird")
    screen = pygame.display.set_mode((600,500))
    game_over = pygame.font.SysFont("courier",70).render("Game over!!!",1,DARKRED,DARKGREEN)

    bird = FlappyBird((200,200),screen)
    gates = GateSpawner(screen)
    score_board = ScoreBoard(screen)

    # main loop
    while 1:
        for event in pygame.event.get():
            key = getkey(event)
            if key == QUIT:
                exit(0)
            bird.handle(key)
        if bird.alive:
            screen.fill(BLACK)
            gates.update(bird)
            bird.update()
            score_board.update(bird)
        else:
            screen.blit(game_over,(50,200))
        pygame.display.flip()
        time.sleep(DELAY)

