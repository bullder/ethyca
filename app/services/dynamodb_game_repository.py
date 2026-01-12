import os
import boto3
from typing import Optional, List
from app.models.game import Game
from .game_repository import GameRepository
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

class DynamoDBGameRepository(GameRepository):
    def __init__(self):
        table_name = os.environ.get('TABLE_NAME')
        if not table_name:
            raise RuntimeError("TABLE_NAME environment variable not set")

        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)

    def save_game(self, game: Game) -> Game:
        try:
            item = game.model_dump(mode='json')
            
            logger.info(f"Saving game to table {self.table.name}: {item}")
            self.table.put_item(Item=item)
            return game
        except ClientError as e:
            logger.error(f"ClientError saving game: {e.response['Error']['Code']} - {e.response['Error']['Message']}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error saving game: {type(e).__name__} - {e}")
            raise

    def get_game(self, game_id: str) -> Optional[Game]:
        try:
            response = self.table.get_item(Key={'id': game_id})
            item = response.get('Item')
            if not item:
                return None
            return Game(**item)
        except ClientError as e:
            logger.error(f"Error fetching game from DynamoDB: {e}")
            return None
        except Exception as e:
            logger.error(f"Error parsing game data: {e}")
            return None

    def list_games(self, limit: int = 100) -> List[Game]:
        try:
            response = self.table.scan(Limit=limit)
            items = response.get('Items', [])
            return [Game(**item) for item in items]
        except ClientError as e:
            logger.error(f"Error listing games from DynamoDB: {e}")
            return []
