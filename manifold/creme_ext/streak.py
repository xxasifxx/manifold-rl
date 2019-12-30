import creme
import creme.stats
from creme import utils


class HotStreak(creme.stats.base.Univariate):
    def __init__(self, pct_dev=0.1, is_range=False, is_movement=False):
        """ Get how long we've seen a given state. We can use this with an absolute state, a range, or with movement data. """
        self.last_item = None
        self.streak_count = 0
        self.is_range = is_range
        self.pct_change = pct_dev

    def _check_exact_last(self, x):
        if self.last_item != x:
            self.streak_count = 0
            self.last_item = x
        else:
            self.streak_count += 1
    
    def _check_last_range(self, x):
        try:
            if self.last_item is not None:
                float(self.last_item)
                pct_diff = self.last_item * self.pct_change
                # We're checking to see if the number is within two standard deviations of the last
                top_line = self.last_item + (2*pct_diff)
                bottom_line = self.last_item - (2*pct_diff)
                if x <= top_line and x >= bottom_line:
                    self.streak_count += 1
                else:
                    self.streak_count = 0
                    self.last_item = x
            else:
                self.last_item = x
                self.streak_count = 0
        except Exception as er:
            # We're going to assume last item is not a number at this point.
            self._check_exact_last(x)
            

    def update(self, x):
        if self.is_range:
            self._check_last_range(x)
        else:
            self._check_exact_last(x)
        return self

    def get(self):
        return  self.streak_count