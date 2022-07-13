import math
import random
from random import randint
from typing import Optional

from src.entities.player import Player


class BoardSpace:
    def __init__(self, index: int):
        self.index: int = index
        self.owner: Optional[Player] = None
        self.value: int = randint(150, 500)
        self.rent: int = math.floor(self.value * 0.25)

    def sell_space(self, player: Player):
        if player.can_buy(cost=self.value):
            self.owner = player


class Board:
    def __init__(self):
        self.__board: list[BoardSpace] = []
        self.__players: list[Player] = []

    def build_board(self, total_spaces: int = 20):
        for idx in range(total_spaces):
            space = BoardSpace(index=idx)
            self.__board.append(space)

    def get_board(self):
        return [(space.index, space.owner, space.value, space.rent) for space in self.__board]

    def set_players(self, players: list[Player]):
        self.__players = players
        random.shuffle(self.__players)

    def get_players(self):
        return [player.name for player in self.__players]

    def start_game(self, players: list[Player]):
        self.build_board()
        self.set_players(players=players)
