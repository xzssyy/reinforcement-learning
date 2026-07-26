from algorithm import epsilon_greedy
import numpy as np
import matplotlib.pyplot as plt
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


def bandit_test(episods, epsilon):
    bandit_10_armed = MultiArmedBandit(10)
    best_arm = bandit_10_armed.best_arm

    estimated_value = {i: 0 for i in range(10)}

    counter = np.zeros(10)

    rewards = []
    choose_best = []

    for episode in range(episods):
        arm = epsilon_greedy(epsilon, estimated_value)
        value = bandit_10_armed.pull(arm)
        counter[arm] += 1

        estimated_value[arm] += (value - estimated_value[arm]) / counter[arm]

        rewards.append(value)
        if arm == best_arm:
            choose_best.append(1)
        else:
            choose_best.append(0)

    return np.array(rewards), np.array(choose_best)

def sample_average(samples, epsilon):
    ave_reward = np.zeros(samples)
    optimal_action = np.zeros(samples)

    for i in tqdm(range(2000)):
        rewards, choose_best = bandit_test(samples, epsilon)
        ave_reward = ave_reward + rewards
        optimal_action = optimal_action + choose_best

    ave_reward /= 2000
    optimal_action /= 2000
    
    return ave_reward, optimal_action
    

greedy_rewards, greedy_optimal_action = sample_average(1000, 0)
eps01_rewards, eps01_optimal_action = sample_average(1000, 0.1)
eps001_rewards, eps001_optimal_action = sample_average(1000, 0.01)


fig, axes = plt.subplots(
    2, 1,
    figsize=(8, 8)
)


# 第一幅：Average Reward
axes[0].plot(
    greedy_rewards,
    label="epsilon=0"
)

axes[0].plot(
    eps01_rewards,
    label="epsilon=0.1"
)

axes[0].plot(
    eps001_rewards,
    label="epsilon=0.01"
)

axes[0].set_ylabel("Average Reward")
axes[0].legend()


# 第二幅：Optimal Action
axes[1].plot(
    greedy_optimal_action,
    label="epsilon=0"
)

axes[1].plot(
    eps01_optimal_action,
    label="epsilon=0.1"
)

axes[1].plot(
    eps001_optimal_action,
    label="epsilon=0.01"
)

axes[1].set_xlabel("Steps")
axes[1].set_ylabel("% Optimal Action")
axes[1].legend()


plt.tight_layout()
plt.savefig("./bandit/10-armed testbed.png")
