from organism import Organism
from monteCarlo import monteCarlo
from constants import Constants
from food import FoodHerbivore



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
    
    def forageWalk(self):
        self.calcSpeed()

        # Find closest food
        closestFood = None
        closestDist = 999999999
        for food in Constants.FOODS:
            dist = self.calcDistance(food.x, food.y)

            if dist < closestDist:
                closestFood = food
