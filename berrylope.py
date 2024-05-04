from organism import Organism
from monteCarlo import monteCarlo
from constants import Constants
import pygame

class Berrylope(Organism):
    def __init__(self, x, y, size=0, maxSpeed=0.8):
        super().__init__(x, y, size, maxSpeed)
        self.hungerThreshold = 70
        self.forageIteration = 0
        self.foodCollisionIteration = 0

        self.

        # Sprite image


    def calcSpeed(self):
        speedGoal = self.speed

        if self.walkType == self.walkTypes.RANDOM:
            speedGoal = self.maxSpeed 

        
        if speedGoal > self.maxSpeed:
            speedGoal = self.maxSpeed
        if speedGoal < 0:
            speedGoal = 0

        self.speed = speedGoal
    
    def calcHungerRate(self):
        return float((self.size / 1000) + (self.speed / 500))
    
    def calcBestMovementType(self):
        # if self.hunger <= self.hungerThreshold:
        #     self.walkType = self.walkTypes.FORRAGE
        # else:
            self.walkType = self.walkTypes.RANDOM

    def randomWalk(self):
        travelVect = monteCarlo("GREATER")
        return (float(self.x + travelVect[0] * 60), float(self.y + travelVect[1] * 60))

    def checkFoodCollision(self):
        print("gonk")

    def move(self):
        velVector = (0, 0)

        self.checkFoodCollision()

        # Update dest based on walk
        self.calcBestMovementType()
        self.calcSpeed()
        if self.walkType == self.walkTypes.RANDOM:
            velVector = self.randomWalk()
        

        # Apply change to destination
        self.destX, self.destY = velVector

        self.calcBoundaries()

        dist = self.calcDistance(self.destX, self.destY)

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

    
    def draw(self):
        pygame.draw.circle(Constants.SCREEN, Constants.GREEN, (self.x, self.y), self.size)
        pygame.draw.circle(Constants.SCREEN, Constants.BLACK, (self.x, self.y), self.size, 2)

        if Constants.DEVELOPER:
            pygame.draw.circle(Constants.SCREEN, Constants.BLACK, (self.destX, self.destY), 2)