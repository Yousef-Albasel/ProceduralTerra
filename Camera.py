import pygame
import numpy,noise
import sys
import options
import grad
import generic
from random import randint,choice
SCREEN_WIDTH = options.width
SCREEN_HEIGHT = options.height
# Camera settings
camera_direction = pygame.math.Vector2()
camera_x = SCREEN_WIDTH//2
camera_y = SCREEN_HEIGHT//2
camera_surface = pygame.Surface((SCREEN_WIDTH//4,SCREEN_HEIGHT//4))
def input():
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            camera_direction.y = -1
        elif keys[pygame.K_DOWN]:
            camera_direction.y = 1
        else:
            camera_direction.y = 0
        if keys[pygame.K_RIGHT]:
            camera_direction.x = 1
        elif keys[pygame.K_LEFT]:
            camera_direction.x = -1
        else:
            camera_direction.x = 0
def camera_move():
    global camera_x
    global camera_y

    max_camera_x = SCREEN_WIDTH - SCREEN_WIDTH // 3
    max_camera_y = SCREEN_HEIGHT - SCREEN_HEIGHT // 3
    # Horizontal movement
    camera_x += camera_direction.x * 2
    camera_x = max(0, min(camera_x, max_camera_x))  
    # Vertical movement
    camera_y += camera_direction.y * 2
    camera_y = max(0, min(camera_y, max_camera_y))  
