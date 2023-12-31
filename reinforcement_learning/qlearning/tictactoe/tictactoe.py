import random

from typing import Tuple, List, Iterable, Optional
from constants import (BLANK, REWARD_WIN,
                       REWARD_TIE, REWARD_LOSE)
from player import Player


class TicTacToe:

    def __init__(self, player1: Player, player2: Player):
        self.player1 = player1
        self.player2 = player2
        self.board = [BLANK] * 9

    def play(self):

        first_player_turn = random.choice([True, False])
        player, other_player = self._get_players(first_player_turn)
        print("Player 1 is %s with ticker %s turn!" % (player.__class__.__name__, player.player_ticker()))
        print("Player 2 is %s with ticker %s" % (other_player.__class__.__name__, other_player.player_ticker()))
        Player.show_board(self.board[:])
        print()

        while True:
            player, other_player = self._get_players(first_player_turn)
            player_tickers = [player.player_ticker(), other_player.player_ticker()]
            move = player.make_move(self.board)
            self.board[move] = player.player_ticker()
            game_over, winner = self._is_game_over(player_tickers)

            if game_over:
                if winner == player.player_ticker():
                    self._win_reward(player, other_player)
                elif winner == other_player.player_ticker():
                    self._win_reward(other_player, player)
                else:
                    self._tie_reward(player, other_player)
                break

            first_player_turn = not first_player_turn

    def _get_players(self, first_player_turn: bool):
        if first_player_turn:
            return self.player1, self.player2

        return self.player2, self.player1

    def _is_game_over(self, player_tickers: List[str]) -> Tuple[bool, Optional[str]]:
        """
        Check if the game has reached it's terminal state.
        The following positions are checkED below:
        0 1 2
        3 4 5
        6 7 0
        """
        for player_ticker in player_tickers:
            # Horizontal check
            if (self._board_check(player_ticker, range(0, 3))
                    or self._board_check(player_ticker, range(3, 6))
                    or self._board_check(player_ticker, range(6, 9))):
                return True, player_ticker

            # Vertical check
            if (self._board_check(player_ticker, [0, 3, 6])
                    or self._board_check(player_ticker, [1, 4, 7])
                    or self._board_check(player_ticker, [2, 5, 8])):
                return True, player_ticker

            # Diagonal check
            if (self._board_check(player_ticker, [0, 4, 8])
                    or self._board_check(player_ticker, [2, 4, 6])):
                return True, player_ticker

        if self.board.count(BLANK) == 0:
            return True, None

        return False, None

    def _board_check(self, player_ticker: str, index: Iterable[int]) -> bool:
        return all([player_ticker == self.board[i] for i in index])

    def _win_reward(self, player: Player, other_player: Player):
        Player.show_board(self.board[:])
        player.reward(REWARD_WIN, self.board[:])
        print("\n%s won!" % player.__class__.__name__)
        other_player.reward(REWARD_LOSE, self.board[:])

    def _tie_reward(self, player: Player, other_player: Player):
        Player.show_board(self.board[:])
        print("\nTie!")
        player.reward(REWARD_TIE, self.board[:])
        other_player.reward(REWARD_TIE, self.board[:])
