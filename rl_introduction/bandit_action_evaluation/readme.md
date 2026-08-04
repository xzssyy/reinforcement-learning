# 10-Armed Bandit Testbed

- 随机生成 2000 个独立的 10-armed bandit 任务作为测试环境。
- 对于每个 bandit，初始化每个动作的真实价值：
  
  $$
  q(a)
  $$

  并保持不变。
- 在每个 bandit 任务中，智能体使用 epsilon-greedy 策略进行 1000 次交互：
  - 根据当前动作价值估计 $Q_t(a)$ 选择动作；
  - 环境返回带噪声的奖励：
    
    $$
    R_t=q(A_t)+\epsilon,\quad \epsilon\sim\mathcal{N}(0,1)
    $$

  - 使用 sample-average 方法更新动作价值估计：
    
    $$
    Q_{t+1}(A_t)=Q_t(A_t)+\frac{1}{N_t(A_t)}
    (R_t-Q_t(A_t))
    $$

- 对 2000 个 bandit 任务在每个时间步的实验结果进行平均，得到算法随训练步数变化的性能曲线。

- 统计两项指标：
  1. **Average Reward**
     - 计算每个时间步所有 bandit 任务获得奖励的平均值，用于衡量算法整体收益。

  2. **Optimal Action Percentage**
     - 记录每个时间步智能体选择真实最优动作的比例：
       
       $$
       \frac{\text{选择 optimal action 的次数}}
       {\text{总任务数量}}
       $$
     - 用于衡量算法发现最优动作的能力。
  

  ![](/bandit/pictures/10-armed%20testbed-1000steps.png)
  ![](/bandit/pictures/10-armed%20testbed-20000steps.png)

  ## 平衡探索和利用

  - 可以采取随时间下降的epsilon-greedy策略来提高算法的性能。
  - 高噪声选择探索，低噪声选择利用。
  - 以及奖励函数随时间变化
  

  # nonstationary enviroment

  The stepsize constant $\alpha$ is used to update the action-value estimates in a nonstationary environment. The update rule is:

 Q_k denote kth estimate of the action value, and R_k denote the kth reward received for that action. 

Q_k -> R_k -> Q_k+1 -> R_k+1 -> ......


$$
\begin{aligned}
Q_{t+1} 
&=Q_t+\alpha(R_t-Q_t) \\
&= \alpha R_t+(1-\alpha)Q_t \\
&= \alpha R_t+(1-\alpha)\alpha R_{t-1}+(1-\alpha)^2\alpha R_{t-2}+\cdots+(1-\alpha)^{t-1}\alpha R_1+(1-\alpha)^t Q_1 \\
&= (1-\alpha)^t Q_1 + \sum_{i=1}^{t} \alpha (1-\alpha)^{t-i} R_i 
\end{aligned}
$$

It called exponential recency-weighted average, which gives more weight to recent rewards. The constant step-size parameter $\alpha$ determines how much weight is given to the most recent reward compared to past rewards. A larger $\alpha$ means that the agent will adapt more quickly to changes in the environment, while a smaller $\alpha$ means that the agent will be more stable and less sensitive to noise.




sample average 越来越相信历史
constant step-size 越来越相信最近的奖励，适应性强，保持更新能力

  