import random
from simulation import Simulation
from constants import Constants
from food import FoodHerbivore

from blob import Blob




if __name__ == "__main__":
    simulation = Simulation()
    for _ in range(30):
        blob = Blob(random.uniform(0.0, float(Constants.SCREEN_WIDTH)), random.uniform(0.0, float(Constants.SCREEN_HEIGHT)), 10, (255, 0, 0))
        Constants.ORGANISMS.append(blob)
    
    for _ in range(20):
        foodHerbivore = FoodHerbivore(random.uniform(0.0, float(Constants.SCREEN_WIDTH)), random.uniform(0.0, float(Constants.SCREEN_HEIGHT)))
        Constants.FOODS.add(foodHerbivore)

    simulation.run()
