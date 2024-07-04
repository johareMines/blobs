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


class WebQueue():
    def __init__(self, startPoint, queue):
        self.startPoint = startPoint
        self.queue = queue

class WebShooter():
    def __init__(self, destX, destY, spider):
        self.destX = destX
        self.destY = destY
        self.startX, self.x = (spider.x for _ in range(2))
        self.startY, self.y = (spider.y for _ in range(2))
        

        
        self.dx = destX - self.x
        self.dy = destY - self.y
        
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
        # Check if node exists close to point
        for strand in self.spider.web:
            for node in strand:
                dist = math.sqrt((self.x - node.x) ** 2 + (self.y - node.y) ** 2)
                if dist < 2:
                    newNode = node

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
        if distToDest < Spider.WEB_SHOOTING_SPEED + 0.1:
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
        # Debug circle
        # pygame.draw.circle(Constants.SCREEN, (24, 87, 191), (self.x, self.y), 5)
        
        # Draw line from start to current dest to give the illusion of shooting
        pygame.draw.line(Constants.SCREEN, (0, 0, 0), (self.startX, self.startY), (self.x, self.y), 3)
        
        
    def die(self):
        self.spider.webShooter = None
        Constants.WEB_SHOOTERS.remove(self)
        
            
            
            
            
            
            
            
            
            
            
            
        

class Spider(Organism):
    MINIMUM_JUICE_TO_SPIN = 16
    JUICE_PER_NODE = 6
    NODE_DISTANCE = 30
    MAX_WEB_JUNCTION = 5
    WEB_SHOOTING_SPEED = 3
    
    def __init__(self, x, y, size, maxSpeed=0.5, maxSize=15.0, deathSize=6.0, webSupportTheta=random.randint(35, 50)):
        super().__init__(x, y, size, maxSpeed, maxSize, deathSize)
        self.hungerThreshold = 60
        
        self.silk = 100
        self.makeSilkIteration, self.MAKE_SILK_ITERATION = 30, 30
        self.webLength = 0
        self.web = []
        self.webShooter = None
        self.maxFireDist = int((100 // Spider.JUICE_PER_NODE) * Spider.NODE_DISTANCE)
        self.maxAnchorStrandLength = self.maxFireDist * 0.65
        self.goToDest = []
        self.webQueue = None
        
        self.randomDest = None
        
        self.anchorPoints = None        
        self.anchorPointsCenter = None
        self.anchorPointsCleaned = False
        self.navigatedAfterSupports = False
        self.anchorPointsShot = 0
        self.anchorPointNavIterator = 1
        self.webCenter = None
        self.webSupportTheta = webSupportTheta
        self.baseWebComplete = False
        self.timesCentered, self.MAX_TIMES_CENTERED = 0, 2
        
        
        self.hunger = 100
        
    
    def update(self):
        super().update()
        self.makeSilk()
        
    
    def makeSilk(self):
        if self.makeSilkIteration <= 0:
            if self.hunger <= 35 or self.silk > 98:
                return
            
            self.silk += 2
            if self.silk >= 100:
                self.silk = 100
                
            # self.hunger -= 2
            
            self.makeSilkIteration = self.MAKE_SILK_ITERATION
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
            self.walkType = self.walkTypes.HOLD_POSITION
        elif len(self.goToDest) > 0:
            self.walkType = self.walkTypes.GO_TO_POINT
        elif not self.baseWebComplete:
            self.walkType = self.walkTypes.SPIN_WEB
        else:
            if self.randomDest is not None:
                self.walkType = self.walkTypes.RANDOM
            else:
                self.walkType = self.walkTypes.SPIN_WEB
        
    
    #### Walk definitions ####
    def goToPointWalk(self):
        if len(self.goToDest) > 0: 
            if self.calcDistance(self.goToDest[0][0], self.goToDest[0][1]) < 1.5:
                self.goToDest.pop(0)
                return (self.x, self.y)
            return self.goToDest[0]
        
        ## Add more instances such as this as necessary
    
    
    def holdPositionWalk(self):
        return(self.x, self.y)
        
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
        
        # If initial web is not spun, spin it
        if not self.baseWebComplete:
            if self.webCenter is None:
                if self.anchorPoints is None:
                    self.findWebSupports()
                return self.centerOfAnchorPointsWalk()
            else:
                # Check if supports list has been cleaned
                if not self.anchorPointsCleaned:
                    # Only allow points within theta degrees
                    cleanedPoints = []
                    
                    
                    # TODO: find sorting based on theta differences
                    
                    thetas = []
                    for p in self.anchorPoints:
                        thetas.append(math.atan2(p[1] - self.y, p[0] - self.x))
                            
                    
                    rankings = [-1 for _ in range(0, len(thetas))]
                    rank = 0
                    while rank < len(thetas):
                        minTheta = 10
                        minIndex = -1
                        for i in range(0, len(thetas)):
                            # Skip ones that have already been ranked
                            if rankings[i] != -1:
                                continue
                            
                            if thetas[i] < minTheta:
                                minTheta = thetas[i]
                                minIndex = i
                        
                        rankings[minIndex] = rank
                        rank += 1
                        
                    
                    # Create properly ordered list
                    orderedAnchorPoints = []
                    rank = 0
                    while rank < len(thetas):
                        for i in range(0, len(rankings)):
                            if rankings[i] == rank:
                                rank += 1
                                orderedAnchorPoints.append(self.anchorPoints[i])
                                continue
                    
                    self.anchorPoints = orderedAnchorPoints
                    
                    for p in self.anchorPoints:
                        
                        if cleanedPoints == []:
                            cleanedPoints.append(p)
                            continue
                        
                        # Clean self.anchorPoints
                        isCleanPoint = True
                        for cleanP in cleanedPoints:
                            cleanX, cleanY = cleanP[0], cleanP[1]
                            
                            cleanPTheta = math.atan2((cleanY - self.y), (cleanX - self.x))
                            pTheta = math.atan2((p[1] - self.y), (p[0] - self.x))
                            
                            thetaDiff = abs(cleanPTheta - pTheta)
                            thetaDiffDegrees = math.degrees(thetaDiff)
                            
                            if thetaDiffDegrees < self.webSupportTheta:
                                isCleanPoint = False
                        
                        if isCleanPoint:
                            cleanedPoints.append(p)
                    
                    
                    
                    self.anchorPoints = cleanedPoints
                    self.anchorPointsCleaned = True
                    # TODO: Possibly implement reducing webSupportTheta and querying again, probably just leave this trait to natural selection though
                
                        
                # Currently at the center of the web, shoot supports out
                if self.anchorPointsShot < len(self.anchorPoints):
                    fireStatus = self.aimAndFire(self.anchorPoints[self.anchorPointsShot])
                    
                    if fireStatus == 1 or fireStatus == -1:
                        self.anchorPointsShot += 1
                    return(self.x, self.y)
                
                # Supports have been made, now navigate to tip and start stringing process
                if not self.navigatedAfterSupports:
                    self.goToDest.append((self.web[1][len(self.web[1])-1].x, self.web[1][len(self.web[1])-1].y))
                    self.navigatedAfterSupports = True
                    return(self.goToPointWalk())
                
                # TODO: Check if web forms a straight line
                
                
                # Start spinning web connections
                if not self.baseWebComplete:
                    self.workOnWebQueue()
                
                return(self.x, self.y)
        else:
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
                
                shooter = WebShooter(webDestX, webDestY, self)
                self.webShooter = shooter
                Constants.WEB_SHOOTERS.add(shooter)
                
                
            
            return self.randomWalk()
                
            # index = random.randint(0, len(potentialNodes)-1)
    
    
    # webQueue = [startPoint(x, y), queue(list)]
    def workOnWebQueue(self):
        # Check if queue exists, if not generate it
        if self.webQueue is None:
            # Assuming spider was just navigated to support edge
            # Standing at point stored at self.web[1][len(self.web[1])-1]
            startPoint = (self.x, self.y)
            queue = []
            
            
            # Calc node count in shortest strand, this determines row count (ignore center at web[0])
            lowestNodeCount = min(len(strand) for strand in self.web[1:])
            
            for i in range(1, lowestNodeCount+1):
                for j in range(2, len(self.web)):
                    strand = self.web[j]
                    queue.append(strand[len(strand)-i])
                queue.append(self.web[1][len(self.web[1])-i])
            
            self.webQueue = WebQueue(startPoint, queue)
        elif len(self.webQueue.queue) == 0:
            self.baseWebComplete = True
            return
            
        fireStatus = self.aimAndFire((self.webQueue.queue[0].x, self.webQueue.queue[0].y))
        
        if fireStatus == 0:
            return
        elif fireStatus == -1:
            # If the shot is impossible, navigate to the center of the web first
            self.goToDest.append((self.web[0][0].x, self.web[0][0].y))
            
        # Navigate to next anchor point and update queue
        self.goToDest.append((self.webQueue.queue[0].x, self.webQueue.queue[0].y))
        
        # If one cycle is complete, move down one node to start the next cycle
        self.anchorPointNavIterator += 1
        if self.anchorPointNavIterator > len(self.anchorPoints):
            if len(self.webQueue.queue) >= len(self.anchorPoints):
                self.anchorPointNavIterator = 1
                self.goToDest.append((self.webQueue.queue[len(self.anchorPoints)].x, self.webQueue.queue[len(self.anchorPoints)].y))
        
        self.webQueue = WebQueue(self.webQueue.queue[0], self.webQueue.queue[1:])
             
    
        
        
    def centerOfAnchorPointsWalk(self):
        # Return destination location for spider to navigate to
        
        # Continue navigation to destination
        if self.anchorPointsCenter is not None:
            # Reached destination
            distToCenter = self.calcDistance(self.anchorPointsCenter[0], self.anchorPointsCenter[1])
            if distToCenter < 2:
                
                if self.timesCentered >= self.MAX_TIMES_CENTERED:
                    self.webCenter = Node(self.x, self.y)
                    
                    # Add center to the web - just a node, not a strand
                    self.web.append([self.webCenter])
                else:
                    self.anchorPoints = None
                    
                self.anchorPointsCenter = None
                
                return (self.x, self.y)
            
            
            return self.anchorPointsCenter
        
        
        
        # Find location in the middle of given points
        xAvg, yAvg = 0, 0
        for p in self.anchorPoints:
            xAvg += p[0]
            yAvg += p[1]
        
        xAvg, yAvg = xAvg / len(self.anchorPoints), yAvg / len(self.anchorPoints)
        
        # print("Average Loc: {}, {}".format(xAvg, yAvg))
        self.anchorPointsCenter = (xAvg, yAvg)
        return (xAvg, yAvg)
        
    def findWebSupports(self):
        # Find all rocks that could work as a support
        self.anchorPoints = []
        for rock in Constants.ROCKS:
            dist = self.calcDistance(rock[0], rock[1])
            if dist < self.maxAnchorStrandLength:
                rockOffset = (rock[0] + Constants.TILE_WIDTH/2, rock[1] + Constants.TILE_HEIGHT/2)
                self.anchorPoints.append(rockOffset)
        
        self.timesCentered += 1
        
        
        
    # Check if there is enough silk to shoot a target, then shoot
    def aimAndFire(self, point):
        # Return T/F if the shot was successful, -1 for spider skill issue
        
        minFireDist = self.calcDistance(point[0], point[1])
        # Check for impossible shot
        if self.maxFireDist < minFireDist:
            print("IMPOSSIBLE SHOT REQUESTED")
            return -1
        
        currentFireDist = (self.silk / Spider.JUICE_PER_NODE) * Spider.NODE_DISTANCE
        if currentFireDist < minFireDist:
            return 0
        
        # Shot is possible
        shooter = WebShooter(point[0], point[1], self)
        self.webShooter = shooter
        Constants.WEB_SHOOTERS.add(shooter)
        return 1
        
        
    # Add strand to web
    def updateWeb(self, webStrand, distAdded):
        self.web.append(webStrand)
        self.webLength += distAdded
        silkCost = (distAdded / Spider.NODE_DISTANCE) * Spider.JUICE_PER_NODE
        self.silk -= silkCost
        print(f"Shot of distance {distAdded} completed, price={silkCost} silk")
        
    
    # Figure out where to move to and how to do it, then do it
    def move(self):
        destVector = (self.x, self.y)
        
        self.calcBestMovementType()
        self.calcSpeed()
        if self.walkType == self.walkTypes.HOLD_POSITION:
            destVector = self.holdPositionWalk()
        elif self.walkType == self.walkTypes.GO_TO_POINT:
            destVector = self.goToPointWalk()
        elif self.walkType == self.walkTypes.RANDOM:
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
        # Debug support areas
        if Constants.DEVELOPER:
            if self.anchorPointsCleaned:
                for ap in self.anchorPoints:
                    pygame.draw.circle(Constants.SCREEN, (200, 100, 20), (ap[0], ap[1]), 5)
                
        for strand in self.web:
            for i in range(len(strand)-1):
                # Add line between current strand and next strand
                pygame.draw.line(Constants.SCREEN, (0, 0, 0), (strand[i].x, strand[i].y), (strand[i+1].x, strand[i+1].y), 3)
        
    
    def die(self):
        print("todo implement spider die") 