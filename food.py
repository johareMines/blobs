
from drawable import Drawable
import random
import pygame
from constants import Constants

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