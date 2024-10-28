import random

from src.card import Card
from src.deck import Deck

cards = [Card(3), Card(5), Card(6)]


def test_init():
    d = Deck(cards=cards)
    assert d.cards == cards


def test_init_shuffle():
    """Проверяем, что карт столько же, но они в другом порядке."""
    full_deck1 = Deck(None)
    full_deck2 = Deck(None)
    assert full_deck1.cards != full_deck2.cards


def test_save():
    d = Deck(cards=cards)
    assert d.save() == "3 5 6"

    d = Deck(cards=[])
    assert d.save() == ""


def test_load():
    d = Deck.load("3 5 6")
    expected_deck = Deck(cards)

    assert d == expected_deck


def test_draw_card():
    d1 = Deck.load("3 5 6")
    d2 = Deck.load("3 5")
    c = d1.draw_card()
    assert c == Card.load("6")
    assert d1 == d2


def test_shuffle_1():
    test_cards = Card.all_cards(numbers=[2, 4, 6])
    deck = Deck(cards=test_cards)
    deck_list = [deck.save()]
    for i in range(5):
        deck.shuffle()
        s = deck.save()
        assert s not in deck_list
        deck_list.append(s)


def test_shuffle_2():
    random.seed(3)

    test_cards = Card.all_cards(numbers=[4, 2, 6])
    deck = Deck(cards=test_cards)
    deck_list = [deck.save()]

    deck.shuffle()
    assert deck.save() == "2 6 4"

    deck.shuffle()
    assert deck.save() == "2 4 6"

    deck.shuffle()
    assert deck.save() == "4 2 6"