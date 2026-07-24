# TicTacToe Reinforcement Learning Project Notes

## 项目简介

通过实现井字棋强化学习智能体，学习强化学习中的核心概念：

- Markov Decision Process (MDP)
- State / Action 定义
- Value Function
- Monte Carlo Prediction
- Epsilon-Greedy Policy
- Model-based / Model-free RL
- Exploration 问题
- Policy 与 Value 的关系

该项目参考 Sutton《Reinforcement Learning: An Introduction》中井字棋案例。

---

# 1. 项目结构

```
tictactoe/

├── env.py
│   └── TicTacToe环境
├── opponent.py
│   └── RuleOpponent / RandomOpponent
├── agent.py
│   └── RLAgent
├── state_generator.py
│   └── 状态空间生成
├── train.py
│   └── Monte Carlo训练
└── evaluate.py
    └── agent评估
```

---

# 2. 环境设计

强化学习首先需要定义环境。

## State

棋盘状态：

- 1：智能体棋子
- -1：对手棋子
- 0：空位置

## Action

智能体可以选择的位置：

```python
(row, col)
```

## Reward

|结果|reward|
|-|-|
|智能体胜利|1|
|平局|0.5|
|失败|0|

---

# 3. State定义的重要性

最开始采用 Sutton 书中的简化定义：

> 只保存轮到智能体行动的状态。

此时：

$$
V(s)
$$

表示：

> 从这个状态开始，智能体获胜的概率。

后来意识到更通用的 MDP 定义：（*没做*）

```python
state = (board, current_player)
```

因为同一个棋盘，不同玩家行动时价值不同。

---

# 4. Value Function

定义：

$$
V(s)
$$

表示从状态 s 开始按照当前策略行动的期望回报。

井字棋中：

$$
V(s)=P(win|s) 
$$

---

# 5. Monte Carlo Prediction

训练流程：

```
生成一局游戏
      ↓
记录trajectory
      ↓
得到最终reward
      ↓
反向更新状态价值
```

更新：

$$
V(s)\leftarrow V(s)+\alpha(V(s')-V(s))
$$

代码思想：

```python
next_value = terminal_reward

for state in reversed(trajectory):

    value = V[state]

    value += alpha * (next_value - value)

    V[state] = value

    next_value = value
```

---

# 6. Epsilon-Greedy

强化学习需要探索：

$$
\epsilon
$$

概率随机选择动作，否则选择当前最优动作。

```python
if random.random() < epsilon:
    random action
else:
    best action
```

---

# 7. Value到Policy

学习的是：

$$
V(s)
$$

但需要产生动作：

$$
\pi(a|s)
$$

因此根据动作后的状态价值选择：

$$
a^*=argmax_a V(s')
$$

---

# 8. Q Value理解

动作价值：

$$
Q(s,a)
$$

表示执行动作后的价值。

当前项目中：

$$
Q(s,a)=V(s')
$$

---

# 9. Opponent作为Environment Model

项目中的：

```python
opponent.act(board)
```

可以看作环境模型的一部分：

```
state
 ↓
agent action
 ↓
opponent model
 ↓
next state
```

这属于 Model-based 思想。

---

# 10. 实验经验

## RandomOpponent

训练效果：

- Value可以收敛
- Agent可以学习基本策略

说明：

- Monte Carlo更新正确
- 状态价值能够学习


## RuleOpponent

问题：

- 对手太强
- Agent早期无法获得正反馈

表现：

```
不断失败
 ↓
V下降
 ↓
探索减少
 ↓
继续失败
```

这是强化学习中的：

- exploration problem
- sparse reward problem

---

# 11. 重要经验总结

## 1. 状态定义决定学习目标

不同state定义对应不同价值函数。

---

## 2. 强对手不一定适合训练

更合理：

```
Random opponent
        ↓
Weak opponent
        ↓
Strong opponent
```

逐渐增加难度。

---

## 3. Value Function依赖环境

训练 RandomOpponent：

$$
V_{random}(s)
$$

测试 RuleOpponent：

需要不同环境下的价值估计。

---

# 12. 后续学习路线

## TD Learning

使用：

$$
R+\gamma V(s')
$$

减少Monte Carlo等待终局的问题。

---

## SARSA

学习：

$$
Q(s,a)
$$

---

## Q-Learning

学习最优动作价值：

$$
Q(s,a)
\leftarrow
Q(s,a)+\alpha(r+\gamma maxQ(s',a')-Q(s,a))
$$

---

## Deep Q Network

使用神经网络代替Q-table：

```
state
 ↓
Neural Network
 ↓
Q values
```

---

# 总结

通过井字棋强化学习项目，完成了完整RL流程：

```
Environment
      ↓
State definition
      ↓
Value estimation
      ↓
Policy selection
      ↓
Exploration
      ↓
Training
      ↓
Evaluation
```

最大的收获：

> 强化学习首先是一个建模问题，其次才是算法问题。

状态如何定义、环境如何表示、策略如何产生，决定了智能体能够学习什么。
