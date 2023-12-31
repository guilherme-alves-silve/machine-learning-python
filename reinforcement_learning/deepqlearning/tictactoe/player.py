class Player:

    def reward(self, reward, board: list):
        pass

    def make_move(self, board: list):
        pass

    def ticker(self) -> str:
        pass

    @staticmethod
    def show_board(board: list):
        print('|'.join(board[0:3]))
        print('|'.join(board[3:6]))
        print('|'.join(board[6:9]))
