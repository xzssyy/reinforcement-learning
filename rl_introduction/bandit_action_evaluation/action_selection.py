import numpy as np
import random


def epsilon_greedy(epsilon, action_values: dict):

    # explore
    if np.random.random() < epsilon:
        return random.choice(list(action_values.keys()))

    # exploit
    else:
        max_value = max(action_values.values())
        best_actions = [a for a, q in action_values.items() if q == max_value]
        return random.choice(best_actions)

