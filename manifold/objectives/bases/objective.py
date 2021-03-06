from typing import List, Dict
from abc import ABC
from manifold.objectives.bases import Ranking, Rewarding

class Objective(ABC):
    """ This determines how we're going to scalarize the different objectives we setup"""
    def __init__(self, name, reward_rule:Rewarding, ranking_rule:Ranking) -> None:
        """ Set the name, and ranking rule we want to apply to the objective"""
        self._history = []
        self.name = name
        self.ranking = ranking_rule
        self.reward_rule = reward_rule

    @property
    def history(self):
        return self.reward_rule.history
    
    @history.setter
    def history(self, hist:list):
        self.reward_rule.history = hist
    
    @property
    def hist_ten(self):
        return self.history[-10:]

    @property
    def hist_twenty(self):
        return self.history[-20:]


    # def transform(self):
    #     return {
    #         "reward": self.transform_reward(),
    #         "ranking": self.transform_rank_score()
    #     }

    def transform_reward(self):
        """ Takes the full history and creates a single number as well as relative rank"""
        raise NotImplementedError
    
    def transform_rank_score(self):
        """ Get the ranking of the objective and it's overall ranking. The ranking score will be passed onto the scalarizer to find the absolute weight."""
        raise NotImplementedError
    
    def push(self, state, ambient=None):
        """ Push the relavent state variables to get the appropiate information"""
        # self.history.append(state)
        self.reward_rule.history.append(state)
        if ambient is not None:
            self.ranking.push(ambient)

    def reset(self):
        """ Resets all of the key variables tied immediately to """
        self.reward_rule.history = []