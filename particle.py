from organism import Organism
from monteCarlo import monteCarlo
from constants import Constants
from enum import Enum
import pygame
import random
import math
import collections

class Quadtree:
    def __init__(self, x, y, width, height, max_particles=3, depth=0, max_depth=15):
        self.bounds = pygame.Rect(x, y, width, height)
        self.max_particles = max_particles
        self.particles = []
        self.divided = False
        self.depth = depth
        self.max_depth = max_depth

    def subdivide(self):
        x, y, w, h = self.bounds
        hw, hh = int(w // 2), int(h // 2)

        self.nw = Quadtree(x, y, hw, hh, self.max_particles, self.depth + 1, self.max_depth)
        self.ne = Quadtree(x + hw, y, hw, hh, self.max_particles, self.depth + 1, self.max_depth)
        self.sw = Quadtree(x, y + hh, hw, hh, self.max_particles, self.depth + 1, self.max_depth)
        self.se = Quadtree(x + hw, y + hh, hw, hh, self.max_particles, self.depth + 1, self.max_depth)

        self.divided = True

    def insert(self, particle):
        if not self.bounds.collidepoint(particle.x, particle.y):
            return False

        if len(self.particles) < self.max_particles or self.depth >= self.max_depth:
            self.particles.append(particle)
            # if self.depth >= self.max_depth:
            #     print(self.depth)
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
            if range.collidepoint(p.x, p.y):
                found.append(p)

        if self.divided:
            self.nw.query(range, found)
            self.ne.query(range, found)
            self.sw.query(range, found)
            self.se.query(range, found)

        return found
    
    def update(self, particle):
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
        self.maxInfluenceDist = 120
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
                        Particle.__particleAttractions[p.name][j] = random.uniform(-0.4, 0.4)
                        Particle.__particleAttractions[list(Particle.particleTypes)[j].name][i] = random.uniform(-0.4, 0.4)
                        
            print(Particle.__particleAttractions)
        
        return Particle.__particleAttractions
        
        
    @staticmethod
    def batchQuery(particles, maxInfluenceDist):
        supercell_size = maxInfluenceDist
        supercell_map = collections.defaultdict(list)
        results = {}

        for p in particles:
            supercell_x = int(p.x // supercell_size)
            supercell_y = int(p.y // supercell_size)
            supercell_map[(supercell_x, supercell_y)].append(p)
            results[p] = []

        for (scx, scy), particles_in_supercell in supercell_map.items():
            range_query = pygame.Rect(
                scx * supercell_size - maxInfluenceDist,
                scy * supercell_size - maxInfluenceDist,
                supercell_size + maxInfluenceDist * 2,
                supercell_size + maxInfluenceDist * 2
            )
            found = Constants.QUADTREE.query(range_query, [])

            for p in particles_in_supercell:
                results[p] = [f for f in found if f != p]

        return results

    @staticmethod
    def batchCalcDest(particles):
        if not particles:
            return  # No particles to process

        # Grab a random particle to determine maxInfluenceDist
        maxInfluenceDist = next(iter(particles)).maxInfluenceDist  # Assuming all particles have the same maxInfluenceDist
        influenceTable = Particle.getParticleAttractions()
        
        # Batch query the quadtree for all particles using supercells
        neighbors_dict = Particle.batchQuery(particles, maxInfluenceDist)
        
        # Calculate destinations for all particles
        for particle in particles:
            finalVelX, finalVelY = 0, 0
            maxInfluenceDistSquared = maxInfluenceDist ** 2
            
            neighbors = neighbors_dict[particle]
            for p in neighbors:
                dx = p.x - particle.x
                dy = p.y - particle.y
                distSquared = dx ** 2 + dy ** 2
                
                if distSquared > maxInfluenceDistSquared:
                    continue
                
                dist = math.sqrt(distSquared)
                influenceIndex = particle.particleTypeByEnum(p.particleType)
                influence = influenceTable[particle.particleType.name][influenceIndex]
                
                if influence > 0 and dist < particle.minInfluenceDist:
                    impact = particle.minInfluenceDist - dist
                    impact *= 0.4
                    influence -= impact
                
                influence *= math.exp(-dist / maxInfluenceDist)
                
                if dist != 0:
                    dirX = dx / dist
                    dirY = dy / dist
                    
                    finalVelX += influence * dirX
                    finalVelY += influence * dirY
            
            particle.destX = particle.x + finalVelX
            particle.destY = particle.y + finalVelY
    

    def calcSpeed(self, dist):
        speedGoal = min(dist, self.maxSpeed)
        self.speed = max(speedGoal, 0)
        
    def calcBoundaries(self):
        retX, retY = self.destX, self.destY
        if self.destX <= 0:
            retX = 0
        elif self.destX >= Constants.SCREEN_WIDTH:
            retX = Constants.SCREEN_WIDTH
        
        if self.destY <= 0:
            retY = 0
        elif self.destY >= Constants.SCREEN_HEIGHT:
            retY = Constants.SCREEN_HEIGHT
        
        self.destX = retX
        self.destY = retY
        
    def move(self):
        # destVector = self.calcDest()
        # self.destX, self.destY = destVector

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
