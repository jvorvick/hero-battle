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

    def __repr__(self):
        return f'Position({self.x}, {self.y})'

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
    def __init__(self, position, name, graphic, strength=20, dexterity=18, health=100):
        super().__init__(position, graphic, 'barbarian', name, strength, dexterity, health)
        self.inventory = [HealthPotion(), ManaPotion()]
        self.equip = [AmuletOfStrength(), Battleaxe()]

    def __repr__(self):
        return f'Barbarian({self.position}, {self.graphic}, {self.name})'

    def __str__(self):
        return self.character_class

class Barbarian2(Entity): # A Hero is a kind of Entity
    def __init__(self, position, name, graphic, strength=20, dexterity=18, health=100):
        super().__init__(position, graphic, 'barbarian', name, strength, dexterity, health)
        self.inventory = [HealthPotion(), ManaPotion()]
        self.equip = [AmuletOfStrength(), Battleaxe()]

class Player_Barbarian(Barbarian):
    def __init__(self, position, name):
        super().__init__(position, name, '@')
        self.experience = 0
        self.level = 1
        self.next_level_exp_req = 0

        @property
        def next_level_exp_req(): 
            return self.level * 100 * 1.25

    def __repr__(self):
        return f'Player_Barbarian({self.position}, {self.name})'
    
    def __str__(self):
        return self.name

class Player_Barbarian2(Barbarian2):
    def __init__(self, position, name):
        super().__init__(position, name, '@')

    def __repr__(self):
        return f'Player_Barbarian2({self.position}, {self.name})'

    def __str__(self):
        return self.name

class Monster(Entity): # A Monster is a kind of Entity
    def __init__(self, position, graphic, character_class, exp_given, name='', strength=15, dexterity=15, health=80):
        super().__init__(position, graphic, character_class, name, strength, dexterity, health)
        self.exp_given = exp_given
        
class Zombie(Monster):
    def __init__(self, position):
        super().__init__(position, 'Z', 'zombie', 75)
        self.health = 40
        self.inventory = [HealthPotion(), ManaPotion()]
        self.equip = []

    def __repr__(self):
        return f'Zombie({self.position})'

    def __str__(self):
        return 'the ' + self.character_class

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
        return f'{self.color} {self.item_type}'

class ManaPotion(Potion):
    def __init__(self):
        super().__init__()
        self.color = 'blue'
        self.attribute = 'restore +10 mana'

    def __repr__(self):
        return 'ManaPotion()'

    def __str__(self):
        return f'{self.color} {self.item_type}'

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
        player = self.get_player()
        self.dimensions = Dimensions(16, 12)
        self.entities = [
            player,
            Zombie(Position(7, 5)),
            Zombie(Position(7, 6))
        ]
        # self.map = Map(self.dimensions, self.entities)
        # self.hero_coord = self.map.place_entity('@', (5, 5)) # place hero
        # self.monster_coord = self.map.place_entity('Z') # place zombie
        # print(f'hero at {self.hero_coord}')
        # print(f'monster at {self.monster_coord}')

    def get_player(self):
        # choose_name = input('Enter name: ')
        choose_name = 'Test'
        # choose_class = input('Enter class: ').upper()
        choose_class = 'BARBARIAN'
        if choose_class == 'BARBARIAN':
            return Player_Barbarian(Position(5, 5), choose_name)
        elif choose_class == 'BARBARIAN2':
            return Player_Barbarian2(Position(5, 5), choose_name)
    
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

    def show_player_stats(self, player):
        print(f'\n{player} -- level: {player.level}, exp: {player.experience}, next level: {player.next_level_exp_req}, strength: {player.strength}, attack: {player.attack}, health: {player.health}, dexterity: {player.dexterity}, defense: {player.defense}, inventory: {player.inventory}, equip: {player.equip}')
    
    def show_enemy_stats(self, enemy):
        print(f'\n{enemy} -- exp given: {enemy.exp_given}, strength: {enemy.strength}, attack: {enemy.attack}, health: {enemy.health}, dexterity: {enemy.dexterity}, defense: {enemy.defense}, inventory: {enemy.inventory}, equip: {enemy.equip}')

    def attack(self, attacker, defender):
        # attacker_title = f'{attacker.name if attacker.name else "The " + attacker.character_class}'
        # defender_title = f'{defender.name if defender.name else "the " + defender.character_class}'
        base_percent = 50
        chance = base_percent + attacker.dexterity - defender.dexterity
        roll = randint(1, 100)
        if roll < chance:
            # damage = randint(1, attacker.strength)
            damage = round(attacker.attack * (100 / (100 + defender.defense)))
            defender.health -= damage
            print(f'\n{attacker}'.title() + f' hits {defender} for {damage}!')
        else:
            print(f'\n{attacker}'.title() + f' misses {defender}!')

    @staticmethod
    def loot_entity(a, b):
        loot = []
        message = '\nYou receive: '
        for item in b.inventory:
            loot.append(str(item))
        a.inventory.extend(b.inventory)
        loot = ', '.join(loot)
        message += loot + '.'
        print(message)

    @staticmethod
    def is_level_up(a):
        a.next_level_exp_req = a.level * 100 * 1.25
        if a.experience >= a.next_level_exp_req:
            return True
        return False

    def gain_experience(self, a, b):
        a.experience += b.exp_given
        print(f'{a} gains {b.exp_given} exp.')
        if self.is_level_up(a):
            a.level += 1
            print(f'{a} is now level {a.level}!')

    def fight(self):
        a = self.entities[0]
        b = self.entities[1]
        print('\n' + repr(a))
        print(repr(b))
        self.show_player_stats(a)
        self.show_enemy_stats(b)
        self.equip_modifier(a)
        self.equip_modifier(b)
        self.show_player_stats(a)
        self.show_enemy_stats(b)

        while a.alive() and b.alive():
            self.attack(a, b)
            self.attack(b, a)
            print('\n' + repr(a), a.health)
            print(repr(b), b.health)
            
        if a.dead() and b.dead():
            print(f'\nIt\'s a massacre! {a} and {b} are both dead!')
        elif a.dead():
            print(f'\nOur hero {a} has been slain! Game over.')
        else:
            print(f'\nHuzzah! {a} has slain {b}!')
            self.loot_entity(a, b)
            self.gain_experience(a, b)
            self.show_player_stats(a)
            self.show_enemy_stats(b)
            self.entities.remove(b)
            
        print('\n' + repr(a), a.health)
        print(repr(b), b.health)
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
game.play()
# game.fight()

# game.entities[0].equip_modifier()
