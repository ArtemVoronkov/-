import pytest

from src.card import Card


def test_init():
    c = Card(3)
    assert c.number == 3

    c = Card(10)
    assert c.number == 10

def test_save():
    c = Card(3)
    assert repr(c) == '3'
    assert c.save() == '3'

    c = Card(10)
    assert repr(c) == '10'
    assert c.save() == '10'

def test_eq():
    c1 = Card(3)
    c2 = Card(3)
    c3 = Card(1)
    c4 = Card(2)
    c5 = Card(10)
    c6 = Card(10)

    assert c1 == c2
    assert c1 != c3
    assert c2 != c4
    assert c1 != c5
    assert c5 == c6

def test_load():
    s = '3'
    c = Card.load(s)
    assert c == Card(3)

    s = '10'
    c = Card.load(s)
    assert c == Card(10)

def test_divzero():
    # пример теста с ловлей исключения
    with pytest.raises(ZeroDivisionError):
        x = 2 / 0
        # y = 3 / 15

def test_validation():
    with pytest.raises(ValueError):
        Card('3')

def test_play_on():
    c1 = Card.load('1')
    c2 = Card.load('2')
    c3 = Card.load('3')
    c4 = Card.load('4')
    c5 = Card.load('10')

    assert c1.can_play_on(c1)
    assert c2.can_play_on(c1)
    assert c2.can_play_on(c2)
    assert c5.can_play_on(c5)
    assert c1.can_play_on(c5)
    assert not c3.can_play_on(c1)
    assert not c4.can_play_on(c1)
    assert not c3.can_play_on(c5)
    assert not c4.can_play_on(c5)

def test_all_cards():
    cards = Card.all_cards(numbers=[5, 2, 6, 10])
    # print(cards)
    expected_cards = [
        Card.load('5'),
        Card.load('2'),
        Card.load('6'),
        Card.load('10'),
    ]
    assert cards == expected_cards


def test_score():
    c = Card(6)
    assert 6 == c.score()

    c = Card(5)
    assert 5 == c.score()

    c = Card(10)
    assert 10 == c.score()
