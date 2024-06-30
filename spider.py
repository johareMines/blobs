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


class WebShooter():
    def __init__(self, destX, destY, startX, startY, spider):
        self.destX = destX
        self.destY = destY
        self.startX, self.x = (startX for _ in range(2))
        self.startY, self.y = (startY for _ in range(2))
        self.x = startX
        self.y = startY

        
        self.dx = destX - startX
        self.dy = destY - startY
        
        self.dist = math.sqrt(self.dx ** 2 + self.dy ** 2)

        self.unitDx = self.dx / self.dist
        self.unitDy = self.dy / self.dist
        
        self.nodes = []
        
        self.spider = spider
        
        print("Shooter spawned, dist: {}".format(self.dist))
        self.attachNewNode()
    
    def update(self):
        self.move()
        self.draw()
        
    
    def attachNewNode(self):
        newNode = Node(self.x, self.y)
        if self.nodes == []:
            self.nodes.append(newNode)
        else:
            self.nodes[-1].attachedNodes.append(newNode)
            newNode.attachedNodes.append(self.nodes[-1])
            self.nodes.append(newNode)
            
    
    # Shift object and add nodes when appropriate
    def move(self):
        self.x = self.x + Spider.WEB_SHOOTING_SPEED * self.unitDx
        self.y = self.y + Spider.WEB_SHOOTING_SPEED * self.unitDy
        
        # Check if distance is far enough to add a node after checking for reached dest
        distToDest = math.sqrt((self.x - self.destX) ** 2 + (self.y - self.destY) ** 2)
        
        # Conclude web building if last node
        if distToDest < Spider.WEB_SHOOTING_SPEED + 1:
            if self in Constants.TERMINATED_WEB_SHOOTERS:
                print("maybe return bug")
                return
            self.attachNewNode()
            self.spider.updateWeb(self.nodes, self.dist)
            Constants.TERMINATED_WEB_SHOOTERS.append(self)
            return
        
        # Attach new node
        if distToDest + (len(self.nodes) * Spider.NODE_DISTANCE) < self.dist - Spider.NODE_DISTANCE:
            self.attachNewNode()

    def draw(self):
        pygame.draw.circle(Constants.SCREEN, (24, 87, 191), (self.x, self.y), 5)
        
        # Draw line from start to current dest to give the illusion of shooting
        pygame.draw.line(Constants.SCREEN, (0, 0, 0), (self.startX, self.startY), (self.x, self.y), 3)
        
        
    def die(self):
        self.spider.webShooter = None
        Constants.WEB_SHOOTERS.remove(self)
        
            
            
        

class Spider(Organism):
    MINIMUM_JUICE_TO_SPIN = 16
    JUICE_PER_NODE = 8
    NODE_DISTANCE = 25
    MAX_WEB_JUNCTION = 5
    WEB_SHOOTING_SPEED = 3
    
    def __init__(self, x, y, size, maxSpeed=0.3, maxSize=15.0, deathSize=6.0):
        super().__init__(x, y, size, maxSpeed, maxSize, deathSize)
        self.hungerThreshold = 60
        
        self.silk = 100
        self.makeSilkIteration, self.MAKE_WEB_JUICE_ITERATION = 400, 400
        self.webLength = 0
        self.web = []
        self.webShooter = None
        
        self.randomDest = None
        
    
    def update(self):
        super().update()
        self.makeSilk()
        
    
    def makeSilk(self):
        
        if self.makeSilkIteration <= 0:
            if self.hunger <= 35 and self.silk < 90:
                return
            
            self.silk += 10
            if self.silk >= 100:
                self.silk = 100
                
            self.hunger -= 3
            
            self.makeSilkIteration = self.MAKE_WEB_JUICE_ITERATION
        else:
            self.makeSilkIteration -= 1
    
    
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
    
    def calcHungerRate(self):
        return 0
    
    def checkBirth(self):
        pass
        
    # Check stats and determine next move
    def calcBestMovementType(self):
        # TODO: Calc how desperately web is needed
        
        if self.webShooter is not None:
            self.walkType = self.walkTypes.SPIN_WEB
        else:
            if self.randomDest is not None:
                self.walkType = self.walkTypes.RANDOM
            else:
                self.walkType = self.walkTypes.SPIN_WEB
            
            
    
    #### Walk definitions ####
    def randomWalk(self):
       
        # Check if destination is in mind
        if self.randomDest is None:
            # Choose random node in web to move to
            possibleNodes = []
            for strand in self.web:
                for node in strand:
                    dist = self.calcDistance(node.x, node.y)
                    if dist > Spider.NODE_DISTANCE * 1.2 and dist < 100:
                        possibleNodes.append(node)
            
            if possibleNodes == []:
                return (self.x, self.y)
            
            i = random.randint(0, len(possibleNodes)-1)
            self.randomDest = (possibleNodes[i].x, possibleNodes[i].y)
        else:
             # Check if destination reached
            if self.calcDistance(self.randomDest[0], self.randomDest[1]) < 2:
                self.randomDest = None
                return (self.x, self.y)
        
        return self.randomDest
        
        
    
    def spinWebWalk(self):
        # Don't move if shooting web
        if self.webShooter is not None:
            return (self.x, self.y)
        
        # Not enough web juice
        if self.silk < self.MINIMUM_JUICE_TO_SPIN:
            return self.randomWalk()
        
        # Check silk level and determine how far is possible
        maxNodes = int(self.silk // self.JUICE_PER_NODE)
        
        maxWebDist = maxNodes * self.NODE_DISTANCE
        
        
        # Choose to attach to existing node, or make new strand
        # TODO: think about probability
        
        potentialNodes = []
        
        # ConnectToExistingNode
        if random.randint(0, 1) <= 0:
            
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
        
        
        ## Spin web ##
        webDestX = None
        webDestY = None
        
        # Spin random web    
        if potentialNodes == []:
            # Choose coordinate less than maxWebDist away
            maxWebDistSquared = maxWebDist ** 2
            
            # Choose dy so that total dist can't be greater than maxWebDist
            dx = random.randint(-maxWebDist, maxWebDist)
            
            maxDy = math.floor(math.sqrt(maxWebDistSquared - (dx ** 2))) # Pythag theorem
            
            dy = random.randint(-maxDy, maxDy)
            
            webDestX = self.x + dx
            webDestY = self.y + dy
            
            # self.shootWebStrand(webDestX, webDestY)
            shooter = WebShooter(webDestX, webDestY, self.x, self.y, self)
            self.webShooter = shooter
            Constants.WEB_SHOOTERS.add(shooter)
            
            
        
        return self.randomWalk()
            
        # index = random.randint(0, len(potentialNodes)-1)
    
    
    def updateWeb(self, webStrand, distAdded):
        self.web.append(webStrand)
        self.webLength += distAdded
        
    
    # Figure out where to move to and how to do it, then do it
    def move(self):
        destVector = (self.x, self.y)
        
        self.calcBestMovementType()
        self.calcSpeed()
        if self.walkType == self.walkTypes.RANDOM:
            destVector = self.randomWalk()
        elif self.walkType == self.walkTypes.SPIN_WEB:
            destVector = self.spinWebWalk()
    
        self.destX = destVector[0]
        self.destY = destVector[1]
        
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
        self.drawWeb()
        pygame.draw.circle(Constants.SCREEN, (0, 0, 0), (self.x, self.y), self.size)
    
        
    def drawWeb(self):
        for strand in self.web:
            for i in range(len(strand)-1):
                # Add line between current strand and next strand
                pygame.draw.line(Constants.SCREEN, (0, 0, 0), (strand[i].x, strand[i].y), (strand[i+1].x, strand[i+1].y), 3)
        
    
    def die(self):
        print("todo implement spider die") 