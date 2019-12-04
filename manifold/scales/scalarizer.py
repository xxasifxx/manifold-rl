from typing import List, Dict
from abc import ABC

class Scalarizer(ABC):
    """ This determines how we're going to scalarize the different objectives we setup"""
    
    def __init__(self) -> None:
        self._history = []


    def ordering_rule(self, vector_values):
        raise NotImplementedError


    def transform(self, vector_values: List[Dict[str, float]]) -> float:
        """ Return the single objective according to how we define the scalar should work"""
        raise NotImplementedError

    def reset(self):
        self._history = []