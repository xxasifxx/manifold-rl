from manifold.objectives import Objective
from manifold.objectives import Ranking
from stochastic.continuous import FractionalBrownianMotion
from manifold import Manifold
# from manifold_test.base_types.valuation import ValueDict

def test_get_all_information():
    """ Checks to see if we've recieved all observations through the main pipeline"""
    # Create an objective with a name

    objective_one = Objective("sample_reward", {}, Ranking("sample_reward"))


    motion = FractionalBrownianMotion()
    motion_two = FractionalBrownianMotion()
    motion_sample = motion.sample(1000) + 1.2
    motion_sample_two = motion_two.sample(1000) + 1.1


    motion_sample = motion_sample * 1000
    motion_sample_two = motion_sample_two * 1000
    manifold = Manifold(objectives=[objective_one])
    
    for i in range(len(motion_sample)):
        value_dict = [dict(name="sample_reward", value=motion_sample[i], ambient=motion_sample_two[i])]
        reward = manifold.step(value_dict)
        print(reward)
    # print(manifold)
    # print(motion_sample)


if __name__ == "__main__":
    test_get_all_information()