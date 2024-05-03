from organism import Organism
from monteCarlo import monteCarlo
from constants import Constants




class Blob(Organism):
    def __init__(self, x, y, size, color, maxSpeed=0.4):
        super().__init__(x, y, size, color, maxSpeed)
        self.hungerThreshold = 45

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
    
    def calcBestMovementType(self):
        if self.hunger <= self.hungerThreshold:
            self.walkType = self.walkTypes.FORRAGE
        else:
            self.walkType = self.walkTypes.RANDOM
    
    def randomWalk(self):
        # Modify speed
        self.calcSpeed()

        # Return a vector that will be added to current destination
        vect = monteCarlo("GREATER")
        vect = tuple(i * 4 for i in vect)
        first = self.destX + vect[0]
        second = self.destY + vect[1]
        return (first, second)
    
    def forageWalk(self):
        
        self.calcSpeed()

        # Find closest food
        closestFood = None
        closestDist = 999999999
        for food in Constants.FOODS:
            dist = self.calcDistance(food.x, food.y)

            if dist < closestDist:
                closestFood = food
                closestDist = dist
                
        
        # Navigate towards food
        dx = closestFood.x
        dy = closestFood.y

        returnVect = (dx, dy)
        return returnVect
    
    
    def move(self):
        velVector = (0, 0)

        # Update dest based on walk
        self.calcBestMovementType()
        if self.walkType == self.walkTypes.RANDOM:
            velVector = self.randomWalk()
        elif self.walkType == self.walkTypes.FORRAGE:
            velVector = self.forageWalk()
          

        # Apply change to existing destination
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
    
