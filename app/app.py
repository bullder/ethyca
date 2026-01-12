import os
import logging
from http import HTTPStatus
from app.models import (
    Move,
    GameMove,
    GameResponse,
    TicTacToeError
)
from chalice import Chalice, Response, NotFoundError as ChaliceNotFoundError, BadRequestError as ChaliceBadRequestError
from app.models.responses.games_list_response import GamesListResponse
from app.services import GameService, DynamoDBGameRepository

app = Chalice(app_name='tic-tac-toe-api')
app.debug = os.environ.get('DEBUG', 'False').lower() == 'true'
app.log.setLevel(logging.INFO)

_game_service = None

def get_game_service():
    global _game_service
    if _game_service is None:
        _game_service = GameService(DynamoDBGameRepository())
    return _game_service

@app.route('/api/games', methods=['POST'], cors=True)
def create_game():
    app.log.info("Creating new game")
    game_service = get_game_service()
    game = game_service.create_game()
    app.log.info(f"Game created with ID: {game.id}")
    return GameResponse().to_response(game, HTTPStatus.CREATED)

@app.route('/api/games', methods=['GET'], cors=True)
def list_games():
    app.log.info("Listing games")
    game_service = get_game_service()
    return GamesListResponse().to_response(games=game_service.list_games())

@app.route('/api/games/{game_id}', methods=['GET'], cors=True)
def get_game(game_id):
    app.log.info(f"Fetching game: {game_id}")
    game_service = get_game_service()
    game = game_service.get_game(game_id)
    if not game:
        app.log.warning(f"Game not found: {game_id}")
        raise ChaliceNotFoundError(f"Game not found: {game_id}")
    return GameResponse().to_response(game)

@app.route('/api/games/{game_id}/move', methods=['POST'], cors=True)
def make_move(game_id):
    app.log.info(f"Making move for game: {game_id}")
    request = app.current_request
    try:
        if not request.json_body:
             app.log.error("Missing request body")
             raise ChaliceBadRequestError("Missing request body")
        game_request = GameMove(game_id=game_id, move=Move(**request.json_body))
    except Exception as e:
        app.log.error(f"Invalid request: {e}")
        raise ChaliceBadRequestError(f"Invalid JSON body: {e}")

    try:
        game_service = get_game_service()
        updated_game = game_service.make_move(game_request)
        app.log.info(f"Move successful for game: {game_id}")
        return  GameResponse().to_response(updated_game)
    except TicTacToeError as e:
        app.log.error(f"Game error: {e}")
        return Response(
            body={"detail": str(e)},
            status_code=e.status_code,
            headers={"Content-Type": "application/json"}
        )
