import pygame


import numpy as np
from drawable import Drawable
from constants import Constants
import random
import math

class Background(Drawable):
    GRID = None
    def __init__(self, xCells, yCells):
        self.xCells = xCells
        self.yCells = yCells

        # self.grid = [[0 for _ in range(self.xCells)] for _ in range(self.yCells)]
        self.generateMap()

    

    def generateMap(self, maxIterations=750):
        Background.GRID = np.zeros((self.xCells, self.yCells))

        kernelUp1 = np.array([[1, -1, 1],
                            [1, 2, 1],
                            [1, -1, 1]])
        
        kernelUp2 = np.array([[1, 1, 1],
                            [-1, 2, -1],
                            [1, 1, 1]])
        
        kernelUp3 = np.array([[-1, 1, 1, 1, -1],
                            [0, 2, 2, 2, 0],
                            [1, 2, 3, 2, 1],
                            [0, 2, 2, 2, 0],
                            [-1, 1, 1, 1, -1]])
        
        kernelUp4 = np.array([[0, 1, 1, 1, 0],
                            [1, 2, 2, 2, 1],
                            [1, 2, 2, 2, 1],
                            [1, 2, 2, 2, 1],
                            [0, 1, 1, 1, 0]])
        
        kernelDown1 = np.array([[-1, -2, -1],
                                [-2, -3, -2],
                                [-1, -2, -1]])
        
        kernelDown2 = np.array([[-1, -1, -1, -1, -1],
                                [-1, -1, -3, -1, -1],
                                [-1, -3, -3, -3, -1],
                                [-1, -1, -3, -1, -1],
                                [-1, -1, -1, -1, -1]])
        
        kernelDown3 = np.array([[0, -1, -1, -1, 0],
                            [-1, -2, -2, -2, -1],
                            [-1, -2, -2, -2, -1],
                            [-1, -2, -2, -2, -1],
                            [0, -1, -1, -1, 0]])
        
        

        # Perform convolution
        gridWidth, gridHeight = Background.GRID.shape
        iterations = 0
        while (True):
            if iterations >= maxIterations:
                break

            whichKer = random.randint(0, 6)
            if whichKer == 0:
                kernel = kernelUp1
            elif whichKer == 1:
                kernel = kernelUp2
            elif whichKer == 2:
                kernel = kernelUp3
            elif whichKer == 3:
                kernel = kernelUp4
            elif whichKer == 4:
                kernel = kernelDown1
            elif whichKer == 5:
                kernel = kernelDown2
            else:
                kernel = kernelDown3

            # Rotate the kernel sometimes
            rotate = random.randint(0, 1)
            if rotate == 0:
                kernel = np.rot90(kernel, k=-1)

            kernelWidth, kernelHeight = kernel.shape

            # Calc padding
            xPadding = kernelWidth // 2 # Floored division
            yPadding = kernelHeight // 2

            i = random.randint(xPadding, gridWidth - xPadding - 1)
            j = random.randint(yPadding, gridHeight - yPadding - 1)

            Background.GRID[i-xPadding:i+xPadding+1, j-yPadding:j+yPadding+1] += kernel

            iterations += 1
        
        # for i in Background.GRID: 
        #     print(i)

    
    def draw(self):
        tileWidth = math.ceil(Constants.SCREEN_WIDTH / self.xCells)
        tileHeight = math.ceil(Constants.SCREEN_HEIGHT / self.yCells)

        
        for i in range(self.xCells):
            for j in range(self.yCells):
                # Calculate color
                elevation = Background.GRID[i][j]

                if elevation < -7: # Water
                    COLOR = (57, 95, 127)
                elif elevation > 7: # Snow
                    COLOR = (235, 240, 245)
                else:
                    COLOR = (30, 110, 45)
                    COLOR = (COLOR[0] + elevation, COLOR[1] + elevation * 4, COLOR[2] + elevation * 3)


                pygame.draw.rect(Constants.SCREEN, COLOR, (tileWidth * i, tileHeight * j, tileWidth, tileHeight))



class Simulation:

    ORGANISMS = []
    FOODS = []
    
    def __init__(self, width=1920, height=1080):
        pygame.init()

        # Windowed
        # self.screen = pygame.display.set_mode((width, height))
        
        screenInfo = pygame.display.Info()

        # Simulation.SCREEN_WIDTH = screenInfo.current_w
        # Simulation.SCREEN_HEIGHT = screenInfo.current_h
        Constants.SCREEN_WIDTH = screenInfo.current_w
        Constants.SCREEN_HEIGHT = screenInfo.current_h

        # Simulation.SCREEN = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.FULLSCREEN, display=0)

        Constants.SCREEN = pygame.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT), pygame.FULLSCREEN, display=0)
        self.clock = pygame.time.Clock()

        Constants.BACKGROUND = Background(85, 50)
        

    def draw_organisms(self):
        Constants.SCREEN.fill((255, 255, 255))  # Clear the screen

        Constants.BACKGROUND.draw()

        for organism in Simulation.ORGANISMS:
            organism.draw(Constants.SCREEN)
        
        for food in Simulation.FOODS:
            food.draw(Constants.SCREEN)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            for organism in Simulation.ORGANISMS:
                organism.move()

            self.draw_organisms()
            self.clock.tick(165)  # FPS Limit

        pygame.quit()