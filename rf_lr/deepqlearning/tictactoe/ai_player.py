import random
import numpy as np

from typing import Sequence
from keras.layers import Dense
from keras.models import Sequential
from constants import BLANK
from player import Player
from player_ticker import PlayerTicker


class DeepAIPlayer(Player):

    def __init__(self,
                 epsilon=0.4,
                 alpha=0.3,
                 gamma=0.9,
                 player_ticker=PlayerTicker.X_PLAYER):
        """
        The training of this AI Player is made using the Q-Learning algorithm, below the Q-Learning formula:
        Q(s, a) = Q(s, a) + alpha[R(s, a) + epsilon max Q(s', a') - Q(s, a)]

        This formula works with time difference.
        """
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.qtable = self._create_deep_qtable()
        self.move = None
        self.board = (BLANK,) * 9
        self._player_ticker = player_ticker

    def ticker(self) -> str:
        return self._player_ticker

    @classmethod
    def available_moves(cls, board: Sequence[str]) -> Sequence[int]:
        return [i for i in range(9) if BLANK == board[i]]

    def get_q(self, state: Sequence, action):
        return self.qtable.predict([self._encode_input(state, action)], batch_size=1, verbose=0)

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
            q_input = self._encode_input(self.board, self.move)
            q_function = prev_q + self.alpha * (reward + self.gamma * max_q_new - prev_q)
            self.qtable.fit(q_input, q_function, epochs=3, verbose=0)

        self.move = None
        self.board = None

    @classmethod
    def _create_deep_qtable(cls) -> Sequential:
        qtable = Sequential()
        qtable.add(Dense(input_dim=36, units=32, activation="relu"))
        qtable.add(Dense(input_dim=32, units=3, activation="relu"))
        qtable.add(Dense(units=1, activation="relu"))
        qtable.compile(optimizer="adam",
                       loss="mse")
        return qtable

    @classmethod
    def _encode_input(cls, board: Sequence, action: int):
        # we represent the (s, a) pair with one-hot representation
        one_hot = []

        # one-hot encoding for the 3 states per cell in the board
        # 1, 0, 0 - It means the given cell has X ticker
        # 0, 1, 0 - It means the given cell has O ticker
        # 0, 0, 1 - It means the given cell has BLANK ticker
        # (9 cells)*(3 values) = 27 values to represent the state
        for cell in board:
            for ticker in ['X', 'O', ' ']:
                if cell == ticker:
                    one_hot.append(1)
                else:
                    one_hot.append(0)

        # one-hot encoding of the action:
        # 1, 0, 0, 0, 0, 0, 0, 0, 0 - ticker X or O of the player (AI) to the first cell
        # 0, 1, 0, 0, 0, 0, 0, 0, 0 - ticker X or O of the player (AI) to the first cell
        for move in range(9):
            if action == move:
                one_hot.append(1)
            else:
                one_hot.append(0)

        # all together 27+9 = 36 (input layer has 36 neurons)
        return np.array([one_hot])
