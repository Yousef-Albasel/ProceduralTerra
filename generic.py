
import pygame
import numpy,noise
import sys
import options
import grad
import generic
from random import randint,choice
lightblue = [0,191,255]
blue = [65,105,225]
green = [34,139,34]
darkgreen = [0,100,0]
sandy = [210,180,140]
beach = [238, 214, 175]
snow = [255, 250, 250]
mountain = [139, 137, 137]
SCREEN_WIDTH = options.width
SCREEN_HEIGHT = options.height
# In Perlin noise : 
# Scale adjusts the zoom
# The number of level of details you want your perlin noise to have is octaves
# Lucunarity adjusts the level of details
# presistence adjusts number that determines how much each octave contributes to the overall shape (adjusts amplitude
map_surface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
map = numpy.zeros((SCREEN_WIDTH,SCREEN_HEIGHT))
def GeneratePerlinMap(seed=0,scale = 50.0,octaves = 6,persistence = 0.5,lacunarity = 2.0):
    for x in range(SCREEN_WIDTH):
        for y in range(SCREEN_HEIGHT):
            map[x][y] = noise.pnoise2(x/scale,y/scale,octaves=octaves,persistence=persistence,lacunarity=lacunarity,repeatx=1024,repeaty=1024,base=seed)

    print("New map generated : seed =",seed)

    return map


def DisplayMap(map):
    for x in range(SCREEN_WIDTH):
        for y in range(SCREEN_HEIGHT):
            threshold=0
            noiseVal=map[x][y]+1
            if noiseVal < threshold + 0.95:
                map_surface.set_at((x, y), options.blue)
            elif noiseVal < threshold + 1.0:
                map_surface.set_at((x, y), options.beach)
            elif noiseVal < threshold + 1.25:
                map_surface.set_at((x, y), options.green)
            elif noiseVal < threshold + 1.3:
                map_surface.set_at((x, y), options.darkgreen)
            elif noiseVal < threshold + 1.35:
                map_surface.set_at((x, y), options.mountain)
            elif noiseVal < threshold + 2.0:
                map_surface.set_at((x, y), options.snow)
    return map_surface
DisplayMap(GeneratePerlinMap(0))

threshold = 0

def GetGradPerlin(map):
    island_noise = numpy.zeros((SCREEN_WIDTH, SCREEN_HEIGHT))
    circle_grad = grad.getCricleGrad()

    for x in range(SCREEN_WIDTH):
        for y in range(SCREEN_HEIGHT):
            island_noise[x][y] = (map[x][y] * circle_grad[x][y])
            if island_noise[x][y] > 0:
                island_noise[x][y] *= 20 # for more contrast

    # get it between 0 and 1
    max_grad = numpy.max(island_noise)
    world_noise = island_noise / max_grad
    return world_noise

def CreateIsland(map):
    island_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    for x in range(SCREEN_WIDTH):
        for y in range(SCREEN_HEIGHT):
            if map[x][y] < threshold + 0.05:
                island_surface.set_at((x, y), options.blue)
            elif map[x][y] < threshold + 0.055:
                island_surface.set_at((x, y), options.sandy)
            elif map[x][y] < threshold + 0.1:
                island_surface.set_at((x, y), options.beach)
            elif map[x][y] < threshold + 0.25:
                island_surface.set_at((x, y), options.green)
            elif map[x][y] < threshold + 0.6:
                island_surface.set_at((x, y), options.darkgreen)
            elif map[x][y] < threshold + 0.7:
                island_surface.set_at((x, y), options.mountain)
            elif map[x][y] < threshold + 1.0:
                island_surface.set_at((x, y), options.snow)
    return island_surface

island_surface = CreateIsland(GetGradPerlin(map))

