import pygame
import time
import sys
import psutil
import threading
import numpy as np
from drawable import Drawable
from constants import Constants
from food import Grapevine
from Player.player import Player
import random
import math
from exceptions import SingletonMultipleInstantiationException

from constants import Constants
from food import Grapevine
from Organisms.blob import Blob
from Organisms.berrylope import Berrylope
from Organisms.spider import Spider

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

    

    def generateMap(self, maxIterations=1500):
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
        
        kernelUp5 = np.array([[0, 1, 1, 2, 1, 1, 0, 0, 0],
                    [1, 2, 2, 3, 2, 2, 1, 0, 0],
                    [1, 2, 3, 4, 3, 2, 1, 0, -1],
                    [2, 3, 4, 5, 4, 3, 2, 1, -1],
                    [1, 2, 3, 4, 3, 2, 0, -1, -1],
                    [1, 2, 2, 3, 2, 1, 0, 0, -1],
                    [0, 1, 1, 2, 1, 0, 0, 0, -1],
                    [0, 0, 0, 1, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0]])
        
        kernelUp6 = np.array([[0, 0, 1, 1, 1, 1, 0, 0, 0],
                            [0, 1, 2, 2, 2, 2, 1, 0, 0],
                            [1, 2, 3, 3, 3, 3, 2, 1, 0],
                            [1, 2, 3, 4, 4, 3, 2, 1, -1],
                            [0, 1, 2, 3, 3, 2, 1, 0, -1],
                            [-1, 0, 1, 2, 2, 1, 0, -1, -2],
                            [-1, -1, 0, 1, 1, 0, -1, -2, -2],
                            [-2, -2, -1, 0, 0, -1, -2, -3, -3],
                            [0, -2, -2, -1, -1, -2, -3, -3, -3]]) 
        
        kernelUp7 = np.array([[0, 0, 0, 0, 0, 0, 0, 1, 1],
                            [0, 0, 0, 0, 0, 0, 1, 2, 2],
                            [0, 0, 0, 1, 1, 1, 2, 3, 3],
                            [0, 0, 1, 2, 2, 2, 3, 3, 4],
                            [0, 1, 2, 3, 3, 3, 3, 4, 3],
                            [1, 2, 2, 3, 3, 2, 2, 1, 1],
                            [1, 2, 2, 2, 2, 2, 1, 0, 0],
                            [2, 2, 1, 1, 1, 1, 0, -1, -1],
                            [2, 1, 1, 0, 0, 0, -1, -1, -2]])
        
        #####
        
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
        
        kernelDown4 = np.array([[-2, -3, -3, -1,  0,  1,  1,  1,  1],
                            [-3, -4, -4, -2, -1,  0,  1,  1,  2],
                            [-3, -4, -5, -3, -1,  0,  1,  2,  2],
                            [-2, -3, -4, -3, -1,  0,  1,  2,  3],
                            [0, -1, -2, -2,  0,  1,  2,  3,  3],
                            [1,  0, -1, -1,  1,  2,  3,  4,  3],
                            [2,  1,  0,  0,  1,  2,  3,  3,  2],
                            [3,  2,  1,  1,  1,  2,  2,  2,  1],
                            [3,  3,  2,  1,  1,  1,  1,  1,  0]])       
        
        kernelDown5 = np.array([[1,  2,  2,  3,  3,  3,  2,  2,  1],
                            [0,  1,  2,  3,  4,  3,  2,  1,  0],
                            [-1,  0,  1,  2,  3,  2,  1,  0, -1],
                            [-2, -1,  0,  1,  2,  1,  0, -1, -2],
                            [-3, -2, -1,  0,  1,  0, -1, -2, -3],
                            [-3, -3, -2, -1,  0, -1, -2, -3, -3],
                            [-3, -3, -3, -2, -1, -2, -3, -4, -4],
                            [-3, -3, -3, -3, -2, -3, -4, -4, -4],
                            [-2, -3, -3, -3, -3, -3, -4, -4, -3]])
        
        kernelDown6 = np.array([[0, 0, 0, 0, 0, 0, 0, -1, -1],
                            [0, 0, 0, 0, 0, 0, -1, -2, -2],
                            [0, 0, 0, -1, -1, -1, -2, -3, -3],
                            [0, 0, -1, -2, -2, -2, -3, -3, -4],
                            [0, -1, -2, -3, -3, -3, -3, -4, -3],
                            [-1, -2, -2, -3, -3, -2, -2, -1, -1],
                            [-1, -2, -2, -2, -2, -2, -1, 0, 0],
                            [-2, -2, -1, -1, -1, -1, 0, -1, -1],
                            [-2, -1, -1, 0, 0, 0, -1, -1, -2]])
        
        kernelDown7 = np.array([[-1,  -2,  -2,  -3,  -3,  -3,  -2,  -2,  -1],
                            [0,  -1,  -2,  -3,  -4,  -3,  -2,  -1,  0],
                            [-1,  0,  -1,  -2,  -3,  -2,  -1,  0, -1],
                            [-2, -1,  0,  1,  2,  1,  0, -1, -2],
                            [-3, -2, -1,  0,  1,  0, -1, -2, -3],
                            [-3, -3, -2, -1,  0, -1, -2, -3, -3],
                            [-3, -3, -3, -2, -1, -2, -3, -4, -4],
                            [-3, -3, -3, -3, -2, -3, -4, -4, -4],
                            [-2, -3, -3, -3, -3, -3, -4, -4, -3]])
        

        allKernels = (kernelUp1, kernelUp2, kernelUp3, kernelUp4, kernelUp5, kernelUp6, kernelUp7, kernelDown1, kernelDown2, kernelDown3, kernelDown4, kernelDown5, kernelDown6, kernelDown7)
        

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
        for i in range(60):
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
                    Constants.ROCKS.add((int(i * Constants.TILE_WIDTH), int(j * Constants.TILE_HEIGHT)))
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
            raise SingletonMultipleInstantiationException()#Exception("Singleton can't be instantiated multiple times.")
        else:
            pygame.init()

            # Windowed
            # self.screen = pygame.display.set_mode((width, height))
            
            screenInfo = pygame.display.Info()

            Constants.SCREEN_WIDTH = screenInfo.current_w
            Constants.SCREEN_HEIGHT = screenInfo.current_h

            Constants.SCREEN = pygame.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.RESIZABLE, display=Constants.DISPLAY.value)
            
            self.clock = pygame.time.Clock()
            self.frame_times = []
            self.frame_print_time = time.time()

            Constants.BACKGROUND = Background(125, 75)
            
            
            self.performanceMonitor = PerformanceMonitor(Constants.MONITOR_INTERVAL) # Interval in seconds
            self.performanceMonitor.start()

            self.playerKeyMappings = {
                pygame.K_w: "up",
                pygame.K_s: "down",
                pygame.K_a: "left",
                pygame.K_d: "right"
            }


            # Setup game objects
            for _ in range(10):
                blob = Blob(random.uniform(0.0, float(Constants.SCREEN_WIDTH)), random.uniform(0.0, float(Constants.SCREEN_HEIGHT)), 10)
                Constants.BLOBS.add(blob)
            
            for _ in range(5):
                berrylope = Berrylope(random.uniform(0.0, float(Constants.SCREEN_WIDTH)), random.uniform(0.0, float(Constants.SCREEN_HEIGHT)), 25)
                Constants.BERRYLOPES.add(berrylope)
            
            # for _ in range(20):
            #     foodHerbivore = FoodHerbivore(random.uniform(0.0, float(Constants.SCREEN_WIDTH)), random.uniform(0.0, float(Constants.SCREEN_HEIGHT)))
            #     Constants.FOODS.add(foodHerbivore)


            for _ in range(4):
                x, y = random.randint(0, Constants.xCELLS - 4), random.randint(0, Constants.yCELLS - 4)
                Constants.GRAPEVINES.add(Grapevine(x,y))
        
            for _ in range(2):
                Constants.SPIDERS.add(Spider(random.uniform(400, 1200), random.uniform(300, 900), 11))

            
            Constants.PLAYER = Player.getInstance()
                
    @staticmethod
    def get_instance():
        # Static method to get the singleton instance
        if Simulation.__instance is None:
            Simulation.__instance = Simulation()
        return Simulation.__instance

    # Handle keyboard press
    def playerKeyDown(self, input):
        Constants.PLAYER_INPUTS[input] = 1
        

    def playerKeyUp(self, input):
        pass

    def run(self):
        running = True
        
        # Constants.QUADTREE = Quadtree(0, 0, Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT)
        # Insert particles into the quadtree
        # for particle in Constants.PARTICLES:
        #     Constants.QUADTREE.insert(particle)
        
        while running:
            start_time = time.time() # For framerate calculation
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_BACKSPACE:
                        Constants.GRAPES = set({})
                    elif event.unicode == '`':
                        if Constants.DEVELOPER:
                            Constants.DEVELOPER = False
                        else:
                            Constants.DEVELOPER = True

                    elif event.key in self.playerKeyMappings:
                        Player.getInstance().playerInputs[self.playerKeyMappings[event.key]] = 1
                        print(f"Keydown {Player.getInstance().playerInputs}")
                elif event.type == pygame.KEYUP:
                    if event.key in self.playerKeyMappings:
                        Player.getInstance().playerInputs[self.playerKeyMappings[event.key]] = 0
                        print(f"Keyup {Player.getInstance().playerInputs}")
            
            Constants.SCREEN.fill((255, 255, 255))  # Clear the screen
            Constants.BACKGROUND.draw()
            
            # # Clear quadtree (more efficient than making a new one)
            # Constants.QUADTREE.clear()

            for berrylope in Constants.BERRYLOPES:
                berrylope.update()
                
            for blob in Constants.BLOBS:
                blob.update()
                
            
            
            for webShooter in Constants.WEB_SHOOTERS:
                webShooter.update()
                
            for spider in Constants.SPIDERS:
                spider.update()
            
            
            # Particle.batchCalcDest(Constants.PARTICLES)
            
            # for particle in Constants.PARTICLES:
            #     particle.update()
            
            # for particle in Constants.PARTICLES:
            #     Constants.QUADTREE.update(particle)
            
            
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
            if len(Constants.TERMINATED_WEB_SHOOTERS) > 0:
                for i in Constants.TERMINATED_WEB_SHOOTERS:
                    i.die()
                Constants.TERMINATED_WEB_SHOOTERS = []
            
            # Spawn new organisms
            if len(Constants.BORN_BLOBS) > 0:
                for i in Constants.BORN_BLOBS:
                    Constants.BLOBS.add(i)
                Constants.BORN_BLOBS = []
            if len(Constants.BORN_BERRYLOPES) > 0:
                for i in Constants.BORN_BERRYLOPES:
                    Constants.BERRYLOPES.add(i)
                Constants.BORN_BERRYLOPES = []
                

            Constants.PLAYER.update()


            # Draw circle at mouse position
            # self.drawMouseCircle()
            
            pygame.display.flip() # Update display
            
            # Calc framerate
            self.clock.tick(60)  # FPS Limit
            end_time = time.time() 
            frame_time = end_time - start_time
            self.frame_times.append(frame_time)
            if len(self.frame_times) > 200:
                self.frame_times.pop(0)
            self.calculateFramerate()
            
            
            
        self.performanceMonitor.stop()
        self.performanceMonitor.join()
        pygame.quit()
        sys.exit()
        
    def drawMouseCircle(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if 0 <= mouse_x <= Constants.SCREEN_WIDTH and 0 <= mouse_y <= Constants.SCREEN_HEIGHT:
            pygame.draw.circle(Constants.SCREEN, (0, 255, 0), (mouse_x, mouse_y), 10)
            print("Mouse x: {} | Mouse y: {}".format(mouse_x, mouse_y))
    
    def calculateFramerate(self):
        if time.time() - self.frame_print_time < Constants.MONITOR_INTERVAL:
            return
        
        if len(self.frame_times) < 200:
            return
            
        avg_frame_time = sum(self.frame_times) / len(self.frame_times)
        fps = 1.0 / avg_frame_time
        print(f"FPS: {round(fps, 1)}")

        self.frame_print_time = time.time()
            
    
    
class PerformanceMonitor(threading.Thread):
    def __init__(self, interval):
        super().__init__()
        self.interval = interval
        self.stopped = threading.Event()
        self.process = psutil.Process()

    def run(self):
        while not self.stopped.wait(self.interval):
            self.monitorCPU()
            self.monitorMemory()
            self.monitorObjects()

    def monitorCPU(self):
        cpu_percent = self.process.cpu_percent()
        print(f"CPU usage: {cpu_percent}%")
    
    def monitorMemory(self):
        memory_info = self.process.memory_info()
        print(f"Memory Usage: {memory_info.rss / (1024 * 1024)} MB")  # Convert to MB
    
    def monitorObjects(self):
        print(f"Blobs: {len(Constants.BLOBS)} | Berrylopes: {len(Constants.BERRYLOPES)} | Grapevines: {len(Constants.GRAPEVINES)} | Grapes: {len(Constants.GRAPES)}")# | Particles: {len(Constants.PARTICLES)}")
    
    def stop(self):
        self.stopped.set()

