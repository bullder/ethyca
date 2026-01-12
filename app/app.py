import logging
from chalice import Chalice, Response, NotFoundError as ChaliceNotFoundError
from http import HTTPStatus

from app.models import (
    Move,
    GameMove,
    GameResponse,
    TicTacToeError,
    BadRequestError as AppBadRequestError
)
from app.models.responses.games_list_response import GamesListResponse
from app.services import GameService, DynamoDBGameRepository

app = Chalice(app_name='tic-tac-toe-api')
app.debug = True
app.log.setLevel(logging.INFO)

game_service = GameService(DynamoDBGameRepository())

@app.route('/api/games', methods=['POST'], cors=True)
def create_game():
    app.log.info("Creating new game")
    game = game_service.create_game()
    app.log.info(f"Game created with ID: {game.id}")
    return GameResponse().to_response(game, HTTPStatus.CREATED)

@app.route('/api/games', methods=['GET'], cors=True)
def list_games():
    app.log.info("Listing games")
    return GamesListResponse().to_response(games=game_service.list_games())

@app.route('/api/games/{game_id}', methods=['GET'], cors=True)
def get_game(game_id):
    app.log.info(f"Fetching game: {game_id}")
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
             raise AppBadRequestError("Missing request body")
        game_request = GameMove(game_id=game_id, move=Move(**request.json_body))
    except Exception as e:
        app.log.error(f"Invalid request: {e}")
        raise AppBadRequestError("Invalid JSON body")

    try:
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
