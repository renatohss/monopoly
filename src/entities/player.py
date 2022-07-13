from abc import ABC, abstractmethod
from random import randint


class Player(ABC):
    def __init__(self, start_cash: float = 300):
        self.cash = start_cash
        self.position = 0
        self.victories = 0
        self.order = 0

    @property
    def is_active(self) -> bool:
        return False if self.cash < 0 else True

    @property
    def name(self) -> str:
        return "Base Player"

    def win_game(self):
        self.victories += 1

    def receive_rent(self, rent: float):
        self.cash += rent

    def pay_rent(self, rent: float):
        self.cash -= rent

    def move(self, dice_roll: int):
        self.position += dice_roll
        if self.position > 19:
            extra_spaces = self.position - 19
            self.cash += 100
            self.position = 0 + extra_spaces

    @abstractmethod
    def can_buy(self, cost: float) -> bool:
        pass


class ImpulsivePlayer(Player):
    def can_buy(self, cost: float):
        if self.cash > cost:
            self.cash -= cost
            return True
        return False

    @property
    def name(self) -> str:
        return "Impulsive"


class DemandingPlayer(Player):
    def can_buy(self, cost: float):
        if 50 < cost < self.cash:
            self.cash -= cost
            return True
        return False

    @property
    def name(self) -> str:
        return "Demanding"


class CautiousPlayer(Player):
    def can_buy(self, cost: float):
        if self.cash - cost >= 80:
            self.cash -= cost
            return True
        return False

    @property
    def name(self) -> str:
        return "Cautious"


class RandomPlayer(Player):
    def can_buy(self, cost: float):
        if randint(1, 2) == 1 and self.cash > cost:
            self.cash -= cost
            return True
        return False

    @property
    def name(self) -> str:
        return "Random"
