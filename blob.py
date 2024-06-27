from organism import Organism
from particle import Particle
from monteCarlo import monteCarlo
from constants import Constants
import pygame
import random




class Blob(Organism):
    def __init__(self, x, y, size, maxSpeed=0.4, maxSize=25.0, deathSize=8.0):
        super().__init__(x, y, size, maxSpeed, maxSize, deathSize)
        self.hungerThreshold = 45
        self.forageIteration = 0
        self.foodCollisionIteration = 0
        self.birthIteration, self.BIRTH_ITERATION = 2000, 2000
        
        self.color = (255, 0, 0)
        
        self.poopIteration, self.POOP_ITERATION = random.randint(0, 800), 800

        # spriteImage = pygame.image.load("images/Small.png")
        # spriteImage = spriteImage.convert_alpha()

        # scaledWidth = size
        # scaledHeight = size

        # self.scaledImage = pygame.transform.scale(spriteImage, (scaledWidth, scaledHeight))

    def update(self):
        super().update()
        self.checkRandomPoop()

    # Calc how fast to move to destination
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
        
        elif self.walkType == self.walkTypes.FORRAGE:
            speedGoal = self.maxSpeed / 2
        
        if speedGoal > self.maxSpeed:
            speedGoal = self.maxSpeed
        if speedGoal < 0:
            speedGoal = 0
        
        self.speed = speedGoal

    def calcHungerRate(self):
        return float(self.size / 1000)
    
    # Check stats and determine next move
    def calcBestMovementType(self):
        if self.hunger <= self.hungerThreshold:
            self.walkType = self.walkTypes.FORRAGE
        else:
            self.walkType = self.walkTypes.RANDOM
    
    
    #### Walk definitions ####
    def randomWalk(self):
        vect = monteCarlo("GREATER")
        vect = tuple(i * 4 for i in vect)
        first = self.destX + vect[0]
        second = self.destY + vect[1]
        return (first, second)
    
    def forageWalk(self):

        if self.forageIteration == 0:
            # Find closest food
            self.closestFood = None
            closestDist = 999999999
            for food in Constants.FOODS:
                dist = self.calcDistance(food.x, food.y)

                if dist < closestDist:
                    self.closestFood = food
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
    
    # Eat food if close and in the mood
    def checkFoodCollision(self):
        if self.hunger >= 95:
            return
        for i in Constants.FOODS:
            dist = self.calcDistance(i.x, i.y)

            # Eat food
            if dist < self.size:
                i.deleteSelf()
                self.size += int(i.size * 0.5)
                self.hunger += i.size * 6
                break

    # Reproduce if successful
    def checkBirth(self):
        if self.birthIteration <= 0:
            if (self.size >= self.maxSize * 0.8) and self.hunger >= 70:
                # Reproduce
                self.size = self.size / 2
                self.hunger -= 30
                newMaxSpeed = self.maxSpeed + (monteCarlo("GREATER")[0] * 0.1)
                newMaxSize = self.maxSize + (monteCarlo("GREATER")[0] * 1.5)
                newBlob = Blob(self.x, self.y, self.size, maxSpeed=newMaxSpeed, maxSize=newMaxSize)
                Constants.BORN_BLOBS.append(newBlob)
                self.birthIteration = self.BIRTH_ITERATION
        else:
            self.birthIteration -= 1
    
    # Poop a particle sometimes
    def checkRandomPoop(self):
        if self.poopIteration <= 0:
            # Chance to poo
            if random.random() > 0.65:
                Constants.PARTICLES.add(Particle(self.x, self.y))
            self.poopIteration = self.POOP_ITERATION
        else:
            self.poopIteration -= 1

    # Figure out where to move to and how to do it, then do it
    def move(self):
        velVector = (0, 0)

        # Only check sometimes to save processing power
        if self.foodCollisionIteration == 0:
            self.checkFoodCollision()
            self.foodCollisionIteration = 5
        else:
            self.foodCollisionIteration -= 1

        # Update dest based on walk
        self.calcBestMovementType()
        self.calcSpeed()
        if self.walkType == self.walkTypes.RANDOM:
            velVector = self.randomWalk()
        elif self.walkType == self.walkTypes.FORRAGE:
            velVector = self.forageWalk()
          

        # Apply change to destination
        self.destX = velVector[0]
        self.destY = velVector[1]

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
        pygame.draw.circle(Constants.SCREEN, self.color, (self.x, self.y), self.size)
        pygame.draw.circle(Constants.SCREEN, Constants.BLACK, (self.x, self.y), self.size, 2)


        if Constants.DEVELOPER:
            pygame.draw.circle(Constants.SCREEN, Constants.BLACK, (self.destX, self.destY), 2)

        
        # spriteWidth, spriteHeight = self.scaledImage.get_rect().size

        # screen.blit(self.scaledImage, (self.x - spriteWidth / 2, self.y - spriteHeight / 2))

    
    def die(self):
        # Constants.BLOBS.remove(self) # Can't remove while iterating through blob set
        Constants.DYING_BLOBS.append(self)