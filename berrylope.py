from organism import Organism
from monteCarlo import monteCarlo
from constants import Constants
import pygame
import random
import sys
from food import FoodHerbivore

class Berrylope(Organism):
    def __init__(self, x, y, size=0, maxSpeed=0.6, maxSize=45.0, pregnantIncubateTime=2000, deathSize=20.0):
        super().__init__(x, y, size, maxSpeed, maxSize, deathSize)
        self.hungerThreshold = 75 # Forage for food if hungrier < this
        self.growBerryHungerThreshold = 70 # Hunger needed to grow berries
        self.mateHungerThreshold = 70
        
        self.forageIteration = 0
        self.foodCollisionIteration = 0

        self.randomSelected = False
        self.randomWaitTimer = -1
        
        self.berries = []
        self.growIteration = 0
        
        self.gender = random.randint(0, 1)
        self.pregnant = False
        self.inHeat = False # Looking for a mate
        self.chosenPartner = None
        self.noAvailableMates = False
        self.isMating = False
        self.pregnantIteration, self.PREGNANT_ITERATION = pregnantIncubateTime, pregnantIncubateTime
        self.birthIteration = random.randint(0, 30)

        # Sprite image

    def update(self):
        super().update()
        self.growBerry()
        self.checkProcreate()
        self.checkBirth()
        
    
    def growBerry(self):
        if len(self.berries) >= 10:
            return
        if self.growIteration == 0:
            if self.hunger > self.growBerryHungerThreshold:
                # Calculate offset
                xOff, yOff = monteCarlo("GREATER")
                xOff *= self.size * 0.85
                yOff *= self.size * 0.85
                
                berry = FoodHerbivore(self.x + xOff, self.y + yOff)
                Constants.FOODS.add(berry)
                self.berries.append(berry)
                
                self.hunger -= 15
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
            speedGoal = self.maxSpeed * 0.6
        elif self.walkType == self.walkTypes.FORRAGE:
            speedGoal = self.maxSpeed * 0.75
        elif self.walkType == self.walkTypes.MATE:
            speedGoal = self.maxSpeed * 0.8
        
        if speedGoal > self.maxSpeed:
            speedGoal = self.maxSpeed
        if speedGoal < 0:
            speedGoal = 0

        self.speed = speedGoal
    
    def calcHungerRate(self):
        return float((self.size / 1300) + (self.speed / 500))
    
    def calcBestMovementType(self):
        if self.inHeat and self.noAvailableMates == False:
            self.walkType = self.walkTypes.MATE
        elif self.hunger <= self.hungerThreshold:
            self.walkType = self.walkTypes.FORRAGE
        else:
            self.walkType = self.walkTypes.RANDOM
        
        self.noAvailableMates = False

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
        
    def forageWalk(self):
        # Finish chosen navigation
        if self.randomSelected == True:
            return self.randomWalk()
        
        if self.forageIteration == 0:
            # Find closest food
            self.closestFood = None
            closestDist = 999999999
            for grape in Constants.GRAPES:
                dist = self.calcDistance(grape.x, grape.y)

                if dist < closestDist:
                    self.closestFood = grape
                    closestDist = dist
                
            self.forageIteration = 10
        else:
            self.forageIteration -= 1

        # If there is no food
        if not self.closestFood:
            dx = self.x
            dy = self.y
            returnVect = (dx, dy)
        else:
            # Navigate towards food
            dx = self.closestFood.x
            dy = self.closestFood.y

            returnVect = (dx, dy)
        return returnVect
    
    def reproductionWalk(self):
        destX, destY = self.x, self.y
        
        if self.chosenPartner is None:
            
            # Add self to mating pool
            if self not in Constants.MATING_BERRYLOPES:
                Constants.MATING_BERRYLOPES.append(self)
                
            # Choose partner from available list
            
            closestDist = sys.maxsize # Largest int
            for berrylope in Constants.MATING_BERRYLOPES:
                # Check if they want to mate with self
                if berrylope.chosenPartner == self:
                    self.chosenPartner = berrylope
                    break
                elif berrylope.chosenPartner is not None:
                    continue
                
                dist = self.calcDistance(berrylope.x, berrylope.y)
                if dist < closestDist and (berrylope.gender != self.gender):
                    closestDist = dist
                    self.chosenPartner = berrylope
        else:
            
            # If other organism started mating, stop moving
            if self.isMating:
                self.mate()
                return(self.x, self.y)
            
            
            # Check for close distance (successful mating)
            dist = self.calcDistance(self.chosenPartner.x, self.chosenPartner.y)
            
            if dist < self.size:
                self.chosenPartner.isMating = True
                self.mate()
                
        if self.chosenPartner is not None:
            destX = self.chosenPartner.x
            destY = self.chosenPartner.y
        else:
            self.noAvailableMates = True
            destX, destY = self.getDest()
            
        
        # Navigate towards chosen partner
        return (destX, destY)
    
    def mate(self):
        self.inHeat = False
        if self.gender == 0:
            self.pregnant = True
            
        # Remove self from dating pool
        for berrylope in Constants.BERRYLOPES:
            if berrylope.chosenPartner == self:
                berrylope.chosenPartner = None
        Constants.MATING_BERRYLOPES.remove(self)
        self.chosenPartner = None
        self.isMating = False

    def checkFoodCollision(self):
        if self.hunger >= 95:
            return
        for i in Constants.GRAPES:
            dist = self.calcDistance(i.x, i.y)

            # Eat food
            if dist < self.size:
                i.deleteSelf()
                
                self.size += 1
                self.hunger += i.size * 5
                break
    
    def checkProcreate(self):
        if self.pregnant or self.inHeat:
            return
        # Don't overpopulate
        if self.birthIteration <= 0:
            # Check for health
            if self.hunger > 60:
                self.inHeat = True # Will attempt to look for a partner
                self.birthIteration = 350
            
        else:
            self.birthIteration -= 1
            
    def checkBirth(self):
        if not self.pregnant:
            return
        
        if self.pregnantIteration == 0:
            # Give birth
            size = random.randint(23, 27)
            newMaxSpeed = self.maxSpeed + (monteCarlo("GREATER")[0] * 0.1)
            newMaxSize = self.maxSize + (monteCarlo("GREATER")[0] * 1.5)
            newPregnantTime = self.PREGNANT_ITERATION + (monteCarlo("GREATER")[0] * 100)
            Constants.BORN_BERRYLOPES.append(Berrylope(self.x, self.y, size, newMaxSpeed, newMaxSize, pregnantIncubateTime=newPregnantTime))
            
            self.pregnant = False
            self.pregnantIteration == self.PREGNANT_ITERATION
        else:
            self.pregnantIteration -= 1
    
    def getDest(self):
        # Update dest based on walk
        self.calcBestMovementType()
        self.calcSpeed()
        if self.walkType == self.walkTypes.RANDOM:
            destVector = self.randomWalk()
        elif self.walkType == self.walkTypes.FORRAGE:
            destVector = self.forageWalk()
        elif self.walkType == self.walkTypes.MATE:
            destVector = self.reproductionWalk()
        
        return destVector
    
    def move(self):
        velVector = (0, 0)

        self.checkFoodCollision()

        
        destVector = self.getDest()

        # Apply change to destination
        self.destX = destVector[0]
        self.destY = destVector[1]

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
        
        if self.gender == 0:
            pygame.draw.circle(Constants.SCREEN, Constants.BLACK, (self.x, self.y), 5)

        if Constants.DEVELOPER:
            pygame.draw.circle(Constants.SCREEN, Constants.BLACK, (self.destX, self.destY), 2)
            
    def die(self):
        for berry in self.berries:
            berry.deleteSelf()
        
        Constants.DYING_BERRYLOPES.append(self)