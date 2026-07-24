def evaluate(board, states_values, terminal_values, opponent, agent, games=1000):
    win = 0
    lose = 0
    draw = 0

    # 保存原来的探索率
    old_epsilon = agent.epsilon

    # 测试关闭探索
    agent.epsilon = 0

    for _ in range(games):

        board.reset()

        turn = -1

        while board.winner() == 0 and not board.is_full():

            if turn == -1:
                # 对手行动
                move = opponent.act(board)

            else:
                # agent行动

                state = board.get_state()
                actions = board.legal_moves()

                q_table = {}

                # 根据当前V估计Q
                for action in actions:

                    board.step(action, 1)

                    # agent直接赢
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

            board.step(move, turn)

            turn *= -1

        result = terminal_values[board.get_state()]

        if result == 1:
            win += 1

        elif result == 0:
            lose += 1

        else:
            draw += 1

    # 恢复epsilon
    agent.epsilon = old_epsilon

    print(f"Games: {games}")
    print(f"Win:  {win} ({win/games:.2%})")
    print(f"Draw: {draw} ({draw/games:.2%})")
    print(f"Lose: {lose} ({lose/games:.2%})")

    return {
        "win_rate": win / games,
        "draw_rate": draw / games,
        "lose_rate": lose / games,
    }
