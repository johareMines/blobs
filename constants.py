

class Constants:
    DEVELOPER = True
    MONITOR_INTERVAL = 10
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
    
    QUADTREE = None

    # ORGANISMS = []
    BORN_BLOBS = []
    DYING_BLOBS = []
    BLOBS = set({})
    
    BORN_BERRYLOPES = []
    DYING_BERRYLOPES = []
    MATING_BERRYLOPES = []
    BERRYLOPES = set({})
    
    PARTICLES = set({})
    
    FOODS = set({})
    GRAPEVINE_ADDED = ((0, 0), False)
    GRAPEVINES = set({})
    GRAPES = set({})


    WATER_HEIGHT = -12
    ROCK_HEIGHT = -101
    SNOW_HEIGHT = 12

    def calcCoords(x, y):
        x *= Constants.TILE_WIDTH
        y *= Constants.TILE_HEIGHT
        return (x, y)
    
    
