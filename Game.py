from Sprite import Entity, Zombie
from Position import Position
from Map import Map
from Dimension import Dimensions

from random import randint

class Game:
    def __init__(self, interface):
        self.interface = interface
        self.buffer = ''

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
        # self.output(f'hero at {self.hero_coord}')
        # self.output(f'monster at {self.monster_coord}')

    def output(self, text):
        self.buffer += str(text) + '\n'

    def get_player(self):
        # choose_name = input('Enter name: ')
        choose_name = 'Test'
        # choose_class = input('Enter class: ').lower()
        choose_class = 'BARBARIAN'
        # if choose_class == 'BARBARIAN':
        #     return Player_Barbarian(Position(5, 5), choose_name)
        # elif choose_class == 'BARBARIAN2':
        #     return Player_Barbarian2(Position(5, 5), choose_name)
        return Entity(Position(5,5), '@', choose_class, choose_name)

    def display(self):
        self.map = Map(self.dimensions, self.entities)
        self.output('STATUS:')
        self.output(self.map)
        self.interface.display_output(self.buffer)

    def get_command(self):
        command = self.interface.get_input()
        return command.strip()

    def play(self):
        self.is_playing = True
        while self.is_playing:
            self.display()
            command = self.get_command()
            self.update_state(command)

    def show_player_stats(self, player):
        self.output(f'\n{player} -- level: {player.level}, exp: {player.experience}, next level: {player.next_level_exp_req} exp, strength: {player.strength}, attack: {player.attack}, health: {player.health}, dexterity: {player.dexterity}, defense: {player.defense}, inventory: {player.inventory}, equip: {player.equip}')
    
    def show_enemy_stats(self, enemy):
        self.output(f'\n{enemy} -- exp given: {enemy.exp_given}, strength: {enemy.strength}, attack: {enemy.attack}, health: {enemy.health}, dexterity: {enemy.dexterity}, defense: {enemy.defense}, inventory: {enemy.inventory}, equip: {enemy.equip}')

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
            self.output(f'\n{attacker}'.title() + f' hits {defender} for {damage}!')
        else:
            self.output(f'\n{attacker}'.title() + f' misses {defender}!')

    def loot_entity(self, a, b):
        loot = []
        for item in b.inventory:
            loot.append(str(item))
        a.inventory.extend(b.inventory)
        loot = ', '.join(loot)
        message = '\nYou receive: ' + loot + '.'
        self.output(message)

    

    def fight(self):
        a = self.entities[0]
        b = self.entities[1]
        self.output('\n' + repr(a))
        self.output(repr(b))
        self.show_player_stats(a)
        self.show_enemy_stats(b)
        a.equip_modifier()
        b.equip_modifier()
        self.show_player_stats(a)
        self.show_enemy_stats(b)

        while a.alive() and b.alive():
            self.attack(a, b)
            self.attack(b, a)
            self.output(f'\n{repr(a)} {a.health}')
            self.output(f'{repr(b)} {b.health}')
            
        if a.dead() and b.dead():
            self.output(f'\nIt\'s a massacre! {a} and {b} are both dead!')
        elif a.dead():
            self.output(f'\nOur hero {a} has been slain! Game over.')
        else:
            self.output(f'\nHuzzah! {a} has slain {b}!')
            self.loot_entity(a, b)
            a.gain_experience(b)
            self.show_player_stats(a)
            self.show_enemy_stats(b)
            self.entities.remove(b)
            
        self.output(f'\n{repr(a)} {a.health}')
        self.output(f'{repr(b)} {b.health}')
        # exit()

# def map():
#     layout = [
#         ['x', 'x', 'x'],
#         ['x', 'x', 'x'],
#         ['x', 'x', 'x']
#     ]
#     self.output(layout)
#     for r in layout:
#         self.output(' '.join(r))

# def map2():
#     x = 5
#     y = 6
#     layout = []
#     self.output(layout)
#     for i in range(x):
#         layout.append(['x'] * y)
#     for r in layout:
#         self.output(' '.join(r))
#     self.output(layout)

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