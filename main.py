import pygame
import os
import time
import random

# Initializing Font And Window
pygame.init()
pygame.font.init()
pygame.mixer.init()
WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")

HITBOX_WIDTH, HITBOX_HEIGHT = 52, 46

# Defining Colors
BLACK = (0,0,0)
WHITE = (255,255,255)


spriteArray = [[None] * 25 for i in range(25)]


# for row in spriteArray:
    # print(row)


# Load In Image Assets
BG = pygame.transform.scale(pygame.image.load(os.path.join("images", "PacManMap.png")), (WIDTH, HEIGHT))
PLAYER_IMAGE  = pygame.image.load(os.path.join("images", "pacman_c.png"))
SPRITE_IMAGE = pygame.image.load(os.path.join("images", "dot.png" ))

# Load Sounds
movingSound = pygame.mixer.Sound(os.path.join("audio", "pacman_chomp.wav"))
FPS = 60

class Sprite:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(img)

    def draw(self, window):
        if self.x == 35 * 4:
            window.blit(self.img,(self.x + 20, self.y))
        elif self.x == 12 * 35:
            window.blit(self.img,(self.x - 20, self.y))
        else:
            window.blit(self.img,(self.x, self.y))

class Player:

    def __init__(self, x, y, img, dir=None):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.Mask((HITBOX_WIDTH, HITBOX_HEIGHT), True)
        self.direction = dir
        self.soundCount = 0
    
    def draw(self, window):
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

    for i in range(25):
        for j in range(25):
            spriteArray[i][j] = Sprite(35 * i, 35 * j, SPRITE_IMAGE)

    BG_MASK = pygame.mask.from_surface(BG)
    

    player = Player( (WIDTH/2 - PLAYER_IMAGE.get_width() / 2), (HEIGHT / 2 - PLAYER_IMAGE.get_height() / 2) + 53, PLAYER_IMAGE)

    n = 0

    def checkCollision(obj1, obj2):
        offset = (obj2.x - 0, obj2.y - 0)
        return obj1.overlap(obj2.mask, offset) != None

    def checkSpriteCollision(obj1, obj2):
        offset_x = obj2.x - obj1.x
        offset_y = obj2.y - obj1.y
        return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

    def redrawWindow():
        WIN.fill(BLACK)
        WIN.blit(BG, (0,0))
        player.draw(WIN)    

        for i in range(25):
            for j in range(25):
                if spriteArray[i][j]:
                    if not checkCollision(BG_MASK, spriteArray[i][j]) and i != 5 and i != 11:
                        spriteArray[i][j].draw(WIN)

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
        
        if player.soundCount == 35:
            pygame.mixer.Sound.play(movingSound)
            player.soundCount = 1
        else:
            player.soundCount += 1
    
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        checkCollision(BG_MASK, player)

        redrawWindow()

        for i in range(25):
            for j in range(25):
                if spriteArray[i][j]:
                    if checkSpriteCollision(player, spriteArray[i][j]):
                        spriteArray[i][j] = None

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0:
            playerCopy = Player(player.x - player_vel, player.y, PLAYER_IMAGE);
            if checkCollision(BG_MASK, playerCopy):
                movePlayer(player)
                continue
            else:
                player.direction = 'l'
                player.img = PLAYER_IMAGE
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:
            playerCopy = Player(player.x + player_vel, player.y, PLAYER_IMAGE);
            if checkCollision(BG_MASK, playerCopy):
                movePlayer(player)
                continue
            else:
                player.direction = 'r'
                player.img = PLAYER_IMAGE
        if keys[pygame.K_w] and player.y - player_vel > 0:
            playerCopy = Player(player.x, player.y - player_vel, PLAYER_IMAGE);
            if checkCollision(BG_MASK, playerCopy):
                movePlayer(player)
                continue
            else:
                player.direction = 'u'
                player.img = PLAYER_IMAGE
        if keys[pygame.K_s] and player.y + player_vel + player.get_height()< HEIGHT:
            playerCopy = Player(player.x, player.y + player_vel, PLAYER_IMAGE);
            if checkCollision(BG_MASK, playerCopy):
                movePlayer(player)
                continue
            else:
                player.direction = 'd'
                player.img = PLAYER_IMAGE

        movePlayer(player)  


    pygame.quit()

main()
    