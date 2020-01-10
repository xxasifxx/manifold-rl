from manifold.objectives import Objective, Rewarding, Ranking


class CountLimiter(Objective):
    """Get the required count over a rolling window. Requires both a transformer and stuffs internally."""
    def __init__(self, name, reward_rule:'Rewarding', ranking_rule:'Ranking') -> None:
        super().__init__(name, reward_rule, ranking_rule)