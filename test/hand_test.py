import random

from src.card import Card
from src.hand import Hand

cards = [Card(3), Card(1), Card(6)]

def test_init():
    d = Hand(cards=cards)
    assert d.cards == cards

def test_save():
    d = Hand(cards=cards)
    assert d.save() == '3 1 6'

    d = Hand(cards=[])
    assert d.save() == ''

def test_load():
    d = Hand.load('3 1 6')
    expected_deck = Hand(cards)
    assert d == expected_deck

def test_score():
    h = Hand.load('3 1 6')
    assert h.score() == 10

    h = Hand.load('5 4')
    assert h.score() == 9

def test_add_card():
    h = Hand.load('3 1 6')
    h.add_card(Card.load('6'))
    assert repr(h) == '3 1 6 6'

    h.add_card(Card.load('4'))
    assert repr(h) == '3 1 6 6 4'

def test_remove_card():
    h = Hand.load('3 1 6 6 4')
    c = Card.load('6')
    h.remove_card(c)
    assert repr(h) == '3 1 6 4'