
def sample_average(episods, epsilon):
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

def bandit_test(steps, epsilon, stepsize_function):
    ave_reward = np.zeros(steps)
    optimal_action = np.zeros(steps)

    for i in tqdm(range(2000)):
        rewards, choose_best = stepsize_function(steps, epsilon)
        ave_reward = ave_reward + rewards
        optimal_action = optimal_action + choose_best

    ave_reward /= 2000
    optimal_action /= 2000
    
    return ave_reward, optimal_action
    


steps = 20000
greedy_rewards, greedy_optimal_action = bandit_test(steps, 0, sample_average)
eps01_rewards, eps01_optimal_action = bandit_test(steps, 0.1, sample_average)
eps001_rewards, eps001_optimal_action = (steps, 0.01, sample_average)



