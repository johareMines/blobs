from enum import Enum
import pygame
import collections

class Constants:
    DEVELOPER = True
    MONITOR_INTERVAL = 5
    BLACK = (0, 0, 0)
    GREEN = (30, 150, 90)
    SCREEN_WIDTH = None
    SCREEN_HEIGHT = None
    TILE_WIDTH = None
    TILE_HEIGHT = None
    xCELLS = None
    yCELLS = None

    SCREEN = None
    BACKGROUND = None
    
    QUADTREE = None

    # ORGANISMS = []
    BORN_BLOBS = []
    DYING_BLOBS = []
    BLOBS = set({})
    
    BORN_BERRYLOPES = []
    DYING_BERRYLOPES = []
    MATING_BERRYLOPES = []
    BERRYLOPES = set({})
    
    PARTICLES = set({})
    
    SPIDERS = set({})
    WEB_SHOOTERS = set({})
    TERMINATED_WEB_SHOOTERS = []
    
    
    FOODS = set({})
    GRAPEVINE_ADDED = ((0, 0), False)
    GRAPEVINES = set({})
    GRAPES = set({})


    WATER_HEIGHT = -12
    ROCK_HEIGHT = -101
    SNOW_HEIGHT = 12
    
    
    # @staticmethod
    # def batchQuery(particles, maxInfluenceDist):
    #     queryRanges = []
    #     results = {}
        
    #     for p in particles:
    #         rangeQuery = pygame.Rect(p.x - maxInfluenceDist, p.y - maxInfluenceDist, maxInfluenceDist * 2, maxInfluenceDist * 2)
    #         queryRanges.append((p, rangeQuery))
    #         results[p] = []
        
    #     for p, rangeQuery in queryRanges:
    #         found = Constants.QUADTREE.query(rangeQuery, [])
    #         results[p] = found
        
    #     return results
    
    SUPERCELL_SIZE = 80
    
    class displays(Enum):
        MAIN = 0
        SECONDARY = 1
        
    DISPLAY = displays.MAIN
    
        
    def calcCoords(x, y):
        x *= Constants.TILE_WIDTH
        y *= Constants.TILE_HEIGHT
        return (x, y)
    
    def calcCell(x, y):
        x = int(x // Constants.TILE_WIDTH)
        y = int(y // Constants.TILE_HEIGHT)
        return (x, y)
    
    def mapValue(input, inputMin, inputMax, outputMin, outputMax):
        return outputMin + ((input - inputMin) / (inputMax - inputMin)) * (outputMax - outputMin)
    
    
