import uuid
import time
import random
import creme
import collections
import creme.stats
from creme import utils
from manifold.creme_ext import CCounter

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
    

if __name__ == "__main__":
    
    roll_count = RollingCount(10)
    ccount = CCounter(counter_list=[0, 3])
    
    while True:
        get_number = random.randint(0, 2)
        roll_count.update(get_number)
        get_count = roll_count.get()
        ccount.update(get_count)
        print(ccount.get())
        time.sleep(0.001)