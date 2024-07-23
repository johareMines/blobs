from exceptions import SingletonMultipleInstantiationException
import numpy as np
from constants import Constants
import pygame

class Player:
    __instance = None
    def __init__(self):
        if Player.__instance is not None:
            raise SingletonMultipleInstantiationException
        else:
            self.health = 100
            self.maxSpeed = 0.7
            self.size = 22
            self.acceleration = 0.05
            self.playerInputs = {
                "up": 0,
                "down": 0,
                "left": 0,
                "right": 0
            }
            self.pos = np.array([Constants.SCREEN_WIDTH // 2, Constants.SCREEN_HEIGHT // 2], dtype=np.float32)

            self.vel = np.array([0, 0], dtype=np.float32)

    def update(self):
        instance = Player.getInstance()
        # print(f"Instance is {Player.get_string()}")

        self.calcVel()
        self.move()
        self.draw(instance)
    
    def calcVel(self):
        newVel = 0.0
        # if self.vel[1] > -self.maxSpeed:
        #     self.vel[1] = max(self.vel[1] - self.acceleration, -self.maxSpeed)
        if self.playerInputs["up"]:
            if self.vel[1] > -self.maxSpeed:
                self.vel[1] = max(self.vel[1] - self.acceleration, -self.maxSpeed)
        else:
            if self.vel[1] < 0.0:
                self.vel[1] = min(self.vel[1] + self.acceleration, 0.0)

        if self.playerInputs["down"]:
            if self.vel[1] < self.maxSpeed:
                self.vel[1] = min(self.vel[1] + self.acceleration, self.maxSpeed)
        else:
            if self.vel[1] > 0.0:
                self.vel[1] = max(self.vel[1] - self.acceleration, 0.0)
        


        if self.playerInputs["left"]:
            if self.vel[0] > -self.maxSpeed:
                self.vel[0] = max(self.vel[0] - self.acceleration, -self.maxSpeed)
        else:
            if self.vel[0] < 0.0:
                self.vel[0] = min(self.vel[0] + self.acceleration, 0.0)

        if self.playerInputs["right"]:
            if self.vel[0] < self.maxSpeed:
                self.vel[0] = min(self.vel[0] + self.acceleration, self.maxSpeed)
        else:
            if self.vel[0] > 0.0:
                self.vel[0] = max(self.vel[0] - self.acceleration, 0.0)



    

    def move(self):
        self.pos += self.vel
        self.checkBoundaries()

    def checkBoundaries(self):
        if self.pos[0] > Constants.SCREEN_WIDTH:
            self.pos[0] = Constants.SCREEN_WIDTH
        elif self.pos[0] < 0:
            self.pos[0] = 0

        if self.pos[1] > Constants.SCREEN_HEIGHT:
            self.pos[1] = Constants.SCREEN_HEIGHT
        elif self.pos[1] < 0:
            self.pos[1] = 0

    def draw(self, instance):
        pygame.draw.rect(Constants.SCREEN, (220, 25, 10), (int(instance.pos[0] - (instance.size // 2)), int(instance.pos[1] - (instance.size // 2)), instance.size, instance.size))


    @staticmethod
    def getInstance():
        if Player.__instance is None:
            Player.__instance = Player()
        return Player.__instance
    

    @staticmethod
    def get_string():
        instance = Player.__instance
        return f"PLAYER: Health {instance.health}, maxSpeed {instance.maxSpeed}, size {instance.size}, pos {instance.pos}"