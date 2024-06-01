

class Constants:
    DEVELOPER = True
    BLACK = (0, 0, 0)
    GREEN = (30, 150, 90)
    SCREEN_WIDTH = None
    SCREEN_HEIGHT = None
    TILE_WIDTH = None
    TILE_HEIGHT = None
    xCELLS = None
    yCELLS = None

    SCREEN = None
    BACKGROUND = None

    ORGANISMS = []
    FOODS = set({})
    GRAPEVINE_ADDED = ((0, 0), False)
    GRAPEVINES = set({})
    GRAPES = set({})


    WATER_HEIGHT = -7
    ROCK_HEIGHT = -101
    SNOW_HEIGHT = 7

    def calcCoords( x, y):
        x *= Constants.TILE_WIDTH
        y *= Constants.TILE_HEIGHT
        return (x, y)
    
    
