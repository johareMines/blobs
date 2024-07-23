import random
from simulation import Simulation
from constants import Constants
from food import FoodHerbivore
from food import Grapevine

from Organisms.blob import Blob
from Organisms.berrylope import Berrylope
# from particle import Particle
from Organisms.spider import Spider
from Player.player import Player




if __name__ == "__main__":
    simulation = Simulation.get_instance()
    for _ in range(10):
        blob = Blob(random.uniform(0.0, float(Constants.SCREEN_WIDTH)), random.uniform(0.0, float(Constants.SCREEN_HEIGHT)), 10)
        Constants.BLOBS.add(blob)
    
    for _ in range(5):
        berrylope = Berrylope(random.uniform(0.0, float(Constants.SCREEN_WIDTH)), random.uniform(0.0, float(Constants.SCREEN_HEIGHT)), 25)
        Constants.BERRYLOPES.add(berrylope)
    
    # for _ in range(20):
    #     foodHerbivore = FoodHerbivore(random.uniform(0.0, float(Constants.SCREEN_WIDTH)), random.uniform(0.0, float(Constants.SCREEN_HEIGHT)))
    #     Constants.FOODS.add(foodHerbivore)


    for _ in range(4):
        x, y = random.randint(0, Constants.xCELLS - 4), random.randint(0, Constants.yCELLS - 4)
        Constants.GRAPEVINES.add(Grapevine(x,y))
    
    # for _ in range(150):
    #     particle = Particle(random.uniform(0.0, Constants.SCREEN_WIDTH), random.uniform(0.0, Constants.SCREEN_HEIGHT))
    #     Constants.PARTICLES.add(particle)
        
    for _ in range(2):
        Constants.SPIDERS.add(Spider(random.uniform(400, 1200), random.uniform(300, 900), 11))

    

    simulation.run()
