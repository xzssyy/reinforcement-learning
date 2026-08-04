from rl_introduction.tictactoe.evaluate import evaluate
from rl_introduction.tictactoe.states_generator import StateGenerator
from rl_introduction.tictactoe.env import TicTacToe
from rl_introduction.tictactoe.agent import RuleOpponent, RLAgent, RandomAgent
from tqdm import tqdm


# 进行一次对局采样
def monteCarlo(
    board: TicTacToe,
    states_values: dict,
    terminal_values: dict,
    opponent: RuleOpponent,
    agent: RLAgent,
) -> list[tuple]:
    board.reset()
    trajectory = []
    turn = -1

    while board.winner() == 0 and not board.is_full():
        if turn == -1:
            move = opponent.act(board)
        else:
            state = board.get_state()
            actions = board.legal_moves()
            q_table = {}

            # 创建q表
            for action in actions:
                board.step(action, 1)
                if board.winner() == 1:
                    value = 1
                else:
                    opponent_action = opponent.act(board)
                    board.step(opponent_action, -1)
                    if board.winner() == -1:
                        value = 0
                    elif board.is_full():
                        value = 0.5
                    else:
                        next_state = board.get_state()
                        if next_state in terminal_values:
                            value = terminal_values[next_state]
                        elif next_state in states_values:
                            value = states_values[next_state]
                        else:
                            raise ValueError("unknown state")

                    board.undo(opponent_action)

                board.undo(action)

                q_table[(state, action)] = value

            move = agent.act(state, actions, q_table)
            
            trajectory.append(state)

        board.step(move, turn)
        turn *= -1

    terminal_state = board.get_state()

    return trajectory, terminal_values[terminal_state]

def train(
    board: TicTacToe,
    states_values: dict,
    terminal_values: dict,
    opponent,
    agent,
    episodes=10000,
    alpha=0.1,
):
    """
    TD(0) 风格价值更新训练

    V(s) <- V(s) + alpha * (V(s') - V(s))
    """

    for episode in tqdm(range(episodes), desc="Training"):

        trajectory, terminal_value = monteCarlo(
            board,
            states_values,
            terminal_values,
            opponent,
            agent,
        )

        # 从终止状态反向传播价值
        next_value = terminal_value

        for state in reversed(trajectory):

            value = states_values[state]

            value += alpha * (
                next_value - value
            )

            states_values[state] = value

            # 当前状态成为下一个状态价值
            next_value = value

    return states_values

if __name__ == "__main__":

    # 超参数
    episodes = 10000
    epsilon = 0.3
    alpha = 0.1


    # 环境
    board = TicTacToe(3, 3)


    # 对手
    opponent = RandomAgent()
    opponent_1 = RuleOpponent()


    # 智能体
    agent = RLAgent(
        epsilon=epsilon
    )


    # 状态空间
    state_generator = StateGenerator()

    states_values, terminal_values = (
        state_generator.generate_states(
            board,
            -1
        )
    )


    # 训练
    # 对于随机策略追求胜利
    # train(
    #     board,
    #     states_values,
    #     terminal_values,
    #     opponent,
    #     agent,
    #     episodes,
    #     alpha,
    # )
    
    train(
            board,
            states_values,
            terminal_values,
            opponent_1,
            agent,
            episodes,
            alpha,
        )


    # 查看价值分布
    values = list(states_values.values())

    print(
        "max:",
        max(values)
    )

    print(
        "min:",
        min(values)
    )

    print(
        "mean:",
        sum(values) / len(values)
    )


    # 测试
    evaluate(
        board,
        states_values,
        terminal_values,
        RuleOpponent(),
        agent,
        games=10000
    ) 
    
    evaluate(
            board,
            states_values,
            terminal_values,
            RandomAgent(),
            agent,
            games=10000
        ) 
