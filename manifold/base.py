from manifold.objectives import Objective
from manifold.scales import Scalarizer


class Manifold(object):
    """ Use some kind of pattern here to manage all of the objectives"""
    def __init__(self) -> None:
        pass

    def add(self, objective:Objective):
        """ Add an objective we're going to watch throughout a simulation"""
        pass
    
    def scalar(self, _scalar:Scalarizer):
        """ Set the scalarization method we want to use"""
        pass

    def transform(self):
        """ Get the current reward given the objective"""
        return 1