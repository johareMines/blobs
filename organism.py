from enum import Enum
import math
from constants import Constants
from monteCarlo import monteCarlo
from abc import ABC, abstractmethod
 

class Organism:
    def __init__(self, x, y, size, maxSpeed=0.4, maxSize=40.0, deathSize=5.0):
        self.x = x
        self.y = y
        self.destX = x
        self.destY = y
        self.size = size
        self.maxSize = maxSize
        self.maxSpeed = maxSpeed
        self.deathSize = deathSize
        self.speed = 0.0

        # Random initial hunger, more likely to be large
        self.hunger = abs(monteCarlo("LESS")[0] * 100)
        self.hungerThreshold = 50

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

    def update(self):
        self.hunger -= self.calcHungerRate()
        if self.hunger < 0.0:
            self.hunger = 0.0

        if self.hunger > 100.0:
            self.hunger = 100.0

        # Consume self if too hungry
        if self.hunger == 0.0:
            self.size -= 1
            self.hunger += 5
        
        # Check for starvation
        if self.size < self.deathSize:
            self.die()
        
        self.move()

        self.checkBirth()
        
        # Check size bounds
        if self.size > self.maxSize:
            self.size = self.maxSize
        self.draw()

    class walkTypes(Enum):
        RANDOM = "RANDOM"
        FORRAGE = "FORRAGE"
        MATE = "MATE"
        SPIN_WEB = "SPIN_WEB"
        GO_TO_POINT = "GO_TO_POINT"


    # Define methods child classes must define
    @abstractmethod
    def randomWalk(self):
        raise NotImplementedError("Parent class method must be overwritten")
    
    @abstractmethod
    def forageWalk(self):
        raise NotImplementedError("Parent class method must be overwritten")

    @abstractmethod
    def calcSpeed(self):
        raise NotImplementedError("Parent class method must be overwritten")
    
    @abstractmethod
    def calcHungerRate(self):
        raise NotImplementedError("Parent class method must be overwritten")

    @abstractmethod
    def calcBestMovementType(self):
        raise NotImplementedError("Parent class method must be overwritten")
    
    @abstractmethod
    def move(self):
        raise NotImplementedError("Parent class method must be overwritten")
    
    @abstractmethod
    def die(self):
        raise NotImplementedError("Parent class method must be overwritten")
    
    @abstractmethod
    def checkBirth(self):
        raise NotImplementedError("Parent class method must be overwritten")

    @abstractmethod
    def draw(self):
        raise NotImplementedError("Parent class method must be overwritten")
    
    


    