from organism import Organism
from monteCarlo import monteCarlo
from constants import Constants
from enum import Enum
import pygame
import random
import math

class Quadtree:
    def __init__(self, x, y, width, height, max_particles=4, depth=0, max_depth=10):
        self.bounds = pygame.Rect(x, y, width, height)
        self.max_particles = max_particles
        self.particles = []
        self.divided = False
        self.depth = depth
        self.max_depth = max_depth

    def subdivide(self):
        x, y, w, h = self.bounds
        hw, hh = w // 2, h // 2

        self.nw = Quadtree(x, y, hw, hh, self.max_particles, self.depth + 1, self.max_depth)
        self.ne = Quadtree(x + hw, y, hw, hh, self.max_particles, self.depth + 1, self.max_depth)
        self.sw = Quadtree(x, y + hh, hw, hh, self.max_particles, self.depth + 1, self.max_depth)
        self.se = Quadtree(x + hw, y + hh, hw, hh, self.max_particles, self.depth + 1, self.max_depth)

        self.divided = True

    def insert(self, particle):
        scaledX = int(particle.x // 5)
        scaledY = int(particle.y // 5)
        if not self.bounds.collidepoint(particle.x, particle.y):
            return False

        if len(self.particles) < self.max_particles or self.depth >= self.max_depth:
            self.particles.append(particle)
            return True
        else:
            if not self.divided:
                self.subdivide()

            if self.nw.insert(particle) or self.ne.insert(particle) or self.sw.insert(particle) or self.se.insert(particle):
                return True

    def clear(self):
        self.particles = []
        self.divided = False
        self.northwest = None
        self.northeast = None
        self.southwest = None
        self.southeast = None
        
    def query(self, range, found):
        if not self.bounds.colliderect(range):
            return found

        for p in self.particles:
            scaledX = int(p.x // 5)
            scaledY = int(p.y // 5)
            if range.collidepoint(p.x, p.y):
                found.append(p)

        if self.divided:
            self.nw.query(range, found)
            self.ne.query(range, found)
            self.sw.query(range, found)
            self.se.query(range, found)

        return found
    
    def update(self, particle):
        scaledX = int(particle.x // 5)
        scaledY = int(particle.y // 5)
        
        # If the particle is still within the current quadtree bounds, do nothing
        if self.bounds.collidepoint(particle.x, particle.y):
            return

        # Otherwise, remove the particle from this quadtree
        if particle in self.particles:
            self.particles.remove(particle)

        # Try to insert the particle in one of the subdivided quadrants
        if self.divided:
            if self.nw.insert(particle) or self.ne.insert(particle) or self.sw.insert(particle) or self.se.insert(particle):
                return
        else:
            # If the particle cannot be inserted into a child, insert it into this quadtree
            self.insert(particle)
    

class Particle(Organism):
    __particleAttractions = None
    def __init__(self, x, y, maxSpeed=0.6):
        super().__init__(x, y, 2, maxSpeed, 2, deathSize=1)
        self.maxInfluenceDist = 300
        self.minInfluenceDist = 5
        self.setType()
        self.getParticleAttractions()

    def setType(self):
        pType = random.randint(0, len(self.particleTypes) - 1)
        self.particleType = self.particleTypeByIndex(pType)

    @staticmethod
    def getParticleAttractions():
        # Static method to get singleton instance
        if Particle.__particleAttractions is None:
            Particle.__particleAttractions = {}
            
            # Initialize to list of 0's
            for p in Particle.particleTypes:
                Particle.__particleAttractions[p.name] = [0] * len(Particle.particleTypes)
            
            typesList = list(Particle.particleTypes)
            for i, p in enumerate(typesList):
                for j in range (i, len(Particle.particleTypes)):
                    if i == j:
                        # Diagonals should be the same (similar particles should act the same)
                        Particle.__particleAttractions[p.name][j] = random.uniform(-0.4, 0.4)
                    else:
                        value = random.uniform(-0.4, 0.4)
                        Particle.__particleAttractions[p.name][j] = value
                        Particle.__particleAttractions[list(Particle.particleTypes)[j].name][i] = value
                        
            print(Particle.__particleAttractions)
        
        return Particle.__particleAttractions
        
            

    def calcDest(self):
        velocities = []
        finalVelX, finalVelY = 0, 0

        range_query = pygame.Rect(self.x - self.maxInfluenceDist, self.y - self.maxInfluenceDist, self.maxInfluenceDist * 2, self.maxInfluenceDist * 2)
        neighbors = Constants.QUADTREE.query(range_query, [])

        for p in neighbors:
            if p is self:
                continue

            dx = p.x - self.x
            dy = p.y - self.y

            dist = math.sqrt(dx ** 2 + dy ** 2)

            if dist > self.maxInfluenceDist:
                continue

            influenceIndex = self.particleTypeByEnum(p.particleType)
            influenceFactor = Particle.getParticleAttractions()[self.particleType.name][influenceIndex]

            # Make them repel if too close
            if influenceFactor > 0:
                if dist < self.minInfluenceDist:
                    impact = self.minInfluenceDist - dist
                    impact *= 0.2
                    influenceFactor -= impact
                
            influence = influenceFactor * math.exp(-dist / self.maxInfluenceDist)

            dirX = dx / dist if dist != 0 else 0
            dirY = dy / dist if dist != 0 else 0

            velX = influence * dirX
            velY = influence * dirY

            velocities.append((velX, velY))

        for v in velocities:
            finalVelX += v[0]
            finalVelY += v[1]

        destX, destY = self.x + finalVelX, self.y + finalVelY
        return (destX, destY)

    def calcSpeed(self, dist):
        speedGoal = dist
        
        if speedGoal > self.maxSpeed:
            speedGoal = self.maxSpeed
        if speedGoal < 0:
            speedGoal = 0
            
        
        self.speed = speedGoal
        
    def move(self):
        destVector = self.calcDest()
        self.destX, self.destY = destVector

        self.calcBoundaries()
        dist = self.calcDistance(self.destX, self.destY)
        self.calcSpeed(dist)

        if dist <= self.speed:
            self.x, self.y = self.destX, self.destY
        else:
            dx = self.destX - self.x
            dy = self.destY - self.y
            velX = dx / dist * self.speed
            velY = dy / dist * self.speed
            self.x += velX
            self.y += velY

    def calcHungerRate(self):
        return 0

    def checkBirth(self):
        pass

    def draw(self):
        pygame.draw.circle(Constants.SCREEN, self.particleType.value, (self.x, self.y), self.size)

    def particleTypeByIndex(self, index):
        switch = {
            0: self.particleTypes.PINK,
            1: self.particleTypes.TEAL,
            2: self.particleTypes.GREY,
            3: self.particleTypes.MAIZE,
            4: self.particleTypes.INDIGO,
            5: self.particleTypes.ORANGE
        }
        return switch.get(index)

    def particleTypeByEnum(self, enum):
        switch = {
            self.particleTypes.PINK: 0,
            self.particleTypes.TEAL: 1,
            self.particleTypes.GREY: 2,
            self.particleTypes.MAIZE: 3,
            self.particleTypes.INDIGO: 4,
            self.particleTypes.ORANGE: 5,
        }
        return switch.get(enum)

    class particleTypes(Enum):
        PINK = (255, 130, 169)
        TEAL = (44, 175, 201)
        GREY = (156, 174, 169)
        MAIZE = (244, 224, 77)
        INDIGO = (84, 13, 110)
        ORANGE = (224, 92, 21)
