from abc import ABC

class Rewarding(ABC):
    """ This determines how we're going to scalarize the different objectives we setup"""
    def __init__(self, name, minimum=0, maximum=1) -> None:
        """ Set the name, and ranking rule we want to apply to the objective"""
        self._history = []
        self.min = minimum
        self.max = maximum
    
    @property
    def history(self):
        return self._history

    @property
    def hist_ten(self):
        return self.history[-10:]

    @property
    def hist_twenty(self):
        return self.history[-20:]

    def processing_rule(self):
        raise NotImplementedError

    def transform(self):
        """ Takes the full history and creates a single number as well as relative rank"""
        raise NotImplementedError
    
    def push(self, state):
        self._history.append(state)

    def reset(self):
        """ Resets all of the key variables tied immediately to """
        self._history = []