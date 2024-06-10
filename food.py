
from drawable import Drawable
import random
import math
import pygame
from constants import Constants
from monteCarlo import monteCarlo

class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def deleteSelf(self):
        if self.__class__.__name__ == "FoodHerbivore":
            Constants.FOODS.remove(self)
            for berrylope in Constants.BERRYLOPES:
                try:
                    berrylope.berries.remove(self)
                except ValueError:
                    pass
                    
        elif self.__class__.__name__ == "Grape":
            Constants.GRAPES.remove(self)

        

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
        self.cellX = x
        self.cellY = y

        coordX, coordY = Constants.calcCoords(x, y)
        super().__init__(coordX, coordY)
        self.color = (6, 50, 29)
        self.growIteration = 0
        self.grapeIteration = 0
        Constants.BACKGROUND.GRID[self.cellX, self.cellY] = (Constants.BACKGROUND.GRID[self.cellX][self.cellY][0], "Vine")

    def grow(self):
        if self.growIteration == 0:
            # Grow a small percentage of the time
            r = abs(monteCarlo("GREATER")[0])
            if r >= 0.95:
                # Grow algorithm
                # Select direction to grow in
                preferredDir = random.sample(range(4), 4)
                
                cell = None
                x = self.cellX
                y = self.cellY
                foundCell = False
                
                for i in preferredDir:
                    if i == 0:
                        if self.cellX != 0:
                            cell = Constants.BACKGROUND.GRID[x - 1, y]
                            if cell[1] == "":
                                x -= 1
                                foundCell = True
                                break
                    elif i == 1:
                        if self.cellX < Constants.xCELLS - 1:
                            cell = Constants.BACKGROUND.GRID[x + 1, y]
                            if cell[1] == "":
                                x += 1
                                foundCell = True
                                break
                    elif i == 2:
                        if self.cellY != 0:
                            cell = Constants.BACKGROUND.GRID[x, y - 1]
                            if cell[1] == "":
                                y -= 1
                                foundCell = True
                                break
                    elif i == 3:
                        if self.cellY < Constants.yCELLS - 1:
                            cell = Constants.BACKGROUND.GRID[x, y + 1]
                            if cell[1] == "":
                                y += 1
                                foundCell = True
                                break
                
                

                if foundCell:
                    # Mark cell to add new grapevine after the grapevine update loop ends
                    Constants.GRAPEVINE_ADDED = ((x, y), True) 
            
            self.growIteration = 15
        else:
            self.growIteration -= 1
            
    def growGrape(self):
        # Try to grow less frequently than every frame
        if self.grapeIteration == 0:
            if random.random() >= 0.95:
                # Calculate offset
                xOff, yOff = monteCarlo("GREATER")
                xOff *= Constants.TILE_WIDTH * 0.45
                yOff *= Constants.TILE_HEIGHT * 0.45
                Constants.GRAPES.add(Grape((self.x + Constants.TILE_WIDTH/2) + xOff, (self.y + Constants.TILE_HEIGHT/2) + yOff))
            
            self.grapeIteration = 10
            
        else:
            self.grapeIteration -= 1
    
    

    def draw(self):
        pygame.draw.rect(Constants.SCREEN, self.color, (self.x, self.y + Constants.TILE_HEIGHT/4, Constants.TILE_WIDTH, Constants.TILE_HEIGHT/2))
        
        
class Grape(Food, Drawable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (136, 6, 89)
        self.size = 2
    
    
    def draw(self):
        pygame.draw.circle(Constants.SCREEN, self.color, (self.x, self.y), self.size)
        pygame.draw.circle(Constants.SCREEN, Constants.BLACK, (self.x, self.y), self.size, 1)