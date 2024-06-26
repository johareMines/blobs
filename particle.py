from organism import Organism
from monteCarlo import monteCarlo
from constants import Constants
from enum import Enum
import pygame
import random
import math


class Particle(Organism):
    def __init__(self, x, y, maxSpeed=0.3):
        super().__init__(x, y, 2, maxSpeed, 2, deathSize=1)
        
        self.maxInfluenceDist = 200
    
        self.setType()
        self.setAttractionValues()
    
    def setType(self):
        # Select random particle type
        pType = random.randint(0, 1)#len(self.particleTypes)-1)
        typeEnum = self.particleTypeByIndex(pType)
        
        self.particleType = typeEnum
        
    def setAttractionValues(self):
        self.particleAttractions = {}
        for p in self.particleTypes:
            self.particleAttractions[p.name] = [random.uniform(-0.4, -0.2) for _ in range(len(self.particleTypes))]
    
    
    # Calculate push effect from all nearby particles
    def calcDest(self):
        velocities = []
        finalVelX, finalVelY = 0, 0
        for i, p in enumerate(Constants.PARTICLES):
            if p is self:
                continue
            
            dx = p.x - self.x
            dy = p.y - self.y
            
            dist = math.sqrt(dx ** 2 + dy ** 2)
            
            if dist > self.maxInfluenceDist:
                continue
            
            influenceIndex = p.particleTypeByEnum(p.particleType)
            influenceFactor = self.particleAttractions[self.particleType.name][influenceIndex]
            
            influence = influenceFactor * math.exp(-dist / self.maxInfluenceDist)
            
            dirX = dx / dist if dist != 0 else 0
            dirY = dy / dist if dist != 0 else 0
            
            velX = influence * dirX
            velY = influence * dirY
            
            velocities.append((velX, velY))
        
        for v in velocities:
            finalVelX += v[0]
            finalVelY += v[1]
        
        destX, destY = self.x + finalVelX, self.y + finalVelY
        velDist = self.calcDistance(destX, destY)
        
        # self.speed = velDist
        
        # return (self.x + finalVelX, self.y + finalVelY)
        return (destX, destY)
            
    def calcSpeed(self, dist):
        speedGoal = dist
        
        if speedGoal > self.maxSpeed:
            speedGoal = self.maxSpeed
        if speedGoal < 0:
            speedGoal = 0
            
        
        self.speed = speedGoal
    
    def move(self):
        
        
        destVector = self.calcDest()

        # Apply change to destination
        self.destX = destVector[0]
        self.destY = destVector[1]
        
        self.calcBoundaries()

        dist = self.calcDistance(self.destX, self.destY)
        self.calcSpeed(dist)

        if dist <= self.speed:
            self.x = self.destX
            self.y = self.destY
            
        else:
            dx = self.destX - self.x
            dy = self.destY - self.y
            velX = dx / dist * self.speed
            velY = dy / dist * self.speed

            self.x += velX
            self.y += velY
            
    def calcHungerRate(self):
        return 0
    
    def checkBirth(self):
        pass
    
    def draw(self):
        pygame.draw.circle(Constants.SCREEN, self.particleType.value, (self.x, self.y), self.size)
    
    def particleTypeByIndex(self, index):
        switch = {
            0: self.particleTypes.PINK,
            1: self.particleTypes.TEAL,
            2: self.particleTypes.GREY,
            3: self.particleTypes.MAIZE,
            4: self.particleTypes.INDIGO,
            5: self.particleTypes.ORANGE
        }
        return switch.get(index)
    
    def particleTypeByEnum(self, enum):
        switch = {
            self.particleTypes.PINK: 0,
            self.particleTypes.TEAL: 1,
            self.particleTypes.GREY: 2,
            self.particleTypes.MAIZE: 3,
            self.particleTypes.INDIGO: 4,
            self.particleTypes.ORANGE: 5,
        }
        return switch.get(enum)
    
    class particleTypes(Enum):
        PINK = (255, 130, 169)
        TEAL = (44, 175, 201)
        GREY = (156, 174, 169)
        MAIZE = (244, 224, 77)
        INDIGO = (84, 13, 110)
        ORANGE = (224, 92, 21)
        
     