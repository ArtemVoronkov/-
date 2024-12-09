import inspect
import json
import sys

from src.deck import Deck
from src.game_state import GameState
from src.hand import Hand
from src.player import Player
from src.Interactions import PlayerInteraction
import src.Player_Interactions as all_player_types

import logging

import enum


class GamePhase(enum.StrEnum):
    CHOOSE_CARD = "Choose card"
    DRAW_EXTRA = "Draw extra card"
    NEXT_PLAYER = "Switch current player"
    DECLARE_WINNER = "Declare a winner"
    GAME_END = "Game ended"


class GameServer:
    INITIAL_HAND_SIZE = 6

    def __init__(self, player_types, game_state):
        self.game_state: GameState = game_state
        self.player_types: dict = player_types  # {player: PlayerInteractions}

    @classmethod
    def load_game(cls):
        # TODO: выбрать имя файла
        filename = 'uno.json'
        with open(filename, 'r') as fin:
            data = json.load(fin)
            game_state = GameState.load(data)
            print(game_state.save())
            player_types = {}
            for player, player_data in zip(game_state.players, data['players']):
                kind = player_data['kind']
                kind = getattr(all_player_types, kind)
                player_types[player] = kind
            return GameServer(player_types=player_types, game_state=game_state)

    def save(self):
        filename = 'uno.json'
        data = self.save_to_dict()
        with open(filename, 'w') as fout:
            json.dump(data, fout, indent=4)

    def save_to_dict(self):
        data = self.game_state.save()
        for player_index, player in enumerate(self.player_types.keys()):
            player_interaction = self.player_types[player]
            data['players'][player_index]['kind'] = self.player_types[player].__name__
        return data

    @classmethod
    def get_players(cls):
        player_count = cls.request_player_count()

        player_types = {}
        for p in range(player_count):
            name, kind = cls.request_player()
            player = Player(name, Hand())
            player_types[player] = kind
        return player_types

    @classmethod
    def new_game(cls, player_types: dict):
        # Shuffle the deck and deal the top card
        deck = Deck(cards=None)
        top = deck.draw_card()
        game_state = GameState(list(player_types.keys()), deck, top)

        # Each player starts with 6 cards
        for _ in range(cls.INITIAL_HAND_SIZE):
            for p in player_types.keys():
                p.hand.add_card(deck.draw_card())

        print(game_state.save())

        res = cls(player_types, game_state)
        return res

    def run(self):
        current_phase = GamePhase.CHOOSE_CARD
        while current_phase != GamePhase.GAME_END:
            # 1. Possible code, but with more copy-paste
            # match current_phase:
            #     case CHOOSE_CARD:
            #         current_phase = choose_card_phase()
            #     case DRAW_EXTRA:
            #         current_phase = draw_extra_phase()
            #     case GAME_END:
            #         current_phase = game_end_phase()

            # 2. Suggested code - minimal and still easy to read
            phases = {
                GamePhase.CHOOSE_CARD: self.choose_card_phase,
                GamePhase.DRAW_EXTRA: self.draw_extra_phase,
                GamePhase.NEXT_PLAYER: self.next_player_phase,
                GamePhase.DECLARE_WINNER: self.declare_winner_phase,
            }
            current_phase = phases[current_phase]()

            # 3. Can use naming convection to not declare phases explicitly,
            # but this may introduce errors later.
            # Looks over-engineered and is hard to read w/o comments.
            # current_phase = getattr(self, current_phase.name.lower() + "_phase")()

    def declare_winner_phase(self) -> GamePhase:
        print(f"{self.game_state.current_player()} is the winner!")
        return GamePhase.GAME_END

    def next_player_phase(self) -> GamePhase:
        if not self.game_state.current_player().hand.cards:
            return GamePhase.DECLARE_WINNER
        self.game_state.next_player()
        print(f"=== {self.game_state.current_player()}'s turn")
        return GamePhase.CHOOSE_CARD

    def draw_extra_phase(self) -> GamePhase:
        current_player = self.game_state.current_player()
        card = self.game_state.draw_card()
        print(f"Player {current_player} draws {card}")
        self.inform_all("inform_card_drawn", current_player)

        if card.can_play_on(self.game_state.top):
            print(f"Игрок {current_player} может сыграть вытянутую карту")
            if self.player_types[current_player].choose_to_play(
                self.game_state.top, card
            ):
                print(f"Играк {current_player.name} играет {card}")
                current_player.hand.remove_card(card)
                self.game_state.top = card
                self.inform_all("inform_card_played", current_player, card)
            else:
                print(f"Игрок решает не играть карту {card}")

        return GamePhase.NEXT_PLAYER

    def choose_card_phase(self) -> GamePhase:
        current_player = self.game_state.current_player()
        playable_cards = current_player.hand.playable_cards(self.game_state.top)

        print(
            f"Игрок {current_player.name} с рукой {current_player.hand} может сыграть {playable_cards} поверх {self.game_state.top}"
        )

        if not playable_cards:
            print(f"Игрок {current_player.name} не может сыграть какую-либо карту")
            return GamePhase.DRAW_EXTRA

        card = self.player_types[current_player].choose_card(
            current_player.hand, self.game_state.top
        )

        if card is None:
            print(f"Игрок {current_player.name} пропускает ход")
            return GamePhase.DRAW_EXTRA

        assert card in playable_cards
        print(f"Игрок {current_player.name} играет {card}")
        current_player.hand.remove_card(card)
        self.game_state.top = card
        self.inform_all("inform_card_drawn", current_player)
        return GamePhase.NEXT_PLAYER

    def inform_all(self, method: str, *args, **kwargs):
        for p in self.player_types.values():
            getattr(p, method)(*args, **kwargs)

    @staticmethod
    def request_player_count() -> int:
        while True:
            try:
                player_count = int(input("Сколько игроков?"))
                if 2 <= player_count <= 10:
                    return player_count
            except ValueError:
                pass
            print("Пожалуйста, введите число от 2 до 10")

    @staticmethod
    def request_player() -> (str, PlayerInteraction):
        """Возвращает имя и тип игрока."""

        """Разрешенные типы игроков из PlayerInteraction."""
        # Getting all names of subclasses of PlayerInteraction from  all_player_types
        player_types = []
        for name, cls in inspect.getmembers(all_player_types):
            if inspect.isclass(cls) and issubclass(cls, PlayerInteraction):
                player_types.append(cls.__name__)
        player_types_as_str = ', '.join(player_types)

        while True:
            name = input("Как зовут игрока?")
            if name.isalpha():
                break
            print("Имя должно быть одним словом")

        while True:
            try:
                kind = input(f"Какой тип игрока({player_types_as_str})?")
                kind = getattr(all_player_types, kind)
                break
            except AttributeError:
                print(f"Allowed player types are: {player_types_as_str}")
        return name, kind


def __main__():
    load_from_file = False
    if load_from_file:
        server = GameServer.load_game()
        server.save()
    else:
        server = GameServer.new_game(GameServer.get_players())
    server.run()


if __name__ == "__main__":
    __main__()