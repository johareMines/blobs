from abc import ABC, abstractmethod

class Drawable:
    @abstractmethod
    def draw(self):
        raise NotImplementedError("Class must implement draw()")
    
    # Provide human readable class name
    def __repr__(self):
        return f"{self.__class__.__name__}"