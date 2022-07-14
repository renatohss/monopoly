import math

from src.entities.board import Board
from src.entities.player import ImpulsivePlayer, DemandingPlayer, CautiousPlayer, RandomPlayer, Player

MAX_SIMS = 300
MAX_ROUNDS = 1000


def get_timeout_winner(players: list[Player]) -> Player:
    wins = [player.cash for player in players]
    winner = players[wins.index(max(wins))]
    return winner


def has_winner(board: Board, rounds: int) -> bool:
    active_players = board.check_active_players()
    if len(active_players) == 1:
        active_players[0].win_game()
        return True
    if rounds > MAX_ROUNDS:
        get_timeout_winner(players=board.get_players()).win_game()
        return True
    return False


def play_round(board: Board, max_rounds: int):
    cur_round = 0
    while cur_round <= max_rounds:
        cur_round += 1
        for player in board.check_active_players():
            player.move(dice_roll=board.dice.roll())
            board_space = board.get_property(player.position)
            if not board_space.owner:
                board_space.sell_space(player=player)
            else:
                board_space.pay_rent(payer=player)
            player.check_status()
            if not player.is_active:
                board.remove_player(player=player)
        if has_winner(board=board, rounds=cur_round):
            break
    return {
        "total_rounds": cur_round,
        "timeout": True if cur_round > 1000 else False
    }


def show_results(timeout: int, rounds: int, players: list[Player]):
    wins = [player.victories for player in players]
    winner = players[wins.index(max(wins))]
    return {
        "Total simulations": MAX_SIMS,
        "Max number of rounds before timeout": MAX_ROUNDS,
        "Total simulations ended with timeout": timeout,
        "Avg. number of rounds": math.floor(rounds/MAX_SIMS),
        f"Win % for {players[0].name}": round((players[0].victories/MAX_SIMS)*100, 2),
        f"Win % for {players[1].name}": round((players[1].victories/MAX_SIMS)*100, 2),
        f"Win % for {players[2].name}": round((players[2].victories/MAX_SIMS)*100, 2),
        f"Win % for {players[3].name}": round((players[3].victories/MAX_SIMS)*100, 2),
        "Player with most wins": winner.name
    }


def main():
    total_timeout = 0
    total_rounds = 0

    players = [ImpulsivePlayer(), DemandingPlayer(), CautiousPlayer(), RandomPlayer()]

    game_board = Board()
    game_board.start_game(players=players)
    for sim in range(MAX_SIMS):
        game_board.new_round()
        result = play_round(board=game_board, max_rounds=MAX_ROUNDS)
        total_rounds += result["total_rounds"]
        if result["timeout"]:
            total_timeout += 1
    print(show_results(timeout=total_timeout, rounds=total_rounds, players=players))


if __name__ == "__main__":
    main()
