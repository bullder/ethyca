import unittest
from unittest.mock import MagicMock, patch
from chalice.test import Client
from app.app import app
from app.models.game import Game

class TestApp(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.patcher = patch('app.app.game_service.repository', self.mock_repo)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_create_game(self):
        with Client(app) as client:
            self.mock_repo.save_game.return_value = None
            
            response = client.http.post('/api/games')
            self.assertEqual(response.status_code, 201)
            self.assertIn('id', response.json_body)
            self.assertEqual(response.json_body['status'], 'IN_PROGRESS')

    def test_list_games(self):
        with Client(app) as client:
            game1 = Game()
            game2 = Game()
            self.mock_repo.list_games.return_value = [game1, game2]

            response = client.http.get('/api/games')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.json_body), 2)
            self.assertEqual(response.json_body[0]['id'], game1.id)

    def test_get_game_found(self):
        with Client(app) as client:
            game = Game()
            self.mock_repo.get_game.return_value = game

            response = client.http.get(f'/api/games/{game.id}')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json_body['id'], game.id)

    def test_get_game_not_found(self):
        with Client(app) as client:
            self.mock_repo.get_game.return_value = None

            response = client.http.get('/api/games/nonexistent')
            self.assertEqual(response.status_code, 404)

    def test_make_move_success(self):
        with Client(app) as client:
            game = Game()
            self.mock_repo.get_game.return_value = game
            
            payload = {'x': 0, 'y': 0}
            response = client.http.post(f'/api/games/{game.id}/move', body=payload)
            
            self.assertEqual(response.status_code, 200)
            game_data = response.json_body
            board = game_data['board']
            self.assertEqual(board[0], 'X')
            self.assertEqual(len(game_data['history']), 2)

            self.mock_repo.save_game.assert_called()

    def test_make_move_invalid_input(self):
        with Client(app) as client:
            game = Game()
            self.mock_repo.get_game.return_value = game
            response = client.http.post(f'/api/games/{game.id}/move', body={'x': 0})
            self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
