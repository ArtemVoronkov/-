"""Карты Lama"""
from typing import Self


# Lama = 10
class Card:
    Lama = 10
    NUMBERS = list(range(1, 7)) + [10]
    count_cards_of_one_type = 8
    count_of_types = 7


    def __init__(self, number: int):
        if number not in Card.NUMBERS:
            raise ValueError
        self.number = number

    def __repr__(self):
        # '3'
        return f'{self.number}'

    def __eq__(self, other):
        if isinstance(other, str):
            other = Card.load(other)
        return self.number == other.number

    def save(self):
        return repr(self)


    @staticmethod
    def load(text: str):
        """From '3' to Card(3)."""
        return Card(number=int(text[:2]))

    """Можно ли играть карту self на карту other."""
    def can_play_on(self, other: Self) -> bool:
        #Метод возвращает логическое значение, указывающее, можно ли сыграть текущую карту (self) на другую карту (other).

        if self.number == other.number or self.number == other.number + 1:
            return True
        if self.number == Card.Lama:
            return other.number == 6 or other.number == Card.Lama
        if other.number == Card.Lama:
            return self.number == 1 or self.number == Card.Lama
        return False


    @staticmethod
    def all_cards(numbers: None | list[int] = None):
        if numbers is None:
            numbers = Card.NUMBERS
        cards = [
            Card(number=num)
            for _ in range(Card.count_cards_of_one_type)
            for num in numbers
        ]
        return cards


    def score(self):
        """Штрафные очки за карту."""
        return self.number