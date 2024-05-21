
from drawable import Drawable
import random
import pygame
from constants import Constants
from monteCarlo import monteCarlo

class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def deleteSelf(self):
        Constants.FOODS.remove(self)

        

class FoodHerbivore(Food, Drawable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.size = random.randint(3, 5)
        self.color = (0, 220, 0)
        self.rooted = True
    

    def draw(self):
        pygame.draw.circle(Constants.SCREEN, self.color, (self.x, self.y), self.size)
        pygame.draw.circle(Constants.SCREEN, Constants.BLACK, (self.x, self.y), self.size, 1)
    

class Grapevine(Food, Drawable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (6, 50, 29)
        self.growIteration = 0

    def grow(self):
        if self.growIteration == 0:
            # Grow a small percentage of the time
            r = abs(monteCarlo("GREATER")[0])
            if r >= 0.95:
                # Grow algorithm
                x = 0
            
            self.growIteration = 5
        else:
            self.growIteration -= 1

    def draw(self):
        pygame.draw.rect(Constants.SCREEN, self.color, (self.x, self.y, Constants.TILE_WIDTH, Constants.TILE_HEIGHT/2))