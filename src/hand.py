import typing

from src.card import Card


class Hand:
    def __init__(self, cards:  list[Card] | None = None):
        if cards is None:
            cards = []
        self.cards: list[Card] = cards

    def __repr__(self):
        return self.save()


    def save(self) -> str:
        """Convert deck to string in '3 1 6' format."""
        scards = [c.save() for c in self.cards]         # ['3', '1', '6']
        s = ' '.join(scards)
        return s

    def __eq__(self, other):
        if isinstance(other, str):
            other = Hand.load(other)
        return self.cards == other.cards


    def add_card(self, card: Card):
        self.cards.append(card)

    @classmethod
    def load(cls, text: str) -> typing.Self:
        """Convert string in '3 1 6' format to Deck. Return deck."""
        cards = [Card.load(s) for s in text.split()]
        return cls(cards=cards)

    def remove_card(self, card: Card):
        self.cards.remove(card)

    def score(self):
        """Штрафные очки"""
        unique_card_numbers = set()  # Множество для хранения уникальных номеров карт
        res = 0
        for c in self.cards:
            if c.number not in unique_card_numbers:  # Если номер карты еще не встречался
                res += c.score()  # Добавляем штрафные очки
                unique_card_numbers.add(c.number)  # Добавляем номер карты в множество
        return res

    def playable_cards(self, top_card: Card) -> [Card]:
        """Какие карты можно сыграть"""
        return [c for c in self.cards if c.can_play_on(top_card)]