class SingletonMultipleInstantiationException(Exception):
    def __init__(self):
        message = "Singleton can't be instantiated multiple times."
        super().__init__(message)