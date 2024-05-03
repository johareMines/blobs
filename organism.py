from enum import Enum
import pygame
import math
from constants import Constants
from monteCarlo import monteCarlo
 

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

        # Random initial hunger, more likely to be large
        self.hunger = abs(monteCarlo("LESS")[0] * 100)
        self.hungerThreshold = 50

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

    def calcBestMovementType(self):
        if self.hunger <= self.hungerThreshold:
            self.walkType = self.walkTypes.FORRAGE
        else:
            self.walkType = self.walkTypes.RANDOM

    # Ensure organism doesn't leave map
    def calcBoundaries(self):
        if self.destX < 0:
            self.destX = 1.0
        elif self.destX > Constants.SCREEN_WIDTH:
            self.destX = float(Constants.SCREEN_WIDTH - 1)
        
        if self.destY < 0:
            self.destY = 1.0
        elif self.destY > Constants.SCREEN_HEIGHT:
            self.destY = float(Constants.SCREEN_HEIGHT - 1)


    def calcDistance(self, targetX, targetY):
        x1 = math.pow(self.x - targetX, 2)
        y1 = math.pow(self.y - targetY, 2)

        return math.sqrt(x1 + y1)


    class walkTypes(Enum):
        RANDOM = "RANDOM"
        FORRAGE = "FORRAGE"


    # Define methods child classes must define
    def randomWalk(self):
        raise NotImplementedError("Parent class method must be overwritten")
    
    def forageWalk(self):
        raise NotImplementedError("Parent class method must be overwritten")

    def calcSpeed(self):
        raise NotImplementedError("Parent class method must be overwritten")
    
    def calcHungerRate(self):
        raise NotImplementedError("Parent class method must be overwritten")

    def update(self):
        self.hunger -= self.calcHungerRate()
        if self.hunger < 0.0:
            self.hunger = 0.0

        # Consume self if too hungry
        if self.hunger == 0.0:
            self.size -= 1
            self.hunger += 3

        
        self.calcBestMovementType()

    def move(self):
        velVector = (0, 0)

        self.update()

        # Update dest based on walk
        if self.walkType == self.walkTypes.RANDOM:
            velVector = self.randomWalk()
        elif self.walkType == self.walkTypes.FORRAGE:
            velVector = self.forageWalk()
          

        # Apply change to existing destination
        self.destX = velVector[0]
        self.destY = velVector[1]

        self.calcBoundaries() 

        self.calcDest()

    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)
        pygame.draw.circle(screen, Constants.BLACK, (self.x, self.y), self.size, 2)


        if Constants.DEVELOPER:
            pygame.draw.circle(screen, Constants.BLACK, (self.destX, self.destY), 2)

        
        # spriteWidth, spriteHeight = self.scaledImage.get_rect().size

        # screen.blit(self.scaledImage, (self.x - spriteWidth / 2, self.y - spriteHeight / 2))


