import random

class Room:
    def __init__(self, description, level):
        self.description = description
        self.level = level
        self.monster = self.generate_monster()
        self.item = self.generate_item()

    def generate_monster(self):
        if random.random() > 0.5:  # 50% шанс появления монстра
            return Monster("Гоблин", random.randint(5, 15))
        return None

    def generate_item(self):
        items = [None, Weapon("Меч", 10), Potion("Зелье здоровья", 20)]
        return random.choice(items)

    def __str__(self):
        return f"Комната: {self.description}, Уровень: {self.level}. " \
               f"{'Здесь есть монстр!' if self.monster else 'Пусто.'} " \
               f"{'Вы нашли предмет: ' + str(self.item) if self.item else ''}"


class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.mana = 50
        self.inventory = []
        self.level = 1
        self.experience = 0

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            raise GameOver(f"{self.name} погиб!")

    def heal(self, amount):
        self.health = min(100, self.health + amount)

    def add_experience(self, exp):
        self.experience += exp
        if self.experience >= self.level * 10:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.health = 100
        self.mana += 20
        print(f"Поздравляем, {self.name} достиг уровня {self.level}!")

    def __str__(self):
        return f"{self.name}: {self.health} HP, {self.mana} MP, Уровень: {self.level}, Инвентарь: {self.inventory}"


class Monster:
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage
        self.health = random.randint(10, 30)

    def attack(self, player):
        player.take_damage(self.damage)
        print(f"{self.name} атакует! Урон: {self.damage}")

    def __str__(self):
        return f"Монстр {self.name}, Урон: {self.damage}, Здоровье: {self.health}"


class Weapon:
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage

    def __str__(self):
        return f"{self.name} (+{self.damage} урона)"


class Potion:
    def __init__(self, name, heal_amount):
        self.name = name
        self.heal_amount = heal_amount

    def use(self, player):
        player.heal(self.heal_amount)
        print(f"Вы использовали {self.name}, восстановлено {self.heal_amount} здоровья.")

    def __str__(self):
        return f"{self.name} (+{self.heal_amount} здоровья)"


class Game:
    def __init__(self):
        self.player = None
        self.floors = []
        self.current_floor = 0
        self.current_room = 0
        self.total_floors = 5
        self.rooms_per_floor = 5

    def generate_floor(self, floor_number):
        return [Room(f"Комната {i+1}, этаж {floor_number}", level=floor_number) for i in range(self.rooms_per_floor)]

    def start(self, player_name):
        self.player = Player(player_name)
        print(f"Добро пожаловать, {self.player.name}!")
        self.floors.append(self.generate_floor(1))
        self.main_loop()

    def main_loop(self):
        while self.current_floor < self.total_floors:
            current_room = self.floors[self.current_floor][self.current_room]
            print(current_room)

            if current_room.monster:
                self.battle(current_room.monster)

            command = input("Ваш ход (вперед/осмотреть): ").lower()
            if command == "вперед":
                self.move(1)
            elif command == "осмотреть":
                print(f"Вы нашли: {current_room.item}")
                if current_room.item:
                    self.player.inventory.append(current_room.item)
                    current_room.item = None
            else:
                print("Неизвестная команда.")

        print("Поздравляем, вы прошли все этажи подземелья и победили!")

    def move(self, direction):
        self.current_room += direction
        if self.current_room >= self.rooms_per_floor:  # Переход на новый этаж
            self.current_room = 0
            self.current_floor += 1
            if self.current_floor < self.total_floors:
                print(f"Вы переходите на этаж {self.current_floor + 1}.")
                self.floors.append(self.generate_floor(self.current_floor + 1))
            else:
                print("Вы достигли последнего этажа!")
        elif self.current_room < 0:
            self.current_room = 0
            print("Вы не можете вернуться назад.")

    def battle(self, monster):
        print(f"Сражение началось! {monster}")
        while monster.health > 0 and self.player.health > 0:
            action = input("Атака/Заклинание/Бег: ").lower()
            if action == "атака":
                monster.health -= 10
                print(f"Вы нанесли 10 урона {monster.name}.")
                if monster.health > 0:
                    monster.attack(self.player)
            elif action == "заклинание" and self.player.mana >= 10:
                monster.health -= 20
                self.player.mana -= 10
                print(f"Вы использовали заклинание! Урон: 20. Осталось маны: {self.player.mana}.")
                if monster.health > 0:
                    monster.attack(self.player)
            elif action == "бег":
                print("Вы сбежали!")
                return
            else:
                print("Неизвестное действие.")
        print(f"Вы победили {monster.name}!" if self.player.health > 0 else f"{monster.name} победил вас.")

class GameOver(Exception):
    pass


if __name__ == "__main__":
    try:
        game = Game()
        game.start("Игрок")
    except GameOver as e:
        print(e)
