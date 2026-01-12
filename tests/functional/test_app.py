import os
import json
os.environ['TABLE_NAME'] = 'test-table'

import unittest
from unittest.mock import MagicMock, patch
from chalice.test import Client
from app.app import app
from app.models.game import Game

class TestApp(unittest.TestCase):
    def setUp(self):
        self.env_patcher = patch.dict('os.environ', {'TABLE_NAME': 'test-table'})
        self.env_patcher.start()
        
        self.mock_repo = MagicMock()
        # Patch the repository class so when GameService is initialized, it uses our mock
        self.repo_patcher = patch('app.app.DynamoDBGameRepository', return_value=self.mock_repo)
        self.repo_patcher.start()
        
        # Reset the singleton to ensure fresh init
        import app.app
        app.app._game_service = None

    def tearDown(self):
        self.repo_patcher.stop()
        self.env_patcher.stop()

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
            headers = {'Content-Type': 'application/json'}
            response = client.http.post(f'/api/games/{game.id}/move', body=json.dumps(payload), headers=headers)
            
            if response.status_code != 200:
                print(f"DEBUG: Status {response.status_code}, Body: {response.json_body}")

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
            headers = {'Content-Type': 'application/json'}
            response = client.http.post(f'/api/games/{game.id}/move', body=json.dumps({'x': 0}), headers=headers)
            self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
