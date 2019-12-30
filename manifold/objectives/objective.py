from typing import List, Dict
from abc import ABC
from manifold.objectives import Ranking, Rewarding

class Objective(ABC):
    """ This determines how we're going to scalarize the different objectives we setup"""
    def __init__(self, name, reward_rule:Rewarding, ranking_rule:Ranking) -> None:
        """ Set the name, and ranking rule we want to apply to the objective"""
        self._history = []
        self.name = name
        self.ranking = ranking_rule
        self.reward_rule = reward_rule

    def transform_reward(self):
        """ Takes the full history and creates a single number as well as relative rank"""
        raise NotImplementedError
    
    def transform_rank_score(self):
        """ Get the ranking of the """
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