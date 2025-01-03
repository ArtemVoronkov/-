from src.card import Card
from src.hand import Hand
from src.player import Player

from src.Interactions import PlayerInteraction


class Bot(PlayerInteraction):
    @classmethod
    def choose_card(
        cls, hand: Hand, top: Card, hand_counts: list[int] | None = None
    ) -> Card:
        """
        Принимает решение, какую карту с руки играть.
        Возвращает карту или None, если нельзя играть карту с руки.
        """
        playable_cards = [card for card in hand.cards if card.can_play_on(top)]
        if playable_cards:
            return playable_cards[0]
        else:
            return None

    @classmethod
    def choose_to_play(cls, top: Card, drawn: Card) -> bool:
        """
        Принимает решение играть или не играть взятую из колоды карту.
        Бот всегда играет карту.
        """
        return True

    @classmethod
    def inform_card_drawn(cls, player: Player):
        """
        Сообщает, что игрок взял карту.
        """
        pass

    @classmethod
    def inform_card_played(cls, player: Player, card: Card):
        """
        Сообщает, что игрок сыграл карту.
        """
        pass