from organism import Organism
from monteCarlo import monteCarlo
from constants import Constants
import pygame
from food import FoodHerbivore

class Berrylope(Organism):
    def __init__(self, x, y, size=0, maxSpeed=0.8):
        super().__init__(x, y, size, maxSpeed)
        self.hungerThreshold = 70
        self.forageIteration = 0
        self.foodCollisionIteration = 0

        self.randomSelected = False
        self.randomWaitTimer = -1
        
        self.berries = []
        self.growIteration = 0

        # Sprite image

    def update(self):
        super().update()
        self.growBerry()
        
    
    def growBerry(self):
        if len(self.berries) >= 10:
            return
        if self.growIteration == 0:
            if self.hunger > 65:
                # Calculate offset
                xOff, yOff = monteCarlo("GREATER")
                xOff *= self.size * 0.85
                yOff *= self.size * 0.85
                
                berry = FoodHerbivore(self.x + xOff, self.y + yOff)
                Constants.FOODS.add(berry)
                self.berries.append(berry)
                
                self.hunger -= 5
                self.growIteration = 50
        else:
            self.growIteration -= 1
    
    def moveBerries(self, xShift, yShift):
        for i in self.berries:
            i.x += xShift
            i.y += yShift
            
        
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
        if self.randomSelected == False:
            travelVect = monteCarlo("GREATER")
            self.randomSelected = True
            multiplier = 80
            return (float(self.x + travelVect[0] * multiplier), float(self.y + travelVect[1] * multiplier))
        elif self.x == self.destX and self.y == self.destY:
            # Start wait timer
            if self.randomWaitTimer == -1:
                self.randomWaitTimer = 60
            elif self.randomWaitTimer == 0:
                self.randomSelected = False
                self.randomWaitTimer = -1
            else:
                self.randomWaitTimer -= 1
            return(self.destX, self.destY)
        else:
            # Continue to selected destination
            return(self.destX, self.destY)

    def checkFoodCollision(self):
        x = 0

    def move(self):
        velVector = (0, 0)

        self.checkFoodCollision()

        # Update dest based on walk
        self.calcBestMovementType()
        self.calcSpeed()
        if self.walkType == self.walkTypes.RANDOM:
            velVector = self.randomWalk()
        

        # Apply change to destination
        self.destX = velVector[0]
        self.destY = velVector[1]

        self.calcBoundaries()

        dist = self.calcDistance(self.destX, self.destY)

        if dist <= self.speed:
            # Move Berries
            self.moveBerries(self.destX - self.x, self.destY - self.y)
            
            self.x = self.destX
            self.y = self.destY
            
        else:
            dx = self.destX - self.x
            dy = self.destY - self.y
            velX = dx / dist * self.speed
            velY = dy / dist * self.speed

            self.x += velX
            self.y += velY
            
            self.moveBerries(velX, velY)

    
    def draw(self):
        pygame.draw.circle(Constants.SCREEN, Constants.GREEN, (self.x, self.y), self.size)
        pygame.draw.circle(Constants.SCREEN, Constants.BLACK, (self.x, self.y), self.size, 2)

        if Constants.DEVELOPER:
            pygame.draw.circle(Constants.SCREEN, Constants.BLACK, (self.destX, self.destY), 2)