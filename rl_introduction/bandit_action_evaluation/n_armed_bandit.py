from rl_introduction.bandit_action_evaluation.action_selection import epsilon_greedy
import numpy as np
from tqdm import tqdm


class MultiArmedBandit:

    def __init__(self, arms):
        self.arms = arms
        self.action_values = np.random.normal(0, 1, arms)
        self.max_value = np.max(self.action_values)
        self.best_arm = np.argmax(self.action_values)

    def pull(self, arm):
        error = np.random.normal(0, 1)
        return self.action_values[arm] + error


