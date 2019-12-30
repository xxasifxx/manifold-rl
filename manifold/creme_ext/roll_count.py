import uuid
import random
import creme
import collections
import creme.stats
from creme import utils


class RollingCount(utils.Window):
    def __init__(self, window_size:int):
        super().__init__(size=window_size)
        self.count = {}
    
    @property
    def window_size(self):
        return self.size
    
    def update(self, x):
        items = self.append(x)
        self.count = dict(collections.Counter(items))
        return self

    def get(self):
        return self.count