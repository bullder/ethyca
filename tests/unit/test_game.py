import unittest
from app.models.game import Game
from app.models.enums.player import Player
from app.models.enums.game_status import GameStatus
from app.models.requests.move import Move
from app.models.exceptions import InvalidTurnError, PositionOccupiedError

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def test_initial_state(self):
        self.assertEqual(self.game.status, GameStatus.IN_PROGRESS)
        self.assertEqual(self.game.current_turn, Player.X)
        self.assertIsNone(self.game.winner)
        self.assertEqual(len(self.game.history), 0)

    def test_process_move_valid(self):
        move = Move(x=0, y=0)
        self.game.process_move(move)
        self.assertEqual(self.game.board.cells[0], Player.X)
        self.assertEqual(len(self.game.history), 2)
        self.assertEqual(self.game.history[0].x, 0)
        self.assertEqual(self.game.history[0].y, 0)
        computer_move = self.game.history[1]
        self.assertEqual(self.game.board.cells[computer_move.position], Player.O)
        self.assertEqual(self.game.current_turn, Player.X)

    def test_process_move_win(self):
        self.game.board.cells[0] = Player.X
        self.game.board.cells[1] = Player.X
        self.game.board.cells[3] = Player.O
        self.game.board.cells[4] = Player.O
        
        move = Move(x=2, y=0)
        self.game.process_move(move)

        self.assertEqual(self.game.status, GameStatus.WON_X)
        self.assertEqual(self.game.winner, Player.X)
        self.assertEqual(len(self.game.history), 1)

    def test_invalid_turn(self):
        self.game.current_turn = Player.O
        move = Move(x=0, y=0)
        with self.assertRaises(InvalidTurnError):
            self.game._validate_move(move, Player.X)

    def test_position_occupied(self):
        self.game.board.cells[0] = Player.X
        move = Move(x=0, y=0)
        with self.assertRaises(PositionOccupiedError):
            self.game._validate_move(move, Player.X)

if __name__ == '__main__':
    unittest.main()
