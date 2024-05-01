import pygame
import random
import math
from enum import Enum

BLACK = (0, 0, 0)
RED = (255, 0, 0)
DEVELOPER = True

def monteCarlo(sign, skew=(0.0, 0.0)):
    i, j, k, l = [random.random() for _ in range(4)]

    if sign == "GREATER":
        while i > j:
            i = random.random()
    elif sign == "LESS":
        while i < j:
            i = random.random()

    # Allow negative values
    if k < 0.5:
        i *= -1
    if l < 0.5:
        j *= -1

    i += skew[0]
    j += skew[1]

    return (i, j)
    


class Drawable:
    def draw(self):
        raise NotImplementedError("Class must implement draw()")

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
    



class Organism:
    def __init__(self, x, y, size, color, maxSpeed=0.4):
        self.x = x
        self.y = y
        self.destX = x
        self.destY = y
        self.size = size
        self.color = color
        self.maxSpeed = maxSpeed
        self.speed = 0.0

        self.walkType = self.walkTypes.RANDOM

        spriteImage = pygame.image.load("images/blob.png")
        spriteImage = spriteImage.convert_alpha()

        scaledWidth = 109
        scaledHeight = 90

        self.scaledImage = pygame.transform.scale(spriteImage, (scaledWidth, scaledHeight))


    # Calc movement to next destination and execute
    def calcDest(self):
        dx = self.destX - self.x
        dy = self.destY - self.y
        dist = math.sqrt(dx**2 + dy**2)

        if dist <= self.speed:
            self.x = self.destX
            self.y = self.destY
        else:
            velX = dx / dist * self.speed
            velY = dy / dist * self.speed

            self.x += velX
            self.y += velY


    # Ensure organism doesn't leave map
    def calcBoundaries(self):
        if self.destX < 0:
            self.destX = 1.0
        elif self.destX > Simulation.SCREEN_WIDTH:
            self.destX = float(Simulation.SCREEN_WIDTH - 1)
        
        if self.destY < 0:
            self.destY = 1.0
        elif self.destY > Simulation.SCREEN_HEIGHT:
            self.destY = float(Simulation.SCREEN_HEIGHT - 1)

    # Check desired move speed
    def calcSpeed(self):
        raise NotImplementedError("Parent class method must be overwritten")


    class walkTypes(Enum):
        RANDOM = "RANDOM"

    def randomWalk(self):
        raise NotImplementedError("Parent class method must be overwritten")
        

    def move(self):
        velVector = (0, 0)
        # Select Walk
        if self.walkType == self.walkTypes.RANDOM:
            velVector = self.randomWalk()
          

        # Apply change to existing destination
        self.destX += velVector[0]
        self.destY += velVector[1]

        self.calcBoundaries() 

        self.calcDest()

    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)
        pygame.draw.circle(screen, BLACK, (self.x, self.y), self.size, 2)


        if DEVELOPER:
            pygame.draw.circle(screen, BLACK, (self.destX, self.destY), 2)

        
        # spriteWidth, spriteHeight = self.scaledImage.get_rect().size

        # screen.blit(self.scaledImage, (self.x - spriteWidth / 2, self.y - spriteHeight / 2))


class Blob(Organism):
    
    def calcSpeed(self):
        speedGoal = self.speed

        if self.walkType == self.walkTypes.RANDOM:
            
            if speedGoal < self.maxSpeed / 4:
                i = monteCarlo("GREATER", (0.2, 0.2))
            elif speedGoal < (self.maxSpeed / 4) * 3:
                i = monteCarlo("GREATER")
            else:
                i = monteCarlo("GREATER", (-0.2, -0.2))

            speedGoal += (i[0] * 0.1)
        
        if speedGoal > self.maxSpeed:
            speedGoal = self.maxSpeed
        if speedGoal < 0:
            speedGoal = 0
        
        self.speed = speedGoal
    
    def randomWalk(self):
        # Modify speed
        self.calcSpeed()

        # Return a vector that will be added to current destination
        vect = monteCarlo("GREATER")
        vect = tuple(i * 4 for i in vect)
        return (vect)

class Simulation:
    SCREEN_WIDTH = 0
    SCREEN_HEIGHT = 0

    ORGANISMS = []
    FOODS = []
    def __init__(self, width=1920, height=1080):
        pygame.init()
        # Windowed
        # self.screen = pygame.display.set_mode((width, height))
        
        screenInfo = pygame.display.Info()
        Simulation.SCREEN_WIDTH = screenInfo.current_w
        Simulation.SCREEN_HEIGHT = screenInfo.current_h
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.FULLSCREEN, display=0)

        self.clock = pygame.time.Clock()
        

    def draw_organisms(self):
        self.screen.fill((255, 255, 255))  # Clear the screen
        for organism in Simulation.ORGANISMS:
            organism.draw(self.screen)
        
        for food in Simulation.FOODS:
            food.draw(self.screen)
            
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

if __name__ == "__main__":
    simulation = Simulation()
    for _ in range(10):
        blob = Blob(random.uniform(0.0, float(simulation.SCREEN_WIDTH)), random.uniform(0.0, float(simulation.SCREEN_HEIGHT)), 10, (255, 0, 0))
        Simulation.ORGANISMS.append(blob)
    
    for _ in range(20):
        foodHerbivore = FoodHerbivore(random.uniform(0.0, float(Simulation.SCREEN_WIDTH)), random.uniform(0.0, float(Simulation.SCREEN_HEIGHT)))
        Simulation.FOODS.append(foodHerbivore)

    simulation.run()
