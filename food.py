
from drawable import Drawable
import random
import pygame
from constants import Constants

class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        

class FoodHerbivore(Food, Drawable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.size = random.randint(3, 5)
        self.color = (0, 220, 0)
        self.rooted = True
    

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)
        pygame.draw.circle(screen, Constants.BLACK, (self.x, self.y), self.size, 1)