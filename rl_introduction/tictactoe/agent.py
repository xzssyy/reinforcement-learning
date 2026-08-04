from env import TicTacToe
import random


class RuleOpponent:
    """
    规则型井字棋对手,相当于一个环境模型

    mark:
        对手棋子，默认 -1

    opponent_mark:
        智能体棋子，默认 1
    """

    def __init__(self, mark=-1, opponent_mark=1):

        self.mark = mark
        self.opponent_mark = opponent_mark

    def act(self, board: TicTacToe):

        moves = board.legal_moves()

        strategies = [
            self.find_winning_move,
            self.find_block_move,
            self.find_fork,
            self.find_block_fork,
            self.find_center,
            self.find_opposite_corner,
            self.find_corner,
            self.find_side,
        ]

        for strategy in strategies:

            move = strategy(board, moves)

            if move is not None:
                return move

        return None

    # 1. 自己能赢就赢
    def find_winning_move(self, board, moves):

        for move in moves:

            board.step(move, self.mark)

            if board.winner() == self.mark:
                board.undo(move)
                return move

            board.undo(move)

        return None

    # 2. 堵对方
    def find_block_move(self, board, moves):

        for move in moves:

            board.step(move, self.opponent_mark)

            if board.winner() == self.opponent_mark:
                board.undo(move)
                return move

            board.undo(move)

        return None

    # 3. 制造 fork
    def find_fork(self, board, moves):

        for move in moves:

            fork_count = 0

            board.step(move, self.mark)

            for next_move in board.legal_moves():

                board.step(next_move, self.mark)

                if board.winner() == self.mark:
                    fork_count += 1

                board.undo(next_move)

            board.undo(move)

            if fork_count >= 2:
                return move

        return None

    # 4. 阻止 fork
    def find_block_fork(self, board, moves):

        for move in moves:

            fork_count = 0

            board.step(move, self.opponent_mark)

            for next_move in board.legal_moves():

                board.step(next_move, self.opponent_mark)

                if board.winner() == self.opponent_mark:
                    fork_count += 1

                board.undo(next_move)

            board.undo(move)

            if fork_count >= 2:
                return move

        return None

    # 5. 抢中心
    def find_center(self, board, moves):

        center = (board.row // 2, board.col // 2)

        if center in moves:
            return center

        return None

    # 6. 抢对角
    def find_opposite_corner(self, board, moves):

        for corner, opposite in board.opposite.items():

            if board.check(corner) == self.opponent_mark and board.check(opposite) == 0:
                return opposite

        return None

    # 7. 抢角落
    def find_corner(self, board, moves):

        for corner in board.corners:

            if corner in moves:
                return corner

        return None

    # 8. 抢边
    def find_side(self, board, moves):

        for move in moves:

            row, col = move

            is_edge = (
                row == 0 or row == board.row - 1 or col == 0 or col == board.col - 1
            )

            if is_edge and move not in board.corners:
                return move

        return None


class RLAgent:

    def __init__(self, epsilon=0.1):
        self.epsilon = epsilon
    

    def act(self, state, actions, q_values: dict):

        # 探索
        if random.random() < self.epsilon:
            return random.choice(actions)

        # 利用
        values = [
            q_values.get(
                (state, action),
            )
            for action in actions
        ]

        max_value = max(values)
        best_actions = [
            action for action, value in zip(actions, values) if value == max_value
        ]

        return random.choice(best_actions)

class RandomAgent:
    """
    随机策略玩家
    """

    def __init__(self, mark=-1):
        self.mark = mark

    def act(self, board: TicTacToe):

        moves = board.legal_moves()

        if not moves:
            return None

        return random.choice(moves)