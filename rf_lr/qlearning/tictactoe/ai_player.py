import random
from typing import Sequence

from constants import BLANK
from player import Player
from player_ticker import PlayerTicker


class AIPlayer(Player):

    def __init__(self,
                 epsilon=0.4,
                 alpha=0.3,
                 gamma=0.9,
                 default_q=1,
                 player_ticker=PlayerTicker.X_PLAYER):
        """
        The training of this AI Player is made using the Q-Learning algorithm, below the Q-Learning formula:
        Q(s, a) = Q(s, a) + alpha[R(s, a) + epsilon max Q(s', a') - Q(s, a)]

        This formula works with time difference.
        """
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.default_q = default_q
        self.qtable = {}
        self.move = None
        self.board = (BLANK,) * 9
        self._player_ticker = player_ticker

    def player_ticker(self) -> str:
        return self._player_ticker

    @classmethod
    def available_moves(cls, board: Sequence[str]):
        return [i for i in range(9) if BLANK == board[i]]

    def get_q(self, state: Sequence, action):
        if self.qtable.get((state, action)) is None:
            self.qtable[(state, action)] = self.default_q

        return self.qtable[(state, action)]

    def make_move(self, board: list):
        self.board = tuple(board)
        actions = self.available_moves(board)

        if random.random() < self.epsilon:
            # Exploration
            self.move = random.choice(actions)
            return self.move

        # Exploitation
        # max Q(s', a')
        q_values = [self.get_q(self.board, a) for a in actions]
        max_q_value = max(q_values)

        if q_values.count(max_q_value) > 1:
            best_actions = [i for i in range(len(actions)) if q_values[i] == max_q_value]
            best_move = actions[random.choice(best_actions)]
        else:
            best_move = actions[q_values.index(max_q_value)]

        self.move = best_move
        return self.move

    def reward(self, reward: int, board: list):
        if self.move:
            # Q(s, a) = Q(s, a) + alpha[R(s, a) + epsilon max Q(s', a') - Q(s, a)]
            prev_q = self.get_q(self.board, self.move)
            max_q_new = max([self.get_q(tuple(board), a) for a in self.available_moves(self.board)])
            self.qtable[(self.board, self.move)] = prev_q + self.alpha * (reward + self.gamma * max_q_new - prev_q)

        self.move = None
        self.board = None
