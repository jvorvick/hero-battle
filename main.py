'''
This is a game where a hero will fight a monster, taking turns, until one has 0 or less hit points. Each attack will do a random amount of damage based on the entity's strength, and will have a random chance of success based on the defender's dexterity. Fight until death.

Nouns: game, hero, monster, attacker, defender, entity
Adjectives: strength, dexterity, hp, dead, turn
Verbs: fight, attack

future: weapons, armor, treasure, inventory, accuracy, experience, stat increase
'''

from random import randint

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Sprite:
    def __init__(self, position, graphic):
        self.position = position
        self.graphic = graphic

class Entity(Sprite):
    def __init__(self, position, graphic, character_class, name='', strength=18, dexterity=18, health=100, inventory=None, equip=None):
        super().__init__(position, graphic)
        self.name = name
        self.character_class = character_class
        self.strength = strength
        self.dexterity = dexterity
        self.health = health
        self.inventory = [] if inventory is None else inventory # ternery operator: mandatory in Python to prevent shared inventory
        self.equip = [] if equip is None else equip
        
        self.attack = strength
        self.defense = dexterity 
    
    def alive(self):
        return self.health > 0

    def dead(self):
        return self.health <= 0


class Barbarian(Entity): # A Hero is a kind of Entity
    def __init__(self, position, graphic, name, strength=20, dexterity=18, health=100):
        super().__init__(
            position, graphic, 'barbarian', name, strength, dexterity, health  #stats #inv #equip
        )
        self.inventory = [HealthPotion(), ManaPotion()]
        self.equip = [AmuletOfStrength(), Battleaxe()]

class Monster(Entity): # A Monster is a kind of Entity
    def __init__(self, position, graphic, character_class, name='', strength=15, dexterity=15, health=80):
        super().__init__(position, graphic, character_class, name, strength, dexterity, health,
            [],
            []
        )

class Zombie(Monster):
    def __init__(self, position):
        super().__init__(position, 'Z', 'zombie')
        self.health = 40

# practice
class Container:
    pi = 3.14
    def __init__(self, a, b, c=''):
        self.a = a
        self.b = b
        self.c = c

class TreasureChest(Container):
    def __init__(self, a, b, d):
        super().__init__(a, b)
        self.d = d

t = TreasureChest(1, 2, 3)
print(t.pi)
print(t.a)
print(t.d)
class Item:
    def __init__(self, item_type):
        self.item_type = item_type

    def modifier_to_str(self, mods):
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
            'health': -2,
            'dexterity': -2
        }

    def __repr__(self):
        return 'AmuletOfStrength()'

    def __str__(self):
        return f'{self.item_type}: {self.name}, {self.modifier_to_str(self.modifier)}'

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
        self.modifier = {'attack': 5}

    def __repr__(self):
        return 'Battleaxe()'

    def __str__(self):
        return f'{self.item_type}: {self.name}, +{self.modifier["strength"]} damage'

class Map():
    def __init__(self, dimensions, entities):
        self.dimensions = dimensions
        self.entities = entities
        self.map_data = []
        for y in range(self.dimensions.height):
            row = []
            for x in range(self.dimensions.width):
                if (x == self.dimensions.width - 1) or (x == 0) or (y == 0) or (y == self.dimensions.height - 1):
                    row.append('#')
                else:
                    row.append('.')
            self.map_data.append(row)

    # def place_entity(self, entity, coord='random'):
    #     if coord == 'random':
    #         coord_list = []
    #         for r in range(len(self.data)):
    #             for c in range(len(self.data[r])):
    #                 if self.data[r][c] == '.':
    #                     coord_list.append((c, r))
    #         coord = choice(coord_list)
    #     x, y = coord
    #     self.data[y][x] = entity
    #     return coord 
    
    def __str__(self):
        for e in self.entities:
            self.map_data[e.position.y][e.position.x] = e.graphic
        text = '\n'
        for r in self.map_data:
            for c in r:
                text += c + ' '
            text += '\n'
        return text

    # def __repr__(self):
    #     for x in self.layout:
    #         str(x)

    # def __str__(self):

class Dimensions:
    def __init__(self, width, height):
        self.width = width
        self.height = height

class Game:
    def __init__(self):
        self.dimensions = Dimensions(16, 12)
        self.entities = [
            Barbarian(Position(5, 5), '@', 'Conan'),
            Zombie(Position(7, 5))
        ]
        # self.map = Map(self.dimensions, self.entities)
        # self.hero_coord = self.map.place_entity('@', (5, 5)) # place hero
        # self.monster_coord = self.map.place_entity('Z') # place zombie
        # print(f'hero at {self.hero_coord}')
        # print(f'monster at {self.monster_coord}')
    
    def display(self):
        self.map = Map(self.dimensions, self.entities)
        print('STATUS:')
        print(self.map)

    def get_command(self):
        command = input('command: ')
        return command

    def play(self):
        self.is_playing = True
        while self.is_playing:
            self.display()
            command = self.get_command()
            self.update_state(command)

    def equip_modifier(self, entity):
        for item in entity.equip:
            for k, v in item.modifier.items():
                new_attribute = getattr(entity, k) + v
                setattr(entity, k, new_attribute)
                if k == 'strength':
                    entity.attack += v
                if k == 'dexterity':
                    entity.defense += v

    def show_stats(self, entity):
        print(f'strength: {entity.strength}, attack: {entity.attack}, health: {entity.health}, dexterity: {entity.dexterity}, defense: {entity.defense}, inventory: {entity.inventory}, equip: {entity.equip}')

    def attack(self, attacker, defender):
        
        base_percent = 50
        chance = base_percent + attacker.dexterity - defender.dexterity
        roll = randint(1, 100)
        if roll < chance:
            # damage = randint(1, attacker.strength)
            damage = round(attacker.attack * (100 / (100 + defender.defense)))
            defender.health -= damage
            print(f'The {attacker.character_class} {attacker.name} hits the {defender.character_class} {defender.name} for {damage}!')
        else:
            print(f'The {attacker.character_class} {attacker.name} misses the {defender.character_class} {defender.name}!')

    def fight(self):
        a = self.entities[0]
        b = self.entities[1]

        self.show_stats(a)
        self.equip_modifier(a)
        self.show_stats(a)

        while a.alive() and b.alive():
            self.attack(a, b)
            self.attack(b, a)
            print(a.name, a.health)
            print(b.name, b.health)

        if a.dead() and b.dead():
            print(f'It\'s a massacre! {a.name} and {b.character_class} are both dead!')
        elif a.dead():
            print(f'Our hero {a.name} has been slain! Game over.')
        else:
            # if isinstance(b, Monster):
            #     self.map.place_entity('T', self.monster_coord)
            self.entities.remove(b)
            print(f'Huzzah! {a.name} has slain {b.character_class}!')
            
        print(a.name, a.health)
        print(b.character_class, b.health)
        # exit()

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

    def input_to_message(self, command):
        message = ''
        command = command.upper()
        if command in ['UP', 'W', 'NORTH']:
            message = 'up'
        elif command in ['DOWN', 'S', 'SOUTH']:
            message = 'down'
        elif command in ['LEFT', 'A', 'WEST']:
            message = 'left'
        elif command in ['RIGHT', 'D', 'EAST']:
            message = 'right'
        elif command in ['Q', 'QUIT', 'EXIT']:
            message = 'quit'
        return message

    # function to take a direction command to move character (arrow keys, wasd, nsew)
    def update_state(self, command):
        message = self.input_to_message(command)
        if message == '':
            return
        if message == 'quit':
            self.is_playing = False
            return
            
        p = self.entities[0].position
        dest = Position(p.x, p.y)
        
        # dest_coord_x, dest_coord_y = (position.x, position.y)

        data = {
            'up': [0, -1],
            'down': [0, 1],
            'left': [-1, 0],
            'right': [1, 0]
        }
        
        dest.x += data[message][0]
        dest.y += data[message][1]

        # destination = Position(dest.x, dest.y)
        # if self.collision_check(destination):
        #     self.entities[0].position = destination
    
        if self.collision_check(dest):
            self.entities[0].position = dest

    def is_empty(self, dest):
        return self.map.map_data[dest.y][dest.x] == '.'

    # function to check for walls or monsters (collision)
    def collision_check(self, dest):
        for entity in self.entities:
            if dest.x == entity.position.x and dest.y == entity.position.y:
                self.fight()
        return self.is_empty(dest)

    # function to move character
    # def update_map(self, destination, hero_coord):
    #     old_coord_x, old_coord_y = hero_coord
    #     self.map.data[old_coord_y][old_coord_x] = '.'
    #     self.map.place_entity('@', destination)

# damage formula incorporating stat bonuses

game = Game()
# game.play()
game.fight()

# game.entities[0].equip_modifier()
