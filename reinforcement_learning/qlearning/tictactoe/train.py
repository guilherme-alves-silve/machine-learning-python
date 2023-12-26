from constants import TRAINING_EPSILON, TRAINING_EPOCHS
from ai_player import AIPlayer
from human_player import HumanPlayer
from player_ticker import PlayerTicker
from tictactoe import TicTacToe


if __name__ == "__main__":
    ai_player1 = AIPlayer(epsilon=TRAINING_EPSILON,
                          player_ticker=PlayerTicker.X_PLAYER)
    ai_player2 = AIPlayer(epsilon=TRAINING_EPSILON,
                          player_ticker=PlayerTicker.O_PLAYER)

    print("Training the AI players...")

    for epoch in range(TRAINING_EPOCHS):
        game = TicTacToe(ai_player1, ai_player2)
        game.play()

    print("\nTraining is done!")

    # epsilon = 0 means no exploration - it will use the Q(s, a) function to make the moves
    ai_player1.epsilon = 0
    human_player = HumanPlayer()
    game = TicTacToe(ai_player1, human_player)
    game.play()
