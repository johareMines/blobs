from enum import Enum
import pygame
import math
from constants import Constants
 

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
        elif self.destX > Constants.SCREEN_WIDTH:
            self.destX = float(Constants.SCREEN_WIDTH - 1)
        
        if self.destY < 0:
            self.destY = 1.0
        elif self.destY > Constants.SCREEN_HEIGHT:
            self.destY = float(Constants.SCREEN_HEIGHT - 1)

    # Check desired move speed
    def calcSpeed(self):
        raise NotImplementedError("Parent class method must be overwritten")
    

    def calcDistance(self, targetX, targetY):
        x1 = math.pow(self.x - targetX, 2)
        y1 = math.pow(self.y - targetY, 2)

        return math.sqrt(x1 + y1)


    class walkTypes(Enum):
        RANDOM = "RANDOM"
        FORRAGE = "FORRAGE"

    def randomWalk(self):
        raise NotImplementedError("Parent class method must be overwritten")
    
    def forageWalk(self):
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
        pygame.draw.circle(screen, Constants.BLACK, (self.x, self.y), self.size, 2)


        if Constants.DEVELOPER:
            pygame.draw.circle(screen, Constants.BLACK, (self.destX, self.destY), 2)

        
        # spriteWidth, spriteHeight = self.scaledImage.get_rect().size

        # screen.blit(self.scaledImage, (self.x - spriteWidth / 2, self.y - spriteHeight / 2))


