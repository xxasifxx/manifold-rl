import numpy as np
import rolling
# import talib
import random
from typing import List
from crayons import magenta, cyan, green, yellow
from scipy.stats import linregress
from stochastic.continuous import FractionalBrownianMotion
import talib as ta


"""
    -----------------------------------------------------
    ------------ Reward related functions. --------------
    -----------------------------------------------------
"""

def get_regression_by_list(r_list: List[float]):
    """ Get the regression of a given list item. """
    if len(r_list) > 3:
        lin_range = list(range(len(r_list)))
        slope, intercept, r_value, p_value, std_err = linregress(r_list, lin_range)
        return r_value
    return 0


def rolling_regression(num_list: List[float]):
    """ Get the rolling regression """
    regression_list = []
    r_list = rolling.Apply(num_list, 6, operation=list, window_type='variable')
    rl_list = list(r_list)
    for _ in rl_list:
        r = get_regression_by_list(_)
        regression_list.append(r)
    return regression_list


def change_labels(rollreg:list):
    """
        Labels if the direction of the regression is heading upward, sideways or downward. 
    """
    rolling_reg_list = list(rolling.Apply(rollreg, 2, operation=list, window_type='variable'))
    filtered = []
    end_label = []
    for reg in rolling_reg_list:
        if len(reg) == 2:
            if reg[0] != 0 and reg[1] != 0:
                filtered.append(reg)

    for label in filtered:
        x1, x2 = label
        if x1 > 0.85 and x2 > 0.85:
            end_label.append(1)
            continue
        elif x1 < -0.85 and x2 < -0.85:
            end_label.append(-1)
        elif x1 > x2:
            end_label.append(-1)
        else:
            end_label.append(1)
    
    return end_label

"""
    -----------------------------------------------------
    ------------ Action related functions. --------------
    -----------------------------------------------------
"""



def get_action_count(window: List[int]) -> int:
    """ Count all of the actions that are 1 and 2. The number of active actions are important. """
    action_count = 0
    for w in window:
        if w == 1 or w == 2:
            action_count += 1
    return action_count


def rolling_action_count(num_list: List[float], count=10) -> List[int]:
    """ Get the count of actions inside of each window of activity. """
    r_list = rolling.Apply(num_list, count, operation=list, window_type='variable')
    rl_list = list(r_list)
    count_list = []
    for _ in rl_list:
        if len(_) < count:
            continue
        action_count = get_action_count(_)
        count_list.append(action_count)
    return count_list


def ideal_difference(window_action_count:List[float], ideal=3):
    """ Get the difference from the current number and an ideal number. """
    windowed_array = np.array(window_action_count)
    return windowed_array - ideal


def getting_closer_check(ideal_difference_list:list) -> list:
    """ Check if the reward is getting closer to an ideal amount. We do this after we get the ideal difference. """
    i = 0
    ideal_len = len(ideal_difference_list)
    # We assume the idea == 0 based on the last function.
    closer_list = []

    while i <= ideal_len - 2:
        if ideal_difference_list[i] == 0:
            # print(yellow("I'm COMING!!!! ~~~~~~~~D"))
            closer_list.append(0)
        else:
            if ideal_difference_list[i] < 0:
                if ideal_difference_list[i] == ideal_difference_list[i+1]:
                    # print(blue("The only way forward is to start thrusting this cunt"))
                    closer_list.append(-1)
                elif ideal_difference_list[i] < ideal_difference_list[i+1]:
                    # Getting closer to a goal is
                    closer_list.append(1)
                else:
                    # Getting away from a goal is not amazing
                    closer_list.append(-1)
            else:
                if ideal_difference_list[i] == ideal_difference_list[i+1]:
                    # No movement is poor movement
                    closer_list.append(-1)
                elif ideal_difference_list[i] > ideal_difference_list[i+1]:
                    # Moving towards a goal is amazing
                    closer_list.append(1)
                else:
                    # Moving away from a goal is not
                    closer_list.append(-1)
        i+=1

    return closer_list


def get_count(narc:list, index:int) -> int:
    """ 
        We get the number of timesteps we've been at this particular state. [0, 1, 1, 1], with an index of 3 equates to a count of 3. 
        * In other words, we're answering the question: How long have we been in this state?
        * We're answering this question by starting at an index, and counting how many times we see the number at the index we set.    
    """
    
    if len(narc) <= index:
        return 0
    
    count = 1
    while index >= 0:
        # print(narc[index])
        if narc[index] == narc[index-1]:
            count += 1
        else:
            break
        index -= 1
    return count


def get_growth_decay(time, rate, base, _type="growth"):
    if _type == "growth":
        return (base * pow((1+rate), time))
    else:
        return (base * pow((1-rate), time))

def get_label_name(label):
    if label == 1:
        return "growth"
    return "decay"

def get_moving_ranking(rank_list):
    """ Get the x value for the exponential value"""
    smoothy = ta.EMA(np.array(rank_list, dtype='f8'), timeperiod=3)
    reg_roll = rolling_regression(smoothy)
    labels = change_labels(reg_roll)
    latest_label = get_label_name(labels[-1])
    latest_count = get_count(labels, (len(labels)-1))
    return latest_count, latest_label

def imitate_sortino_change():
    foundation_variables = FractionalBrownianMotion(hurst=0.61).sample(10000, zero=False)
    sortino = abs(foundation_variables*random.uniform(1000, 10000))
    smoothy = ta.EMA(sortino, timeperiod=6)
    reg_roll = rolling_regression(smoothy)
    labels = change_labels(reg_roll)
    count = get_count(labels, (len(labels)-1))
    # Once we have the labels, we can assign a score
    return count


def get_rate_by_type(_type):
    if _type == "growth":
        return 0.07
    return 0.14




def get_general_base_by_type_sortino(_type):
    if _type == "growth":
        return 9
    return 4

def get_general_base_by_type_sharpe(_type):
    if _type == "growth":
        return 1.1
    return 1


# -------------------------------------------------- 
# ---------------- Ratio Rewards ------------------- 
# -------------------------------------------------- 


def sortino_rate_reward(rolled):
    x, _type = get_moving_ranking(rolled)
    rate = get_rate_by_type(_type)
    base = get_general_base_by_type_sortino(_type)
    reward = get_growth_decay(time=x, rate=rate, base=base, _type="growth")
    return reward


def sharpe_rate_reward(rolled):
    x, _type = get_moving_ranking(rolled)
    rate = get_rate_by_type(_type)
    base = get_general_base_by_type_sharpe(_type)
    reward = get_growth_decay(time=x, rate=rate, base=base, _type=_type)
    return reward

def action_reward(actions):
    rolled_actions = rolling_action_count(actions)
    rolled_ideal = ideal_difference(rolled_actions)
    ideal_change = getting_closer_check(rolled_ideal)

    change_list = []
    item_list = []
    for i in reversed(range(1, len(ideal_change))):
        back_index = (len(ideal_change)-i)
        current_item = ideal_change[back_index]

        # How long have we been at this step? The number we have here will go into x for the equation 1(1+r)^x or 1(1-r)^x given
        ideal_count = get_count(ideal_change, back_index) 
        base_multiplier = 1
        change_rate = 0.01 # one percent change per step. 

        _type = "growth"
        if current_item == 0:
            base_multiplier = 2.5
            change_rate = 0.03 # one percent change per step. 
        # We're heading Away from a goal
        elif current_item == -1:
            base_multiplier = .84
            change_rate = 0.05 # one percent change per step.
            _type = "decay"
        # We're heading towards a goal
        elif current_item == 1: 
            base_multiplier = 1.2
            change_rate = 0.02 # one percent change per step. 
        item_list.append((ideal_count, current_item))
        change = get_growth_decay(ideal_count, change_rate, base_multiplier, _type)
        change_list.append(change)
    reward = 0
    if len(change_list) > 0:
        reward = change_list[-1]
    return reward

def multi_sortino():
    foundation_variables = FractionalBrownianMotion(hurst=0.61).sample(10000, zero=False)
    sortino = abs(foundation_variables*random.uniform(1000, 10000))
    roll_sortino_list = rolling.Apply(sortino, 30, operation=list, window_type='variable')
    roll_sortino_list = list(roll_sortino_list)
    base = 10
    rate = 0.04
    cum_reward = 0
    for rolled in roll_sortino_list:
        if len(rolled) > 9:
            x, _type = get_moving_ranking(rolled)
            rate = get_rate_by_type(_type)
            base = get_general_base_by_type_sortino(_type)
            reward = get_growth_decay(time=x, rate=rate, base=base, _type=_type)

            print("------------------------------------")
            print(f"Type:\t{yellow(_type, bold=True)}")
            print(f"Rate:\t{magenta(rate, bold=True)}")
            print(f"Base:\t{green(base, bold=True)}")
            print(f"Streak:\t{cyan(x, bold=True)}")
            print(f"Reward:\t{yellow(reward, bold=True)}")
            print("------------------------------------\n\n")
            cum_reward += reward
            print(cum_reward)

            # if x > 15:
            #     time.sleep(1)
if __name__ == "__main__":
    multi_sortino()
    # bp = WienerProcess()
    # s = bp.sample(10000) * 10000
    # actions = [np.random.randint(0, 2) for x in range(1000)]
    # action_score = rolling_action_count(actions)
    # print(action_score)
    # print(rlist)
    # real = talib.ROCP(s, timeperiod=20)
    # print(real)
    # real2 = talib.LINEARREG_SLOPE(s, timeperiod=20)
    
    # n = 20
    # clipped_list = np.array(s[n-1:])
    # r_mean = np.array(list(rolling.Mean(s, n)))
    # r_mean = np.array(r_mean[~np.isnan(r_mean)].tolist())

    # r_std = np.array(list(rolling.Std(s, n)))
    # r_std = np.array(r_std[~np.isnan(r_std)].tolist())
    

    # x_minus = clipped_list - r_mean
    # rolling_normalized = x_minus/r_std
    # print(rolling_normalized)
    # print(r_std)
    
    # print(real[100:150])
    # print(real2[100:150])
