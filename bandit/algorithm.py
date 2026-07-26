import numpy as np
import random


def epsilon_greedy(epsilon, action_values: dict):

    # explore
    if np.random.random() < epsilon:
        # print("explore")
        return random.choice(list(action_values.keys()))

    # exploit
    else:
        max_value = max(action_values.values())
        best_actions = [a for a, q in action_values.items() if q == max_value]
        # print("exploit")
        return random.choice(best_actions)



if __name__ == "__main__":
    epsilon = 0.3
    actions = list(range(4))
    action_values = {0 : 1, 
                     1 : 2,
                     2 : 2,
                     3 : 1}
    print(epsilon_greedy(epsilon, action_values))
    