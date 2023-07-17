import pygame
import sys
import options
import grad
from random import randint, choice
from pygame.locals import *
import numpy
# Initialize Pygame
pygame.init()

# Set up screen
SCREEN_WIDTH = options.width
SCREEN_HEIGHT = options.height
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
# Load background image
bg_image = pygame.image.load('Glacial-mountains-parallax-background_vnitti/background_glacial_mountains.png')
bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Function to apply blur effect to the image

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Blurring the background image

    # Drawing the blurred background onto the screen
    screen.blit(bg_image, (0, 0))

    # Add your game objects and logic here

    # Update the display
    pygame.display.flip()

    # Set the frame rate
    clock.tick(60)
