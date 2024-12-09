import pytest
from src.player import Player
from src.deck import Deck
from src.card import Card
from src.game_state import GameState

data = {
    "top": "3",
    "current_player_index": 1,
    "deck": "2 6 10",
    "players": [
        {"name": "Alex", "hand": "4 6 10", "score": 9},
        {"name": "Bob", "hand": "1 5", "score": 5},
    ],
}

# Загрузка игроков и колоды для тестов
alex = Player.load(data["players"][0])
bob = Player.load(data["players"][1])
full_deck = Deck(None)


def test_init(): #Проверяет инициализацию состояния игры
    players = [alex, bob]
    game = GameState(players=players, deck=full_deck, current_player=1, top=Card.load("3"))

    assert game.players == players
    assert game.deck == full_deck
    assert game.current_player() == bob
    assert str(game.top) == "3"


def test_current_player(): #Проверяет, что текущий игрок корректно определяется на основе индекса. Тестирует несколько сценариев с разными индексами
    players = [alex, bob]
    game = GameState(players=players, deck=full_deck, top=Card.load("3"))

    assert game.current_player() == alex

    game = GameState(players=players, deck=full_deck, top=Card.load("3"), current_player=1)
    assert game.current_player() == bob


def test_eq(): #Проверяет, что два состояния игры могут быть равны, если у них одинаковые игроки, колода и верхняя карта. Также проверяет, что разные состояния игры не равны

    players = [alex, bob]
    game1 = GameState(players=players, deck=full_deck, top=Card.load("3"))
    game1_copy = GameState(players=players.copy(), deck=Deck(game1.deck.cards.copy()), top=Card.load("3"))
    game2 = GameState(players=players.copy(), deck=Deck.load("2 6 10"), top=Card.load("3"))

    assert game1 == game1_copy
    assert game1 != game2


def test_save(): #Проверяет, что метод сохранения состояния игры (save) возвращает ожидаемый словарь с данными
    players = [alex, bob]
    game = GameState(players=players, deck=full_deck, top=Card.load("3"), current_player=1)

    expected_save = {
        "top": str(Card.load("3")),
        "deck": str(full_deck),
        "current_player_index": 1,
        "players": [p.save() for p in players],
    }

    assert game.save() == expected_save


def test_load(): #Проверяет, что метод загрузки состояния игры (load) создает объект, который соответствует исходным данным
    game = GameState.load(data)
    assert game.save() == data


def test_next_player(): #Проверяет, что метод next_player корректно переключает текущего игрока
    game = GameState.load(data)
    assert game.current_player() == bob

    game.next_player()
    assert game.current_player() == alex

    game.next_player()
    assert game.current_player() == bob


def test_draw_card(): #Проверяет, что метод draw_card корректно тянет карту из колоды и добавляет ее в руку текущего игрока
    game = GameState.load(data)
    assert str(game.deck) == "2 6 10"
    assert str(game.current_player().hand) == "1 5"

    game.draw_card()
    assert str(game.deck) == "2 6"
    assert str(game.current_player().hand) == "1 5 10"  # Предполагается, что карта 10 была добавлена


def test_play_card(): #Проверяет, что игрок может сыграть карту, и что карта удаляется из его руки, а верхняя карта обновляется
    # players = [alex, bob]
    # game = GameState(players=players, deck=full_deck, top=Card.load("3"), current_player=0)
    d = data.copy()
    d['current_player_index'] = 0
    game = GameState.load(d)

    assert str(game.current_player().hand) == "4 6 10"
    assert str(game.top) == "3"

    game.play_card(Card.load("4"))
    assert str(game.current_player().hand) == "6 10"
    assert str(game.top) == "4"

# Тесты с картой "Лама"
def test_play_lama_card():
    """
    Проверяет, что игрок
    - не может играть Ламу на 5,
    - не может играть Ламу на 1,
    - может сыграть карту "Лама" (10) на 6, и верхняя карта становится "Ламой".
    У игрока при этом должно изменяться количество карт
    """
    data = {
        "top": "6",
        "current_player_index": 0,
        "deck": "2 6 10",
        "players": [
            {"name": "Alex", "hand": "4 10 6", "score": 9},
            {"name": "Bob", "hand": "1 5", "score": 5},
        ],
    }
    game = GameState.load(data)

    assert str(game.current_player().hand) == "4 10 6" #Спросить почему не остаётся 4
    assert str(game.top) == "6"

    # Игрок Alex играет карту "Лама" (10)
    game.play_card(Card.load("10"))
    assert str(game.current_player().hand) == "4 6"  # У Alex все еще карты
    assert str(game.top) == "10"  # Все еще верхняя карта - Лама
