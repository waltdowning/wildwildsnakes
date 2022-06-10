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

# Initialize variables for scores.
score = 0
bad_score = 0

# Initialize a list to hold tuples representing the (x,y) coordinates of apples for the purpose of NPC movement logic.
apple_map = [(0,0),(0,0),(0,0)]

class Snake(pygame.sprite.Sprite):
    """ The player's character, controlled by keypad. Keeps moving unless it hits the edge of the screen
    or spacebar is pressed. """
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
    """ An NPC snake with a target integer from 0 to 2 representing the apple it wants. Moves left/right then
    up/down until it reaches the apple. """
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
    """ An apple at given (x, y) coordinates. """
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/apple.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x,y) 
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Score:
    """ The player's score, which will draw itself in white in the upper right. """
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
    """ The collective NPC score, which will draw itself in purple in the upper left. """
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

# Initialize snakes and apples and scores.
S1 = Snake()
B1 = BadSnake(0)
B2 = BadSnake(1)
B3 = BadSnake(2)
A1 = Apple(randint(10,390), randint(10,390))
A2 = Apple(randint(10,390), randint(10,390))
A3 = Apple(randint(10,390), randint(10,390))

gameScore = Score()
enemyScore = BadScore()

# Add sprites to groups (only currently using bad_snakes group, but leaving the rest in for the future)
apples = pygame.sprite.Group()
apples.add(A1, A2, A3)
bad_snakes = pygame.sprite.Group()
bad_snakes.add(B1, B2, B3)
all_sprites = pygame.sprite.Group()
all_sprites.add(A1, A2, A3, S1, B1, B2, B3)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    # Update all snakes.
    S1.update()
    B1.update()
    B2.update()
    B3.update()
   
    # Clear the screen.
    DISPLAYSURF.fill(BLACK)
    
    # Draw the apples and update the map of locations.
    A1.draw(DISPLAYSURF)
    A2.draw(DISPLAYSURF)
    A3.draw(DISPLAYSURF)
    apple_map = [A1.rect.center, A2.rect.center, A3.rect.center]
    
    # Draw the NPC snakes.
    B1.draw(DISPLAYSURF)
    B2.draw(DISPLAYSURF)
    B3.draw(DISPLAYSURF)
    S1.draw(DISPLAYSURF)

    # Draw the scores.
    gameScore.draw(DISPLAYSURF, gameScore.currentScoreToString())
    enemyScore.draw(DISPLAYSURF, enemyScore.currentScoreToString())
   
   # Check for the player reaching an apple. If so, repop the apple and update score.
    if pygame.sprite.collide_rect(S1, A1):
        A1 = Apple(randint(10,390), randint(10,390))
        gameScore.current_score += 1
    if pygame.sprite.collide_rect(S1, A2):
        A2 = Apple(randint(10,390), randint(10,390))
        gameScore.current_score += 1
    if pygame.sprite.collide_rect(S1, A3):
        A3 = Apple(randint(10,390), randint(10,390))
        gameScore.current_score += 1
    
    # Check for each NPC snake reaching an apple. If so, repop the apple and update score.
    # Note the NPC snake can eat any apple, not just the one it is targeting.
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