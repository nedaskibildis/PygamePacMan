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
ORANGE_GHOST = pygame.image.load(os.path.join("images", "ghost3.png"))

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

class Ghost:
    def __init__(self, x, y, img, timer):
        self.x = x
        self.y = y
        self.img = img
        self.timer = timer
        self.direction = 'up'
        self.mask = pygame.mask.Mask((HITBOX_WIDTH, HITBOX_HEIGHT), True)
    
    def draw(self, window):
        window.blit(self.img, (self.x + 4, self.y + 4))
        # window.blit(self.mask.to_surface(unsetcolor=(0,0,0), setcolor=(0,255,255)), (self.x, self.y))
class Player:

    def __init__(self, x, y, img, dir=None):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.Mask((HITBOX_WIDTH, HITBOX_HEIGHT), True)
        self.direction = dir
        self.soundCount = 0
        self.direction = "down"
    
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

    # Create Sprite Array
    for i in range(25):
        for j in range(25):
            spriteArray[i][j] = Sprite(35 * i, 35 * j, SPRITE_IMAGE)

    # Set BG_mask
    BG_MASK = pygame.mask.from_surface(BG)
    
    # Create Player And 4 Ghosts
    player = Player( (WIDTH/2 - PLAYER_IMAGE.get_width() / 2), (HEIGHT / 2 - PLAYER_IMAGE.get_height() / 2) + 53, PLAYER_IMAGE)
    orangeGhost = Ghost(349, 320, ORANGE_GHOST, 0)

    n = 0

    def checkCollision(obj1, obj2):
        offset = (obj2.x - 0, obj2.y - 0)
        return obj1.overlap(obj2.mask, offset) != None

    def checkSpriteCollision(obj1, obj2):
        offset_x = obj2.x - obj1.x
        offset_y = obj2.y - obj1.y
        return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None
    
    def checkCrossroads(ghost, bgMask):
        openCount = 0

        leftGhost = Ghost(ghost.x, ghost.y, ORANGE_GHOST, 0)
        leftGhost.direction = "left"
        rightGhost = Ghost(ghost.x, ghost.y, ORANGE_GHOST, 0)
        rightGhost.direction = "right"
        downGhost = Ghost(ghost.x, ghost.y, ORANGE_GHOST, 0)
        downGhost.direction = "down"
        upGhost = Ghost(ghost.x, ghost.y, ORANGE_GHOST, 0)
        upGhost.direction = "up"

        if not checkGhostCollision(bgMask, leftGhost, leftGhost.direction):
            openCount += 1
        if not checkGhostCollision(bgMask, rightGhost, rightGhost.direction):
            openCount += 1
        if not checkGhostCollision(bgMask, upGhost, upGhost.direction):
            openCount += 1
        if not checkGhostCollision(bgMask, downGhost, downGhost.direction):
            openCount += 1
        
        if openCount >= 3:
            if ghost.direction == "left":
                ghost.direction = "right"
                changeDirection(ghost, bgMask)
            elif ghost.direction == "right":
                ghost.direction = "left"
                changeDirection(ghost, bgMask)
            elif ghost.direction == "down":
                ghost.direction = "up"
                changeDirection(ghost, bgMask)
            elif ghost.direction == "up":
                ghost.direction = "down"
                changeDirection(ghost, bgMask)

    def redrawWindow():
        WIN.fill(BLACK)
        WIN.blit(BG, (0,0))
        player.draw(WIN)    

        for i in range(25):
            for j in range(25):
                if spriteArray[i][j]:
                    if not checkCollision(BG_MASK, spriteArray[i][j]) and i != 5 and i != 11:
                        spriteArray[i][j].draw(WIN)
        orangeGhost.draw(WIN)
        pygame.display.update()

    def movePlayer(player):
        if player.x < 0:
            player.x = WIDTH
        if player.x > WIDTH:
            player.x = 0

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
    
    def moveGhost(ghost):
        if ghost.timer > 30:
            if ghost.x >= 296 and ghost.x <= 402 and ghost.y + HITBOX_HEIGHT == 318:
                return
        else:
            ghost.timer += 1
        if ghost.x < 0:
            ghost.x = WIDTH
        if ghost.x > WIDTH:
            ghost.x = 0
        if ghost.direction == "up":
            ghost.y -= 2
        elif ghost.direction == "down":
            ghost.y += 2
        if ghost.direction == "left":
            ghost.x -= 2
        if ghost.direction == "right":
            ghost.x += 2

    def checkGhostCollision(obj1, obj2, direction):
        if direction == "up":
            offset = (obj2.x - 0, obj2.y - 2)
        elif direction == "down":
            offset = (obj2.x - 0, obj2.y + 2)
        elif direction == "left":
            offset = (obj2.x - 2, obj2.y - 0)
        elif direction == "right":
            offset = (obj2.x + 2, obj2.y - 0)
        return obj1.overlap(obj2.mask, offset) != None
    
    def changeDirection(ghost, bg):
        newDirection = ghost.direction
        goodToGo = False
        while newDirection == ghost.direction or goodToGo == False :
            newDirection = random.choice(('up', 'left', 'right', 'down'))
            if checkGhostCollision(bg, ghost, newDirection):
                goodToGo = False
            else:
                goodToGo = True
        ghost.direction = newDirection

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
        
        if checkGhostCollision(BG_MASK, orangeGhost, orangeGhost.direction):
            changeDirection(orangeGhost, BG_MASK)
        
        checkCrossroads(orangeGhost,BG_MASK)
        moveGhost(orangeGhost)  


    pygame.quit()

main()
    