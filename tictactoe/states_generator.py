from env import TicTacToe
class StateGenerator:

    def __init__(self):
        # 智能体需要决策的状态
        self.states = set()

        # V(s)
        self.V = {}

        # 终止状态的结果
        # 1: 智能体赢
        # 0: 平局
        # -1: 智能体输
        self.terminal_values = {}

        # 防止重复搜索
        self.visited = set()


    def generate_states(self, board: TicTacToe, player):
        self.backtrace(board, player)
        
        return self.V, self.terminal_values
        
    def backtrace(self, board: TicTacToe, player):

        state = board.get_state()

        # 当前棋盘已经搜索过
        if state in self.visited:
            return

        self.visited.add(state)


        # 遍历当前玩家所有动作
        for move in board.legal_moves():

            board.step(move, player)

            next_state = board.get_state()


            # ---------- 终止 ----------
            winner = board.winner()

            if winner != 0:

                # winner:
                # 1  智能体赢
                # 0 对手赢
                self.terminal_values[next_state] = (winner + 1) // 2

                board.undo(move)
                continue


            if board.is_full():

                self.terminal_values[next_state] = 0.5

                board.undo(move)
                continue


            # ---------- 非终止 ----------
            # 如果刚刚是对手落子
            # 那么现在轮到智能体
            if player == -1:

                if next_state not in self.states:
                    self.states.add(next_state)

                    # 初始价值
                    self.V[next_state] = 0.5


            # 下一回合
            self.backtrace(
                board,
                -player
            )


            # 回溯
            board.undo(move)
            
            
        