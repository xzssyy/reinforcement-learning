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
  
  