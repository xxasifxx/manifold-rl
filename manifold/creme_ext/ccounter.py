import creme
import creme.stats
from creme import utils


class CCounter(creme.stats.base.Univariate):
    def __init__(self, counter_list=[1, 2]):
        """ Given a counter transformation, get a total for all of the variables you're looking for """
        self.counter_list = counter_list
        self.count = 0

    def update(self, x):
        try:
            total = 0
            for item in self.counter_list:
                current_count = x.get(item, 0)
                total += current_count
            self.count = total
        except Exception as e:
            self.count = 0
        return self

    def get(self):
        return  self.count