import pygame
import random
from drawable import Drawable
from simulation import Simulation
from constants import Constants
import numpy as np

from monteCarlo import monteCarlo
from blob import Blob


 

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
    



if __name__ == "__main__":
    simulation = Simulation()
    for _ in range(10):
        blob = Blob(random.uniform(0.0, float(Constants.SCREEN_WIDTH)), random.uniform(0.0, float(Constants.SCREEN_HEIGHT)), 10, (255, 0, 0))
        Simulation.ORGANISMS.append(blob)
    
    for _ in range(20):
        foodHerbivore = FoodHerbivore(random.uniform(0.0, float(Constants.SCREEN_WIDTH)), random.uniform(0.0, float(Constants.SCREEN_HEIGHT)))
        Simulation.FOODS.append(foodHerbivore)

    simulation.run()
