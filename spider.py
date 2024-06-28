from organism import Organism

from constants import Constants
from monteCarlo import monteCarlo
import pygame
import math
import random

class Node():
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.attachedNodes = []

class Spider(Organism):
    MINIMUM_JUICE_TO_SPIN = 16
    JUICE_PER_NODE = 2
    NODE_DISTANCE = 50
    MAX_WEB_JUNCTION = 5
    
    def __init__(self, x, y, size, maxSpeed=0.3, maxSize=15.0, deathSize=6.0):
        super().__init__(x, y, size, maxSpeed, maxSize, deathSize)
        self.hungerThreshold = 60
        
        self.webJuice = 100
        self.makeWebJuiceIteration, self.MAKE_WEB_JUICE_ITERATION = 400, 400
        self.webLength = 0
        self.web = []
        
    
    def update(self):
        super().update()
        self.makeWebJuice()
        
    
    def makeWebJuice(self):
        if self.makeWebJuiceIteration <= 0:
            if self.hunger <= 35:
                return
            
            self.webJuice += 10
            self.hunger -= 3
            
            self.makeWebJuiceIteration = self.MAKE_WEB_JUICE_ITERATION
        else:
            self.makeWebJuiceIteration -= 1
    
    
    # Calc how fast to move to destination
    def calcSpeed(self):
        speedGoal = self.speed
        webFactor = 1
        
        # TODO: Slow web factor if spider is far from web
        if self.walkType == self.walkTypes.RANDOM:
            speedGoal = self.maxSpeed * 0.6
        elif self.walkType == self.walkTypes.SPIN_WEB:
            speedGoal = self.maxSpeed * 0.8
            
        if speedGoal > self.maxSpeed:
            speedGoal = self.maxSpeed
        if speedGoal < 0:
            speedGoal = 0
            
        # Modify if starving
        cappedHunger = self.hunger
        if cappedHunger > 80:
            cappedHunger = 80
        elif cappedHunger < 30:
            cappedHunger = 30
            
        hungerMultiplier = Constants.mapValue(cappedHunger, 30, 80, 0.6, 1)
        
        speedGoal *= hungerMultiplier
        
        self.speed = speedGoal
        
        
    # Check stats and determine next move
    def calcBestMovementType(self):
        # TODO: Calc how desperately web is needed
        if self.webLength < 1000:
            self.walkType = self.walkTypes.SPIN_WEB
        else:
            self.walkType = self.walkTypes.RANDOM
            
    
    #### Walk definitions ####
    def randomWalk(self):
        pass
    
    def spinWebWalk(self):
        # Not enough web juice
        if self.webJuice < self.MINIMUM_JUICE_TO_SPIN:
            return self.randomWalk()
        
        maxNodes = int(self.juice // self.JUICE_PER_NODE)
        
        maxWebDist = maxNodes * self.NODE_DISTANCE
        
        
        # Choose to attach to existing node, or make new strand
        # TODO: think about probability
        
        potentialNodes = []
        
        if random.randint(0, 1) <= 1:
            
            # Find close web node to attach to
            # TODO: use quadtree if applicable
            
            for webStrand in self.web:
                for node in webStrand:
                    dist = math.sqrt(node.x ** 2 + node.y ** 2)
                    
                    if dist > maxWebDist:
                        continue
                    
                    # Check if node already connected to self
                    if self in node.attachedNodes:
                        continue
                    
                    potentialNodes.append(node)
        
        # Spin random web    
        if potentialNodes == []:
            targetDist = abs(maxWebDist * monteCarlo("GREATER")[0])d
        index = random.randint(0, len(potentialNodes)-1)
            
    
   
            
            
    # Figure out where to move to and how to do it, then do it
    def move(self):
        destVector = (self.x, self.y)
        
        self.calcBestMovementType()
        self.calcSpeed()
        if self.walkType == self.walkTypes.RANDOM:
            destVector = self.randomWalk()
        elif self.walkType == self.walkTypes.SPIN_WEB:
            destVector = self.spinWebWalk()
    
    
    def draw(self):
        pygame.draw.circle(Constants.SCREEN, (0, 0, 0), (self.x, self.y), self.size)
        
    
    def die(self):
        print("todo implement spider die")