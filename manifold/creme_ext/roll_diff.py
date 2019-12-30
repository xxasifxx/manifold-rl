import uuid
import creme
import random
import creme.stats
from creme import utils

class RollingDifference(utils.Window):
    def __init__(self, window_size, ideal:dict):
        super().__init__(size=window_size)
        self.abs_max = window_size
        self.ideal = ideal
        self.required_size = len(self.ideal)
        self.score = 0.0

        if len(self.ideal) == 0:
            raise IndexError("Required keys don't exist")
        
        
    def _score(self, x:dict):
        total = 0
        for key in self.ideal.keys():
            diff = abs(self.ideal[key]-x[key])
            total += self.abs_max - diff
        return (total/self.required_size)
    
    def _movement_score(self):
        if len(self) < 2:
            return 0.0
        
        return 0.0


    def _check_for_required(self, x:dict):
        base = {
            0: x.get(0, self.abs_max),
            1: x.get(1, self.abs_max),
            2: x.get(2, self.abs_max),
        }
        return base
    
    def update(self, x:dict):
        base = self._check_for_required(x)
        main_score = self._score(base)
        movement_score = self._movement_score()
        
        # self.append(score)

        # Now 

        return self
    
    def get(self):
        return self.score