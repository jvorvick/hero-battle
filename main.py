'''
This is a game where a hero will fight a monster, taking turns, until one has 0 or less hit points. Each attack will do a random amount of damage based on the entity's strength, and will have a random chance of success based on the defender's dexterity. Fight until death.

Nouns: game, hero, monster, attacker, defender, entity
Adjectives: strength, dexterity, hp, dead, turn
Verbs: fight, attack

future: weapons, armor, treasure, inventory, accuracy, experience, stat increase
'''

from random import randint

class Entity:
    def __init__(self, name, character_class, strength=18, dexterity=18, health=100, inventory=None):
        self.name = name
        self.character_class = character_class
        self.strength = strength
        self.dexterity = dexterity
        self.health = health
        self.inventory = [] if inventory is None else inventory # ternery operator: mandatory in Python to prevent shared inventory
    
    def alive(self):
        return self.health > 0

    def dead(self):
        return self.health <= 0

class Barbarian(Entity): # A Hero is a kind of Entity
    def __init__(self, name, strength=18, dexterity=18, health=100):
        super().__init__(name, 'barbarian', strength, dexterity, health, [HealthPotion(), ManaPotion(), AmuletOfStrength(), Battleaxe()])

class Zombie(Entity): # A Monster is a kind of Entity
    def __init__(self, name, strength=18, dexterity=18, health=100):
        super().__init__(name, 'zombie', strength, dexterity, health)

class Item:
    def __init__(self, item_type):
        self.item_type = item_type

    def __repr__(self):
        return f'Item("{self.item_type}")'
    
    def __str__(self):
        return self.item_type

class Potion(Item):
    def __init__(self):
        super().__init__('potion')
    
    def __repr__(self):
        return 'Potion()'

    def __str__(self):
        return self.item_type

class HealthPotion(Potion):
    def __init__(self):
        super().__init__()
        self.color = 'red'
        self.attribute = 'restore +10 health'
    
    def __repr__(self):
        return 'HealthPotion()'

    def __str__(self):
        return f'{self.color} {self.item_type}, {self.attribute}'

class ManaPotion(Potion):
    def __init__(self):
        super().__init__()
        self.color = 'blue'
        self.attribute = 'restore +10 mana'

    def __repr__(self):
        return 'ManaPotion()'

    def __str__(self):
        return f'{self.color} {self.item_type}, {self.attribute}'

class Accessory(Item):
    def __init__(self):
        super().__init__('Accessory')

    def __repr__(self):
        return 'Accessory()'
    
    def __str__(self):
        return self.item_type

class AmuletOfStrength(Accessory):
    def __init__(self):
        super().__init__()
        self.name = 'Amulet of Strength'
        self.attribute = 'strength +5'

    def __repr__(self):
        return 'AmuletOfStrength()'

    def __str__(self):
        return f'{self.item_type}: {self.name}, {self.attribute}'

class Weapon(Item):
    def __init__(self):
        super().__init__('Weapon')
        
    def __repr__(self):
        return 'Weapon()'

    def __str__(self):
        return self.item_type

class Battleaxe(Weapon):
    def __init__(self):
        super().__init__()
        self.name = 'Battleaxe'
        self.attribute = 'attack +5'

    def __repr__(self):
        return 'Battleaxe()'

    def __str__(self):
        return f'{self.item_type}: {self.name}, {self.attribute}'

class Game:
    def __init__(self):
        self.player_list = [
            Barbarian('Conan'),
            Zombie('Zed')
        ]
        print(self.player_list[0].inventory)
        print(self.player_list[0].inventory[0])
        print(self.player_list[0].inventory[1])
        print(self.player_list[0].inventory[2])
        print(self.player_list[0].inventory[3])

    def attack(self, attacker, defender):
        base_percent = 50
        chance = base_percent + attacker.dexterity - defender.dexterity
        roll = randint(1, 100)
        if roll < chance:
            damage = randint(1, attacker.strength)
            defender.health -= damage
            print(f'The {attacker.character_class} {attacker.name} hits the {defender.character_class} {defender.name} for {damage}!')
        else:
            print(f'The {attacker.character_class} {attacker.name} misses the {defender.character_class} {defender.name}!')

    def fight(self):
        a = self.player_list[0]
        b = self.player_list[1]

        # while a.alive() and b.alive():
        #     self.attack(a, b)
        #     self.attack(b, a)
        #     print(a.name, a.health)
        #     print(b.name, b.health)

        # if a.dead() and b.dead():
        #     print(f'It\'s a massacre! {a.name} and {b.name} are both dead!')
        # elif a.dead():
        #     print(f'Our hero {a.name} has been slain! Game over.')
        # else:
        #     print(f'Huzzah! {a.name} has slain {b.name}!')

        # print(a.name, a.health)
        # print(b.name, b.health)

game = Game()
game.fight()