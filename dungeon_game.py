import tkinter as tk
from tkinter import messagebox
import random

class Room:
    def __init__(self, description, level):
        self.description = description
        self.level = level
        self.monster = self.generate_monster()
        self.item = self.generate_item()

    def generate_monster(self):
        if random.random() > 0.5:
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

    def __str__(self):
        return f"{self.name}: {self.health} HP, {self.mana} MP, Инвентарь: {', '.join(str(item) for item in self.inventory) if self.inventory else 'пусто'}"

class Monster:
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage
        self.health = random.randint(10, 30)

    def attack(self, player):
        player.take_damage(self.damage)
        return f"{self.name} атакует и наносит {self.damage} урона!"

    def __str__(self):
        return f"Монстр {self.name}, Здоровье: {self.health}"

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
        return f"Вы использовали {self.name}, восстановлено {self.heal_amount} здоровья."

    def __str__(self):
        return f"{self.name} (+{self.heal_amount} здоровья)"

class GameOver(Exception):
    pass

class Game:
    def __init__(self, root):
        self.root = root
        self.player = None
        self.floors = []
        self.current_floor = 0
        self.current_room = 0
        self.total_floors = 5
        self.rooms_per_floor = 5

        # UI Elements
        self.text_area = None
        self.health_label = None
        self.mana_label = None
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Подземелье")
        self.text_area = tk.Text(self.root, height=15, width=50, state=tk.DISABLED)
        self.text_area.grid(row=0, column=0, columnspan=3)

        tk.Button(self.root, text="Вперед", command=lambda: self.move(1)).grid(row=1, column=0)
        tk.Button(self.root, text="Осмотреть", command=self.inspect_room).grid(row=1, column=1)
        tk.Button(self.root, text="Атака", command=lambda: self.battle("attack")).grid(row=2, column=0)
        tk.Button(self.root, text="Заклинание", command=lambda: self.battle("spell")).grid(row=2, column=1)
        tk.Button(self.root, text="Бег", command=lambda: self.battle("run")).grid(row=2, column=2)

        self.health_label = tk.Label(self.root, text="HP: 100")
        self.health_label.grid(row=3, column=0)
        self.mana_label = tk.Label(self.root, text="MP: 50")
        self.mana_label.grid(row=3, column=1)

    def start(self, player_name):
        self.player = Player(player_name)
        self.floors.append(self.generate_floor(1))
        self.display_message(f"Добро пожаловать, {self.player.name}!")
        self.display_room()

    def generate_floor(self, floor_number):
        return [Room(f"Комната {i+1} этажа {floor_number}", level=floor_number) for i in range(self.rooms_per_floor)]

    def move(self, direction):
        # Проверяем, есть ли монстр в текущей комнате
        current_room = self.floors[self.current_floor][self.current_room]
        if current_room.monster is not None:  # Если монстр не побежден
            self.display_message("В комнате еще есть монстр! Победите его перед переходом.")
            return

        # Переход в следующую комнату
        self.current_room += direction
        if self.current_room >= self.rooms_per_floor:
            self.current_room = 0
            self.current_floor += 1
            if self.current_floor < self.total_floors:
                self.floors.append(self.generate_floor(self.current_floor + 1))
                self.display_message(f"Вы переходите на этаж {self.current_floor + 1}.")
            else:
                messagebox.showinfo("Победа!", "Вы прошли всё подземелье! Поздравляем!")
                self.root.quit()
        self.display_room()

    def inspect_room(self):
        current_room = self.floors[self.current_floor][self.current_room]
        if current_room.item:
            self.player.inventory.append(current_room.item)
            self.display_message(f"Вы нашли: {current_room.item}")
            current_room.item = None
        else:
            self.display_message("Здесь ничего нет.")

    def battle(self, action):
        current_room = self.floors[self.current_floor][self.current_room]
        monster = current_room.monster
        if not monster:
            self.display_message("В комнате нет монстра.")
            return

        if action == "attack":
            monster.health -= 10
            self.display_message(f"Вы нанесли 10 урона монстру {monster.name}.")
        elif action == "spell" and self.player.mana >= 10:
            monster.health -= 20
            self.player.mana -= 10
            self.display_message(f"Вы использовали заклинание! Урон 20. Осталось маны: {self.player.mana}.")
        elif action == "run":
            self.display_message("Вы сбежали из комнаты!")
            return
        else:
            self.display_message("Недостаточно маны для заклинания.")

        if monster.health > 0:
            result = monster.attack(self.player)
            self.display_message(result)
            self.update_status()
        else:
            self.display_message(f"Вы победили монстра {monster.name}!")
            current_room.monster = None

    def display_room(self):
        current_room = self.floors[self.current_floor][self.current_room]
        self.display_message(str(current_room))

    def display_message(self, message):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.config(state=tk.DISABLED)

    def update_status(self):
        self.health_label.config(text=f"HP: {self.player.health}")
        self.mana_label.config(text=f"MP: {self.player.mana}")

if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    game.start("Игрок")
    root.mainloop()
