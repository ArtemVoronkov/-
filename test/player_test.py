from src.hand import Hand
from src.player import Player


def test_init():
    h = Hand.load("2 5 10")
    p = Player(name="Misha", hand=h, score=10)
    assert p.name == "Misha"
    assert p.hand == h
    assert p.score == 10


def test_str():
    h = Hand.load("2 5 10")
    p = Player(name="Misha", hand=h, score=20)
    assert str(p) == "Misha(20): 2 5 10"


def test_save():
    h = Hand.load("2 5 10")
    p = Player(name="Misha", hand=h, score=20)
    assert p.save() == {"name": "Misha", "score": 20, "hand": "2 5 10"}


def test_eq():
    h1 = Hand.load("2 5 10")
    h2 = Hand.load("2 5 10")
    p1 = Player(name="Misha", hand=h1, score=10)
    p2 = Player(name="Misha", hand=h2, score=10)
    assert p1 == p2
    h1 = Hand.load("2 5 10")
    h2 = Hand.load("1 3 6")
    p1 = Player(name="Misha", hand=h1, score=10)
    p2 = Player(name="Petr", hand=h2, score=10)
    assert p1 != p2


def test_load():
    data = {"name": "Misha", "score": 10, "hand": "2 5 10"}
    h = Hand.load("2 5 10")
    p_expected = Player(name="Misha", hand=h, score=10)
    p = Player.load(data)
    assert p == p_expected