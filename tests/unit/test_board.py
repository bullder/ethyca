import unittest
from app.models.board import Board
from app.models.enums.player import Player

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_initial_state(self):
        self.assertTrue(all(cell is None for cell in self.board.cells))
        self.assertFalse(self.board.is_full())

    def test_is_occupied(self):
        self.board.cells[0] = Player.X
        self.assertTrue(self.board.is_occupied(0))
        self.assertFalse(self.board.is_occupied(1))

    def test_is_full(self):
        self.board.cells = [Player.X] * 9
        self.assertTrue(self.board.is_full())
        
        self.board.cells[0] = None
        self.assertFalse(self.board.is_full())

    def test_check_winner_rows(self):
        self.board.cells[0] = Player.X
        self.board.cells[1] = Player.X
        self.board.cells[2] = Player.X
        self.assertEqual(self.board.check_winner(), Player.X)

    def test_check_winner_cols(self):
        self.board.cells[0] = Player.O
        self.board.cells[3] = Player.O
        self.board.cells[6] = Player.O
        self.assertEqual(self.board.check_winner(), Player.O)

    def test_check_winner_diag(self):
        self.board.cells[0] = Player.X
        self.board.cells[4] = Player.X
        self.board.cells[8] = Player.X
        self.assertEqual(self.board.check_winner(), Player.X)

    def test_get_random_available_cell_initial(self):
        move = self.board.get_random_available_cell()
        self.assertIsNotNone(move)
        self.assertTrue(0 <= move.x <= 2)
        self.assertTrue(0 <= move.y <= 2)

    def test_get_random_available_cell_full(self):
        self.board.cells = [Player.X] * 9
        move = self.board.get_random_available_cell()
        self.assertIsNone(move)

if __name__ == '__main__':
    unittest.main()
