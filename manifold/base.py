from typing import List, Dict, Any
from manifold.objectives import Objective
# from manifold_test.base_types.valuation import ValueDict, IndividualWeight, IndividualRewards



class Manifold(object):
    """ Use some kind of pattern here to manage all of the objectives"""
    def __init__(self, objectives:List[Objective]=[]) -> None:
        self._scalar = None
        self._objectives = []
        self._objective_dict = {}
        if len(objectives) > 0:
            for objective in objectives:
                self.add(objective)

    def add(self, objective:Objective):
        """ Add an objective we're going to watch throughout a simulation"""
        objective_name = objective.name
        self._objective_dict[objective_name] = objective
        self._objectives.append(
            objective
        )
    
    @property
    def scalar(self):
        return self._scalar

    @scalar.setter
    def scalar(self, _scalar):
        """ Set the scalarization method we want to use. This should be noted as something we use to get the weights"""
        self._scalar = _scalar
    
    @property
    def weights(self) -> Dict[str, float]:
        # Get all of the `IndividualWeight` in a list and flatten them into a single key/value dict.
        # The weights are found using the scalar
        return {}


    @property
    def rewards(self) -> Dict[str, float]:
        general_rewards = self._get_individual_rewards()
        return {}

    

    def _push_values(self, monitored:List[Dict[str, Any]]):


        for monitor in monitored:
            monitored_name = monitor['name']
            current_objective = self._objective_dict.get(monitored_name, None)
            current_value = monitor['value']
            current_ambient = monitor['ambient']
            

            if current_objective is not None:
                current_objective.push(state=current_value, ambient=current_ambient)
                self._objective_dict[monitored_name] = current_objective


    def _get_individual_rewards(self) -> Dict[str, Any]:
        """ Get the list rewards """
        rewards_dict = {}

        objective_keys = list(self._objective_dict.keys())
        for ok in objective_keys:
            objective = self._objective_dict[ok]
            name = objective.name
            reward = objective.transform_reward()
            rewards_dict[name] = reward
        return rewards_dict
    

    def _get_individual_weights(self) -> Dict[str, Any]:
        """ Get the current score and get the percentage of the total score to derive the weight. """
        return {}

    def step(self, monitored:List[Dict[str, Any]]=[]):
        """ Go through each monitored value and get the reward for each value. """
        if len(monitored) == 0:
            return 0.0

        self._push_values(monitored)
        

        weights = self.weights
        rewards = self.rewards

        if len(weights.keys()) == 0 or len(rewards.keys()) == 0:
            return 0
        
        total_reward = 0.0
        for weight_name, weight_value in weights.items():
            reward_value = rewards.get(weight_name, 0.0)
            current_total = reward_value * weight_value
            total += current_total
        return total_reward


    def reset(self):
        """ Reset all of the lists"""
        pass