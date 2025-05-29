import pygame
import sys
from Game import GameManager 

def main():
    pygame.init()
    infoObject = pygame.display.Info()
    WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("MeoWar")
    clock = pygame.time.Clock()

    game = GameManager(screen, WIDTH, HEIGHT) 
    game.run(clock)  

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
