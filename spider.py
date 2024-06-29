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
    
    def update(self):
        self.move()
        self.draw()
    
    # Shift object and add nodes when appropriate
    def move(self):
        self.x = self.x + Spider.WEB_SHOOTING_SPEED * self.unitDx
        self.y = self.y + Spider.WEB_SHOOTING_SPEED * self.unitDy
        
        # Check if distance is far enough to add a node after checking for reached dest
        distToDest = math.sqrt((self.x - self.destX) ** 2 + (self.y - self.destY) ** 2)
        newNode = Node(self.x, self.y)
        
        def attachNewNode(self, newNode):
            self.nodes[-1].attachedNodes.append(newNode)
            newNode.attachedNodes.append(self.nodes[-1])
            self.nodes.append(newNode)
            
        # Conclude web building
        if distToDest < Spider.WEB_SHOOTING_SPEED + 1:
            if self in Constants.TERMINATED_WEB_SHOOTERS:
                print("maybe return bug")
                return
            attachNewNode(newNode)
            self.sendStrandToWeb()
            Constants.TERMINATED_WEB_SHOOTERS.append(self)
            return
        
        if distToDest - (len(self.nodes) * Spider.NODE_DISTANCE) < distToDest - Spider.NODE_DISTANCE:
            # Connect to previous node if it exists
            if self.nodes == []:
                self.nodes.append(newNode)
            else:
                attachNewNode(newNode)

    def draw(self):
        pygame.draw.circle(Constants.SCREEN, (24, 87, 191), (self.x, self.y), 5)
        
        
    def die(self):
        Constants.WEB_SHOOTERS.remove(self)
        
            
            
        

class Spider(Organism):
    MINIMUM_JUICE_TO_SPIN = 16
    JUICE_PER_NODE = 2
    NODE_DISTANCE = 50
    MAX_WEB_JUNCTION = 5
    WEB_SHOOTING_SPEED = 1
    
    def __init__(self, x, y, size, maxSpeed=0.3, maxSize=15.0, deathSize=6.0):
        super().__init__(x, y, size, maxSpeed, maxSize, deathSize)
        self.hungerThreshold = 60
        
        self.webJuice = 100
        self.makeWebJuiceIteration, self.MAKE_WEB_JUICE_ITERATION = 400, 400
        self.webLength = 0
        self.web = []
        self.webShooter = None
        
    
    def update(self):
        super().update()
        self.makeWebJuice()
        self.checkWebShooterCompletion()
        
    
    def makeWebJuice(self):
        
        if self.makeWebJuiceIteration <= 0:
            if self.hunger <= 35 and self.webJuice < 90:
                return
            
            self.webJuice += 10
            if self.webJuice >= 100:
                self.webJuice = 100
                
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
    
    def calcHungerRate(self):
        return 0
    
    def checkBirth(self):
        pass
        
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
        # Don't move if shooting web
        if self.webShooter is not None:
            return (self.x, self.y)
        
        # Not enough web juice
        if self.webJuice < self.MINIMUM_JUICE_TO_SPIN:
            return self.randomWalk()
        
        # Check silk level and determine how far is possible
        maxNodes = int(self.webJuice // self.JUICE_PER_NODE)
        
        maxWebDist = maxNodes * self.NODE_DISTANCE
        
        
        # Choose to attach to existing node, or make new strand
        # TODO: think about probability
        
        potentialNodes = []
        
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
            # dx, dy = (random.randint(int(-maxWebDistSqrt), int(maxWebDistSqrt)) for _ in range(2))
            
            # Choose dy so that total dist can't be greater than maxWebDist
            dx = random.randint(-maxWebDist, maxWebDist)
            maxDy = math.floor(math.sqrt(maxWebDistSquared - (dx ** 2)))
            
            dy = random.randint(-maxDy, maxDy)
            
            # debugDist = math.sqrt(dx ** 2 + dy ** 2)
            # print("Random web, distance: {} | Max Web Distance: {}".format(debugDist, maxWebDist))
            
            
            webDestX = self.x + dx
            webDestY = self.y + dy
            
            # self.shootWebStrand(webDestX, webDestY)
            self.webShooter = WebShooter(webDestX, webDestY, self.x, self.y)
            
            
        
        return (self.x, self.y)
            
        # index = random.randint(0, len(potentialNodes)-1)
    
    
    def updateWeb(self, webStrand):
        self.web.append(webStrand)
    
    
    
    def checkWebShooterCompletion(self):
        if self.webShooter in Constants.TERMINATED_WEB_SHOOTERS:
            self.webShooter = None
            
    
    # def shootWebStrand(self, destX, destY):
        
    #     if self.webShooter is not None:
    #         return
        
        
        
        
        # # Calculate distance between start and end points
        # dist = math.sqrt((destX - self.x) ** 2 + (destY - self.y) ** 2)

        # # Calculate the direction vector
        # dx = destX - self.x
        # dy = destY - self.y

        # # Normalize the direction vector
        # unit_dx = dx / dist
        # unit_dy = dy / dist

        # # Check if spider is on existing node
        # # TODO: implement quadtree to make this query better than O(n^2) (Currently iterates through every node in the web @ worst case scenario, loops through every node of every strand)
        # currentNode = None
        # nodeFound = False
        # for strand in self.web:
        #     if nodeFound:
        #         break
        #     for node in strand:
        #         nodeDist = math.sqrt((node.x - self.x) ** 2 + (node.y - self.y) ** 2)
                
        #         # Spider is close enough to existing node
        #         if nodeDist <= 5:
        #             currentNode = node
        #             nodeFound = True
        #             break
        
        # nodes = []
        # if currentNode is not None:
        #     nodes.append(currentNode)
        # else:
        #     nodes.append(Node(self.x, self.y))
        # nodes = [(self.x, self.y)]

        # # Step size (distance between nodes)
        # step_size = 50

        # # Add nodes every 50 units
        # num_steps = int(dist // step_size)
        # for step in range(1, num_steps + 1):
        #     node_x = self.x + step * step_size * unit_dx
        #     node_y = self.y + step * step_size * unit_dy
        #     nodes.append((node_x, node_y))

        # # Add the final destination node
        # nodes.append((destX, destY))

        # return nodes
        
        
    # def addNodesRecursively(self, dist):
       
    #    # When passed in a dist:
    # #    numSteps = math.ceil(dist / Spider.NODE_DISTANCE)

    #     # Base case
    #     if dist < Spider.NODE_DISTANCE:

    #     else:
    #         self.addNodesRecursively(dist - Spider.NODE_DISTANCE)


      
            
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
        pass
        
    
    def die(self):
        print("todo implement spider die") 