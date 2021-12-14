'''
This is a game where a hero will fight a monster, taking turns, until one has 0 or less hit points. Each attack will do a random amount of damage based on the entity's strength, and will have a random chance of success based on the defender's dexterity. Fight until death.

Nouns: game, hero, monster, attacker, defender, entity
Adjectives: strength, dexterity, hp, dead, turn
Verbs: fight, attack

future: weapons, armor, treasure, inventory, accuracy, experience, stat increase
'''

from random import randint, choice

class Entity:
    def __init__(self, name, character_class, strength=18, attack=18, dexterity=18, defense=18, health=100, inventory=None, equip=None):
        self.name = name
        self.character_class = character_class
        self.strength = strength
        self.attack = attack
        self.dexterity = dexterity
        self.defense = defense
        self.health = health 
        self.inventory = [] if inventory is None else inventory # ternery operator: mandatory in Python to prevent shared inventory
        self.equip = [] if equip is None else equip
    
    def alive(self):
        return self.health > 0

    def dead(self):
        return self.health <= 0

class Barbarian(Entity): # A Hero is a kind of Entity
    def __init__(self, name, strength=18, attack=18, dexterity=18, defense=18, health=100):
        super().__init__(
            name, 'barbarian', strength, attack, dexterity, defense, health, #stats
            [HealthPotion(), ManaPotion()], #inv
            [AmuletOfStrength(), Battleaxe()] #equip
        )

class Zombie(Entity): # A Monster is a kind of Entity
    def __init__(self, name, strength=18, attack=18, dexterity=18, defense=18, health=100):
        super().__init__(name, 'zombie', strength, attack, dexterity, defense, health,
            [],
            []
        )

class Item:
    def __init__(self, item_type):
        self.item_type = item_type

    def modifer_to_str(self, mods):
        return ', '.join([f'{k} {v}' for k, v in mods.items()])

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
        self.modifier = {
            'strength': 5,
            'health': -2
        }

    def __repr__(self):
        return 'AmuletOfStrength()'

    def __str__(self):
        return f'{self.item_type}: {self.name}, {self.modifer_to_str(self.modifier)}'

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
        self.modifier = {'strength': 5}

    def __repr__(self):
        return 'Battleaxe()'

    def __str__(self):
        return f'{self.item_type}: {self.name}, +{self.modifier["strength"]} damage'

class Map():
    def __init__(self, width, height):
        self.data = []
        for y in range(height):
            row = []
            for x in range(width):
                if x == width - 1 or x == 0 or y == 0 or y == height - 1:
                    row.append('#')
                else:
                    row.append('.')
            self.data.append(row)

    def place_entity(self, entity, coord='random'):
        if coord == 'random':
            coord_list = []
            for r in range(len(self.data)):
                for c in range(len(self.data[r])):
                    if self.data[r][c] == '.':
                        coord_list.append((c, r))
            coord = choice(coord_list)
        x, y = coord
        self.data[y][x] = entity
        return coord 
    
    def __str__(self):
        text = '\n'
        for r in self.data:
            for c in r:
                text += c + ' '
            text += '\n'
        return text

    # def __repr__(self):
    #     for x in self.layout:
    #         str(x)

    # def __str__(self):
        
class Game:
    def __init__(self):
        self.player_list = [
            Barbarian('Conan'),
            Zombie('Zed')
        ]
        self.map = Map(16, 9)
        self.hero_coord = self.map.place_entity('@', (5, 5)) # place hero
        self.monster_coord = self.map.place_entity('Z') # place zombie
        print(f'hero at {self.hero_coord}')
        print(f'monster at {self.monster_coord}')
        # print(self.player_list[0].inventory)
        # print(self.player_list[0].inventory[0])
        # print(self.player_list[0].inventory[1])
        # print(self.player_list[0].equip)
        # print(self.player_list[0].equip[0])
        # print(self.player_list[0].equip[1])
    
    def play(self):
        while True:
            print(self.map)
            print(self.hero_coord)
            command = input('command: ')
            if command in ['q', 'quit', 'exit', '']:
                break
            self.hero_coord = self.movement_command(self.hero_coord, command)

    def attack(self, attacker, defender):
        base_percent = 50
        chance = base_percent + attacker.dexterity - defender.dexterity
        roll = randint(1, 100)
        if roll < chance:
            damage = randint(1, attacker.strength)
            # damage = attack * (100 / (100 + defense))
            defender.health -= damage
            print(f'The {attacker.character_class} {attacker.name} hits the {defender.character_class} {defender.name} for {damage}!')
        else:
            print(f'The {attacker.character_class} {attacker.name} misses the {defender.character_class} {defender.name}!')

    def fight(self):
        a = self.player_list[0]
        b = self.player_list[1]

        while a.alive() and b.alive():
            self.attack(a, b)
            self.attack(b, a)
            print(a.name, a.health)
            print(b.name, b.health)

        if a.dead() and b.dead():
            print(f'It\'s a massacre! {a.name} and {b.name} are both dead!')
        elif a.dead():
            print(f'Our hero {a.name} has been slain! Game over.')
        else:
            print(f'Huzzah! {a.name} has slain {b.name}!')
            

        print(a.name, a.health)
        print(b.name, b.health)
        exit()

# def map():
#     layout = [
#         ['x', 'x', 'x'],
#         ['x', 'x', 'x'],
#         ['x', 'x', 'x']
#     ]
#     print(layout)
#     for r in layout:
#         print(' '.join(r))

# def map2():
#     x = 5
#     y = 6
#     layout = []
#     print(layout)
#     for i in range(x):
#         layout.append(['x'] * y)
#     for r in layout:
#         print(' '.join(r))
#     print(layout)

    # function to take a direction command to move character (arrow keys, wasd, nsew)
    def movement_command(self, hero_coord, command):
        
        command = command.upper()
        dest_coord_x, dest_coord_y = hero_coord

        if command in ['UP', 'W', 'NORTH']:
            dest_coord_y -= 1
        elif command in ['DOWN', 'S', 'SOUTH']:
            dest_coord_y += 1
        elif command in ['LEFT', 'A', 'WEST']:
            dest_coord_x -= 1
        elif command in ['RIGHT', 'D', 'EAST']:
            dest_coord_x += 1
        else:
            print('invalid command')

        destination = dest_coord_x, dest_coord_y
        if self.collision_check(destination):
            self.update_map(destination, hero_coord)
            return destination
        else:
            return hero_coord

    # function to check for walls or monsters (collision)
    def collision_check(self, destination):
        dest_coord_x, dest_coord_y = destination
        if self.map.data[dest_coord_y][dest_coord_x] == 'Z':
            self.fight()
        return self.map.data[dest_coord_y][dest_coord_x] == '.'

    # function to move character
    def update_map(self, destination, hero_coord):
        old_coord_x, old_coord_y = hero_coord
        self.map.data[old_coord_y][old_coord_x] = '.'
        self.map.place_entity('@', destination)

# damage formula incorporating stat bonuses

game = Game()
game.play()