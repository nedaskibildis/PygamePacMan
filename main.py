import pygame
import os
import time
import random

# Initializing Font And Window
pygame.font.init()
WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")

HITBOX_WIDTH, HITBOX_HEIGHT = 52, 46

# Defining Colors
BLACK = (0,0,0)
WHITE = (255,255,255)

# Load In Image Assets
BG = pygame.transform.scale(pygame.image.load(os.path.join("images", "PacManMap.png")), (WIDTH, HEIGHT))
PLAYER_IMAGE = pygame.image.load(os.path.join("images", "pacman_c.png"))


FPS = 60

class Player:

    def __init__(self, x, y, img, dir=None):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.Mask((HITBOX_WIDTH, HITBOX_HEIGHT), True)
        self.direction = dir
    
    def draw(self, window):
        window.blit(self.mask.to_surface(unsetcolor=(255,0,0), setcolor=(255,0,0)), (self.x, self.y))
        window.blit(self.img,(self.x + 8, self.y + 6))

    def get_width(self):
        return self.img.get_width()
    
    def get_height(self):
        return self.img.get_height()
    
    def get_direction(self):
        return self.direction


def main():
    run = True
    clock = pygame.time.Clock()
    player_vel = 2

    BG_MASK = pygame.mask.from_surface(BG)
    

    player = Player( (WIDTH/2 - PLAYER_IMAGE.get_width() / 2), (HEIGHT / 2 - PLAYER_IMAGE.get_height() / 2) + 53, PLAYER_IMAGE)

    n = 0

    def checkCollision(obj1, obj2):
        offset = (obj2.x - 0, obj2.y - 0)
        return obj1.overlap(obj2.mask, offset) != None

    def redrawWindow():
        WIN.fill(BLACK)
        WIN.blit(BG, (0,0))
        player.draw(WIN)    



        pygame.display.update()

    def movePlayer(player):
        if player.direction == 'l':
            playerCopy = Player(player.x - player_vel, player.y, PLAYER_IMAGE);
            if checkCollision(BG_MASK, playerCopy):
                return
            player.x -= player_vel
        elif player.direction == 'r':
            playerCopy = Player(player.x + player_vel, player.y, PLAYER_IMAGE);
            if checkCollision(BG_MASK, playerCopy):
                return
            player.x += player_vel
        elif player.direction == 'u':
            playerCopy = Player(player.x, player.y - player_vel, PLAYER_IMAGE);
            if checkCollision(BG_MASK, playerCopy):
                return
            player.y -= player_vel
        elif player.direction == 'd':
            playerCopy = Player(player.x, player.y + player_vel, PLAYER_IMAGE);
            if checkCollision(BG_MASK, playerCopy):
                return
            player.y += player_vel
    
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        checkCollision(BG_MASK, player)
        redrawWindow()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0:
            playerCopy = Player(player.x - player_vel, player.y, PLAYER_IMAGE);
            if checkCollision(BG_MASK, playerCopy):
                continue
            else:
                player.direction = 'l'
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:
            playerCopy = Player(player.x + player_vel, player.y, PLAYER_IMAGE);
            if checkCollision(BG_MASK, playerCopy):
                continue
            else:
                player.direction = 'r'
        if keys[pygame.K_w] and player.y - player_vel > 0:
            playerCopy = Player(player.x, player.y - player_vel, PLAYER_IMAGE);
            if checkCollision(BG_MASK, playerCopy):
                continue
            else:
                player.direction = 'u'
        if keys[pygame.K_s] and player.y + player_vel + player.get_height()< HEIGHT:
            playerCopy = Player(player.x, player.y + player_vel, PLAYER_IMAGE);
            if checkCollision(BG_MASK, playerCopy):
                continue
            else:
                player.direction = 'd'

        movePlayer(player)  


    pygame.quit()

main()
    