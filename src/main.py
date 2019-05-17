# import the pygame module, so you can use it
import pygame
import time

from sprite import FlappyBird, Obstacle

DELAY=0.01 
BLACK=(0,0,0)

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # initialize the pygame module
    pygame.init()
    # load and set the logo
#    logo = pygame.image.load("bird.png")

    pygame.display.set_caption("Flappy bird")
    screen = pygame.display.set_mode((600,500))

    bird = FlappyBird((200,0),screen)
    obstacle1 = Obstacle((400,300),screen)
    obstacle2 = Obstacle((400,0),screen)
    # main loop
    while 1:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            bird.handle(event)
        screen.fill(BLACK)
        obstacle1.update(bird)
        obstacle2.update(bird)
        bird.update()
        pygame.display.flip()
        time.sleep(DELAY)

