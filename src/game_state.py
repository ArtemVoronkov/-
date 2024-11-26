from src.player import Player  # Импортируйте класс Player
from src.deck import Deck  # Импортируйте класс Deck
from src.card import Card  # Импортируйте класс Card

class GameState:
    def __init__(
            self, players: list[Player], deck: Deck, top: Card, current_player: int = 0
    ):
        self.players: list[Player] = players
        self.deck: Deck = deck
        self.top: Card = top
        self.__current_player: int = current_player

    @property
    def current_player_index(self):   #Возвращает индекс текущего игрока
        return self.__current_player

    def current_player(self) -> Player:  #Метод, возвращающий текущего игрока
        return self.players[self.__current_player]

    def __eq__(self, other): #Метод для сравнения двух объектов GameState. Он проверяет, равны ли списки игроков, колоды, верхняя карта и индекс текущего игрока
        if self.players != other.players:
            return False
        if self.deck != other.deck:
            return False
        if self.top != other.top:
            return False
        if self.__current_player != other.__current_player:
            return False
        return True

    def save(self) -> dict: #Метод, который возвращает состояние игры в виде словаря, что может быть полезно для сохранения игры
        return {
            "top": str(self.top),
            "deck": str(self.deck),
            "current_player_index": self.__current_player,
            "players": [p.save() for p in self.players],
        }

    @classmethod
    def load(cls, data: dict):
        """
        data = {
            'top': '3',
            'current_player_index': 1,
            'deck': '2 6 10',
            'players': [
                {
                    'name': 'Alex',
                    'hand': '3 6 10',
                    'score': 5
                },
                {
                    'name': 'Bob',
                    'hand': '1 5',
                    'score': 1
                },
            ]
        }
        """
        players = [Player.load(d) for d in data["players"]]

        return cls(
            players=players,
            deck=Deck.load(data["deck"]),
            top=Card.load(data["top"]),
            current_player=int(data["current_player_index"]),
        )

    def next_player(self): #Метод, который переходит к следующему игроку
        """Ход переходит к следующему игроку."""
        n = len(self.players)
        self.__current_player = (self.__current_player + 1) % n

    def draw_card(self) -> Card: #Метод, позволяющий текущему игроку взять карту из колоды
        """Текущий игрок берет карту из колоды."""
        if not self.deck.cards:  # Проверяем, что в колоде есть карты
            print("Колода пуста, нельзя взять карту.")
            return None
        card = self.deck.draw_card()
        self.current_player().hand.add_card(card)
        return card

    def play_card(self, card: Card): #Метод, который позволяет текущему игроку сыграть карту
        """Карта card от текущего игрока переходит в top."""
        if card.can_play_on(self.top):  # Проверяем, можно ли сыграть карту
            self.current_player().hand.remove_card(card)
            self.top = card
        else:
            print(f"{card} нельзя сыграть на {self.top}.")

    def deal_cards(self, num_cards: int = 6): #Метод для раздачи карт игрокам
        """Раздача карт игрокам."""
        for _ in range(num_cards):
            for player in self.players:
                if self.deck.cards:  # Проверяем, что в колоде есть карты
                    player.hand.add_card(self.deck.draw_card())

    def start_game(self): #Метод для начала игры, который перемешивает колоду и раздает карты
        """Начало игры."""
        self.deck.shuffle()
        self.deal_cards()
        self.top = self.deck.draw_card()  # Перевернуть верхнюю карту
        print(f"Начальная карта: {self.top}")

    def player_action(self): #Метод, который обрабатывает действия текущего игрока, запрашивая у него выбор действия (играть, взять или выйти)
        """Обработка действий текущего игрока."""
        current = self.current_player()
        print(f"{current.name}: {current.hand}")

        while True:
            action = input(f"{current.name}, выберите действие (играть/взять/выйти): ").strip().lower()
            if action == "играть":
                card_value = input("Введите значение карты, которую хотите сыграть: ")
                try:
                    card = Card(int(card_value))  # Пробуем создать карту
                    if card in current.hand.cards:
                        self.play_card(card)
                        print(f"{current.name} играет {card}")
                        break
                    else:
                        print("Такой карты нет в руке.")
                except ValueError:
                    print("Недопустимое значение карты.")
            elif action == "взять":
                self.draw_card()
                print(f"{current.name} берет карту.")
                break
            elif action == "выйти":  # Убираем карты игрока
                print(f"{current.name} выходит из раунда.")
                break
            else:
                print("Неверное действие. Попробуйте снова.")