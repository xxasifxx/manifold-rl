from typing import List, Dict
from abc import ABC
from manifold.objectives import Ranking


class Objective(ABC):
    """ This determines how we're going to scalarize the different objectives we setup"""
    def __init__(self, name, ranking_rule:Ranking) -> None:
        """ Set the name, and ranking rule we want to apply to the objective"""
        self._history = []
        self.ranking = ranking_rule
        self.name = name

    def transform(self):
        """ Takes the full history and creates a single number as well as relative rank"""
        raise NotImplementedError
    
    def push(self, main, ambient=None):
        """ Push the relavent state variables to get the appropiate information"""
        self.push_main_state(main)
        if ambient is not None:
            self.ranking.push(ambient)

    def push_main_state(self, state):
        self._history.append(state)

    def reset(self):
        """ Resets all of the key variables tied immediately to """
        self._history = []