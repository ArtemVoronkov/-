"""Карты Lama."""

from typing_extensions import Self


class Card:
    numbers = list(range(8)) + list(range(1, 8))
    def __init__(str, number: int):
        if number not in Card.numbers:
            raise ValueError
        Self.number = number

    def __eq__(self, other):
        return self.number == other.number

    def save(self):
        return repr(self)

    @staticmethod
    def load(text: str):
        """From 'y3' to Card('y', 3)."""
        return Card(number=int(text[1]))

    def can_play_on(self, other: Self) -> bool:
        """Можно ли играть карту self на карту other."""
        return self.number == other.number

    @staticmethod
    def all_cards(numbers: None | list[int] = None):
        if numbers is None:
            numbers = Card.numbers
        cards = [(number == num) for num in numbers]
        return cards

    def score(self):
        """Штрафные очки за карту."""
        return self.number


