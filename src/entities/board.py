import math
import random
from random import randint
from typing import Optional

from src.entities.misc import Dice
from src.entities.player import Player


class BoardSpace:
    def __init__(self, index: int):
        self.index: int = index
        self.owner: Optional[Player] = None
        self.value: int = randint(100, 500)
        self.rent: int = math.floor(self.value * 0.25)

    def sell_space(self, player: Player):
        if player.can_buy(cost=self.value):
            self.owner = player

    def pay_rent(self, payer: Player):
        if payer != self.owner:
            payer.cash -= self.rent
            self.owner.cash += self.rent


class Board:
    def __init__(self):
        self.dice = Dice()
        self.__board: list[BoardSpace] = []
        self.__players: list[Player] = []

    def build_board(self, total_spaces: int = 20):
        for idx in range(total_spaces):
            space = BoardSpace(index=idx)
            self.__board.append(space)

    def get_board(self):
        return [(space.index, space.owner, space.value, space.rent) for space in self.__board]

    def get_property(self, index: int) -> BoardSpace:
        return self.__board[index]

    def set_players(self, players: list[Player]):
        self.__players = players

    def get_players(self):
        return [player for player in self.__players]

    def check_active_players(self) -> list[Player]:
        active_players = []
        for player in self.__players:
            if player.is_active:
                active_players.append(player)
        return active_players

    def new_round(self):
        random.shuffle(self.__players)
        for player in self.__players:
            player.cash = 300
            player.is_active = True
        for space in self.__board:
            space.owner = None

    def start_game(self, players: list[Player]):
        self.build_board()
        self.set_players(players=players)
