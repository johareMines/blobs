import random
from simulation import Simulation
from constants import Constants
from food import FoodHerbivore
from food import Grapevine

from blob import Blob
from berrylope import Berrylope




if __name__ == "__main__":
    simulation = Simulation.get_instance()
    for _ in range(2000):
        blob = Blob(random.uniform(0.0, float(Constants.SCREEN_WIDTH)), random.uniform(0.0, float(Constants.SCREEN_HEIGHT)), 10)
        Constants.BLOBS.add(blob)
    
    for _ in range(3):
        berrylope = Berrylope(random.uniform(0.0, float(Constants.SCREEN_WIDTH)), random.uniform(0.0, float(Constants.SCREEN_HEIGHT)), 25)
        Constants.BERRYLOPES.add(berrylope)
    
    # for _ in range(20):
    #     foodHerbivore = FoodHerbivore(random.uniform(0.0, float(Constants.SCREEN_WIDTH)), random.uniform(0.0, float(Constants.SCREEN_HEIGHT)))
    #     Constants.FOODS.add(foodHerbivore)


    for _ in range(3):
        x, y = random.randint(0, Constants.xCELLS - 4), random.randint(0, Constants.yCELLS - 4)
        Constants.GRAPEVINES.add(Grapevine(x,y))
        

    simulation.run()
