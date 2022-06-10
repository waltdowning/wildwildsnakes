""" A snake-eating-apples arcade game """

import pygame
import pygame.freetype
from pygame.locals import *
import random
from random import randint
pygame.init()

# Assign FPS a value
FPS = 30
FramePerSec = pygame.time.Clock()
 
# Setting up color objects
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 100)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (149, 8, 231)
 
# Define the game window
DISPLAYSURF = pygame.display.set_mode((400,400))
DISPLAYSURF.fill(BLACK)
pygame.display.set_caption("Wild Wild Snakes!")
 
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
score = 0
bad_score = 0
apple_map = [(0,0),(0,0),(0,0)]

class Snake(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/snake_up.png")
        self.rect = self.image.get_rect()
        self.rect.center = (200,200)
        self.snake_moving = "NONE"
 
    def update(self):      
        
        # Which way are we moving?
        pressed_keys = pygame.key.get_pressed()
        
        if pressed_keys[K_UP]:
            self.snake_moving = "UP"
        if pressed_keys[K_DOWN]:
            self.snake_moving = "DOWN"
        if pressed_keys[K_RIGHT]:
            self.snake_moving = "RIGHT"
        if pressed_keys[K_LEFT]:
            self.snake_moving = "LEFT"
        if pressed_keys[K_SPACE]:
            self.snake_moving = "NONE"       

        # Move the snake
        if self.rect.top > 0:
            if self.snake_moving == "UP":
                self.image = pygame.image.load("img/snake_up.png")
                self.rect.move_ip(0,-3)        
        if self.rect.bottom < SCREEN_HEIGHT:
            if self.snake_moving == "DOWN":
                self.image = pygame.image.load("img/snake_down.png")
                self.rect.move_ip(0,3)
        if self.rect.left > 0:
            if self.snake_moving == "LEFT":
                self.image = pygame.image.load("img/snake_left.png")
                self.rect.move_ip(-3, 0)
        if self.rect.right < SCREEN_WIDTH:
            if self.snake_moving == "RIGHT":
                self.image = pygame.image.load("img/snake_right.png")
                self.rect.move_ip(3, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class BadSnake(pygame.sprite.Sprite):
    def __init__(self, target):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/badsnake_up.png")
        self.rect = self.image.get_rect()
        self.rect.center = (200,200)
        self.snake_moving = "NONE"
        self.targetApple = target
    
    def update(self):
        if self.rect.left > apple_map[self.targetApple][0]:
            self.image = pygame.image.load("img/badsnake_left.png")
            self.rect.move_ip(-1, 0)
        elif self.rect.left < apple_map[self.targetApple][0]:
            self.image = pygame.image.load("img/badsnake_right.png")
            self.rect.move_ip(1, 0)
        elif self.rect.top < apple_map[self.targetApple][1]:
            self.image = pygame.image.load("img/badsnake_down.png")
            self.rect.move_ip(0, 1)
        elif self.rect.top > apple_map[self.targetApple][1]:
            self.image = pygame.image.load("img/badsnake_up.png")
            self.rect.move_ip(0, -1)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Apple(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/apple.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x,y) 
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Score:
    def __init__(self):
        self.current_score = 0

    def currentScoreToString(self):
        """ Returns the current score as a 4-digit string with leading zeros. """
        tempString = str(self.current_score)
        zerosToAdd = 4 - len(tempString)
        return str("0" * zerosToAdd + tempString)

    def draw(self, surface, score_string):
        text_rect = font.get_rect(score_string, size = 20)
        text_rect.left = SCREEN_WIDTH - text_rect.width
        text_rect.top = 0
        font.render_to(surface, text_rect, score_string, WHITE, size = 20)

class BadScore:
    def __init__(self):
        self.current_score = 0

    def currentScoreToString(self):
        """ Returns the current score as a 4-digit string with leading zeros. """
        tempString = str(self.current_score)
        zerosToAdd = 4 - len(tempString)
        return str("0" * zerosToAdd + tempString)

    def draw(self, surface, score_string):
        text_rect = font.get_rect(score_string, size = 20)
        text_rect.left = 0
        text_rect.top = 0
        font.render_to(surface, text_rect, score_string, PURPLE, size = 20)

font = pygame.freetype.SysFont("Courier", 0)

S1 = Snake()
B1 = BadSnake(0)
B2 = BadSnake(1)
B3 = BadSnake(2)
A1 = Apple(randint(10,390), randint(10,390))
A2 = Apple(randint(10,390), randint(10,390))
A3 = Apple(randint(10,390), randint(10,390))
apples = pygame.sprite.Group()
apples.add(A1, A2, A3)
bad_snakes = pygame.sprite.Group()
bad_snakes.add(B1, B2, B3)
all_sprites = pygame.sprite.Group()
all_sprites.add(A1, A2, A3, S1, B1, B2, B3)

gameScore = Score()
enemyScore = BadScore()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
   
    S1.update()
    B1.update()
    B2.update()
    B3.update()
    DISPLAYSURF.fill(BLACK)
    A1.draw(DISPLAYSURF)
    A2.draw(DISPLAYSURF)
    A3.draw(DISPLAYSURF)
    apple_map = [A1.rect.center, A2.rect.center, A3.rect.center]
    B1.draw(DISPLAYSURF)
    B2.draw(DISPLAYSURF)
    B3.draw(DISPLAYSURF)
    S1.draw(DISPLAYSURF)
    gameScore.draw(DISPLAYSURF, gameScore.currentScoreToString())
    enemyScore.draw(DISPLAYSURF, enemyScore.currentScoreToString())
   
    if pygame.sprite.collide_rect(S1, A1):
        A1 = Apple(randint(10,390), randint(10,390))
        gameScore.current_score += 1
    if pygame.sprite.collide_rect(S1, A2):
        A2 = Apple(randint(10,390), randint(10,390))
        gameScore.current_score += 1
    if pygame.sprite.collide_rect(S1, A3):
        A3 = Apple(randint(10,390), randint(10,390))
        gameScore.current_score += 1
    
    for bad_snake in bad_snakes:
        if pygame.sprite.collide_rect(bad_snake, A1):
            A1 = Apple(randint(10,390), randint(10,390))
            enemyScore.current_score += 1
        if pygame.sprite.collide_rect(bad_snake, A2):
            A2 = Apple(randint(10,390), randint(10,390))
            enemyScore.current_score += 1
        if pygame.sprite.collide_rect(bad_snake, A3):
            A3 = Apple(randint(10,390), randint(10,390))
            enemyScore.current_score += 1
    
    
    
    
    pygame.display.update()
    FramePerSec.tick(FPS)