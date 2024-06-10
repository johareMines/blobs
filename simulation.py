import pygame
import time
import sys
import psutil
import threading
import numpy as np
from drawable import Drawable
from constants import Constants
from food import Grapevine
import random
import math

class Background(Drawable):
    GRID = None
    def __init__(self, xCells, yCells):
        Constants.xCELLS = xCells
        Constants.yCELLS = yCells

        Constants.TILE_WIDTH = math.ceil(Constants.SCREEN_WIDTH / Constants.xCELLS)
        Constants.TILE_HEIGHT = math.ceil(Constants.SCREEN_HEIGHT / Constants.yCELLS)

        # self.grid = [[0 for _ in range(self.xCells)] for _ in range(self.yCells)]
        self.generateMap()
        self.createBackgroundSurface()

    

    def generateMap(self, maxIterations=750):
        # Different grid than static GRID
        GRID = np.zeros((Constants.xCELLS, Constants.yCELLS))

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
        
        
        
        # kernelUp1 = np.array([[0, 1, 1, 2, 1, 1, 0, 0, 0],
        #             [1, 2, 2, 3, 2, 2, 1, 0, 0],
        #             [1, 2, 3, 4, 3, 2, 1, 0, -1],
        #             [2, 3, 4, 5, 4, 3, 2, 1, -1],
        #             [1, 2, 3, 4, 3, 2, 0, -1, -1],
        #             [1, 2, 2, 3, 2, 1, 0, 0, -1],
        #             [0, 1, 1, 2, 1, 0, 0, 0, -1],
        #             [0, 0, 0, 1, 0, 0, 0, 0, 0],
        #             [0, 0, 0, 0, 0, 0, 0, 0, 0]])       
        
        # kernelUp2 = np.array([[0, 0, 1, 1, 1, 1, 0, 0, 0],
        #                     [0, 1, 2, 2, 2, 2, 1, 0, 0],
        #                     [1, 2, 3, 3, 3, 3, 2, 1, 0],
        #                     [1, 2, 3, 4, 4, 3, 2, 1, -1],
        #                     [0, 1, 2, 3, 3, 2, 1, 0, -1],
        #                     [-1, 0, 1, 2, 2, 1, 0, -1, -2],
        #                     [-1, -1, 0, 1, 1, 0, -1, -2, -2],
        #                     [-2, -2, -1, 0, 0, -1, -2, -3, -3],
        #                     [0, -2, -2, -1, -1, -2, -3, -3, -3]])  

        # kernelDown1 = np.array([[0, 0, 0, 0, 0, 0, 0, 1, 1],
        #                     [0, 0, 0, 0, 0, 0, 1, 2, 2],
        #                     [0, 0, 0, 1, 1, 1, 2, 3, 3],
        #                     [0, 0, 1, 2, 2, 2, 3, 3, 4],
        #                     [0, 1, 2, 3, 3, 3, 3, 4, 3],
        #                     [1, 2, 2, 3, 3, 2, 2, 1, 1],
        #                     [1, 2, 2, 2, 2, 2, 1, 0, 0],
        #                     [2, 2, 1, 1, 1, 1, 0, -1, -1],
        #                     [2, 1, 1, 0, 0, 0, -1, -1, -2]])
                
        # kernelDown2 = np.array([[-2, -3, -3, -1,  0,  1,  1,  1,  1],
        #                     [-3, -4, -4, -2, -1,  0,  1,  1,  2],
        #                     [-3, -4, -5, -3, -1,  0,  1,  2,  2],
        #                     [-2, -3, -4, -3, -1,  0,  1,  2,  3],
        #                     [0, -1, -2, -2,  0,  1,  2,  3,  3],
        #                     [1,  0, -1, -1,  1,  2,  3,  4,  3],
        #                     [2,  1,  0,  0,  1,  2,  3,  3,  2],
        #                     [3,  2,  1,  1,  1,  2,  2,  2,  1],
        #                     [3,  3,  2,  1,  1,  1,  1,  1,  0]])       
                
        # kernelUp3 = np.array([[1,  2,  2,  3,  3,  3,  2,  2,  1],
        #                     [0,  1,  2,  3,  4,  3,  2,  1,  0],
        #                     [-1,  0,  1,  2,  3,  2,  1,  0, -1],
        #                     [-2, -1,  0,  1,  2,  1,  0, -1, -2],
        #                     [-3, -2, -1,  0,  1,  0, -1, -2, -3],
        #                     [-3, -3, -2, -1,  0, -1, -2, -3, -3],
        #                     [-3, -3, -3, -2, -1, -2, -3, -4, -4],
        #                     [-3, -3, -3, -3, -2, -3, -4, -4, -4],
        #                     [-2, -3, -3, -3, -3, -3, -4, -4, -3]])  
        

        allKernels = (kernelUp1, kernelUp2, kernelUp3, kernelUp4, kernelDown1, kernelDown2, kernelDown3)
        
        

        # Perform convolution
        gridWidth, gridHeight = GRID.shape
        iterations = 0
        while (True):
            if iterations >= maxIterations:
                break

            # Select random kernel
            whichKer = random.randint(0, len(allKernels) - 1)
            kernel = allKernels[whichKer]

            # Rotate the kernel 0, 1, 2, or 3 times
            rotate = random.randint(0, 3)
            for i in range(0, rotate):
                kernel = np.rot90(kernel, k=-1)

            kernelWidth, kernelHeight = kernel.shape

            # Calc padding
            xPadding = kernelWidth // 2 # Floored division
            yPadding = kernelHeight // 2

            i = random.randint(xPadding, gridWidth - xPadding - 1)
            j = random.randint(yPadding, gridHeight - yPadding - 1)

            GRID[i-xPadding:i+xPadding+1, j-yPadding:j+yPadding+1] += kernel

            iterations += 1
        
        # Add rocks
        for i in range(5):
            i = random.randint(1, gridWidth - 2)
            j = random.randint(1, gridHeight - 2)

            GRID[i, j] = Constants.ROCK_HEIGHT
            
            bonusRocks = random.randint(0, 3)
            for _ in range(bonusRocks):
                x = y = 0
                while x == 0 and y == 0:
                    x, y = random.randint(-1, 1), random.randint(-1, 1)
                
                GRID[i+x, j+y] = Constants.ROCK_HEIGHT
        
        # Transform GRID into a tuple to store extra info about tile
        # Save in static var
        Background.GRID = np.empty((Constants.xCELLS, Constants.yCELLS), dtype=object)
        for i in range(Constants.xCELLS):
            for j in range(Constants.yCELLS):
                if GRID[i, j] == Constants.WATER_HEIGHT:
                    # print("Before: {}".format(GRID[i,j]))
                    Background.GRID[i, j] = (GRID[i, j], "Water")
                    # print("After: {}".format(Background.GRID[i,j]))
                elif GRID[i, j] == Constants.ROCK_HEIGHT:
                    Background.GRID[i, j] = (GRID[i, j], "Rock")
                elif GRID[i, j] == Constants.SNOW_HEIGHT:
                    Background.GRID[i, j] = (GRID[i, j], "Snow")
                else:
                    Background.GRID[i, j] = (GRID[i, j], "")
                
                # print(Background.GRID[i,j])
        
    def createBackgroundSurface(self):
        # Create a surface to draw the background once
        self.background_surface = pygame.Surface((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
        for i in range(Constants.xCELLS):
            for j in range(Constants.yCELLS):
                # Calculate color
                elevation = Background.GRID[i, j][0]

                if elevation == Constants.ROCK_HEIGHT:  # Rock
                    COLOR = (111, 111, 111)
                elif elevation < Constants.WATER_HEIGHT:  # Water
                    COLOR = (57, 95, 127)
                elif elevation > Constants.SNOW_HEIGHT:  # Snow
                    COLOR = (235, 240, 245)
                else:
                    COLOR = (30, 110, 45)
                    COLOR = (COLOR[0] + elevation, COLOR[1] + elevation * 4, COLOR[2] + elevation * 3)

                pygame.draw.rect(self.background_surface, COLOR,
                                 (Constants.TILE_WIDTH * i, Constants.TILE_HEIGHT * j, Constants.TILE_WIDTH,
                                  Constants.TILE_HEIGHT))

    
    def draw(self):
        Constants.SCREEN.blit(self.background_surface, (0,0))
        


class Simulation:
    __instance = None
    def __init__(self, width=1920, height=1080):
        if Simulation.__instance is not None:
            raise Exception("Singleton can't be instantiated multiple times.")
        else:
            pygame.init()

            # Windowed
            # self.screen = pygame.display.set_mode((width, height))
            
            screenInfo = pygame.display.Info()

            Constants.SCREEN_WIDTH = screenInfo.current_w
            Constants.SCREEN_HEIGHT = screenInfo.current_h

            Constants.SCREEN = pygame.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT), pygame.NOFRAME | pygame.RESIZABLE, display=0)
            
            self.clock = pygame.time.Clock()
            self.frame_times = []
            self.frame_print_time = time.time()

            Constants.BACKGROUND = Background(85, 50)
            
            
            self.cpuMonitor = CPUMonitor(1) # one second interval
            self.cpuMonitor.start()
                
    @staticmethod
    def get_instance():
        # Static method to get the singleton instance
        if Simulation.__instance is None:
            Simulation.__instance = Simulation()
        return Simulation.__instance

    def run(self):
        running = True
        while running:
            start_time = time.time() # For framerate calculation
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            Constants.SCREEN.fill((255, 255, 255))  # Clear the screen
            Constants.BACKGROUND.draw()

            for berrylope in Constants.BERRYLOPES:
                berrylope.update()
                
            for blob in Constants.BLOBS:
                blob.update()
            
            for grapevine in Constants.GRAPEVINES:
                grapevine.draw()
                grapevine.grow()
                grapevine.growGrape()
                
            for food in Constants.FOODS:
                food.draw()
            
            for grape in Constants.GRAPES:
                grape.draw()
            
            # Add grapevines after iteration is finished
            if Constants.GRAPEVINE_ADDED[1]:
                Constants.GRAPEVINES.add(Grapevine(Constants.GRAPEVINE_ADDED[0][0], Constants.GRAPEVINE_ADDED[0][1]))
                Constants.GRAPEVINE_ADDED = ((0, 0), False)

            # Kill required objects
            if len(Constants.DYING_BLOBS) > 0:
                for i in Constants.DYING_BLOBS:
                    Constants.BLOBS.remove(i)
                Constants.DYING_BLOBS = []
            if len(Constants.DYING_BERRYLOPES) > 0:
                for i in Constants.DYING_BERRYLOPES:
                    Constants.BERRYLOPES.remove(i)
                Constants.DYING_BERRYLOPES = []
            
            # Spawn new organisms
            if len(Constants.BORN_BLOBS) > 0:
                for i in Constants.BORN_BLOBS:
                    Constants.BLOBS.add(i)
                Constants.BORN_BLOBS = []
            if len(Constants.BORN_BERRYLOPES) > 0:
                for i in Constants.BORN_BERRYLOPES:
                    Constants.BERRYLOPES.add(i)
                Constants.BORN_BERRYLOPES = []
            
            pygame.display.flip() # Update display
            
            # Calc framerate
            self.clock.tick(60)  # FPS Limit
            end_time = time.time() 
            frame_time = end_time - start_time
            self.frame_times.append(frame_time)
            if len(self.frame_times) > 100:
                self.frame_times.pop(0)
            self.calculateFramerate()
            
            
            
        self.cpuMonitor.stop()
        self.cpuMonitor.join()
        pygame.quit()
        sys.exit()
        
        
    def calculateFramerate(self):
        if time.time() - self.frame_print_time < 1:
            return
        
        if len(self.frame_times) < 100:
            return
            
        avg_frame_time = sum(self.frame_times) / len(self.frame_times)
        fps = 1.0 / avg_frame_time
        print(f"FPS: {round(fps, 1)}")

        self.frame_print_time = time.time()
            
    
    
class CPUMonitor(threading.Thread):
    def __init__(self, interval):
        super().__init__()
        self.interval = interval
        self.stopped = threading.Event()
        self.process = psutil.Process()

    def run(self):
        while not self.stopped.wait(self.interval):
            cpu_percent = self.process.cpu_percent()
            print(f"CPU usage: {cpu_percent}%")

    def stop(self):
        self.stopped.set()