from player import Player
from player_ticker import PlayerTicker


class HumanPlayer(Player):

    def __init__(self, player_ticker=PlayerTicker.O_PLAYER):
        self._player_ticker = player_ticker

    def reward(self, _, board: list):
        pass

    def make_move(self, board: list):
        while True:
            try:
                Player.show_board(board)
                move = input('Your next move (cell index 1-9):')
                move = int(move)

                if not (move-1 in range(9)):
                    raise ValueError()
            except ValueError:
                print('Invalid move; try again:\n')
            else:
                return move-1

    def player_ticker(self) -> str:
        return self._player_ticker
