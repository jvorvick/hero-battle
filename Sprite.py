from Item import HealthPotion, ManaPotion, AmuletOfStrength, Battleaxe

class Sprite:
    def __init__(self, position, graphic):
        self.position = position
        self.graphic = graphic

class Entity(Sprite):
    def __init__(self, position, graphic, character_class, name='', strength=18, dexterity=18, health=100, inventory=None, equip=None):
        super().__init__(position, graphic)
        self.name = name
        self.character_class = character_class
        self.strength = strength + self.get_mod('strength')
        self.dexterity = dexterity + self.get_mod('dexterity')
        self.health = health
        self.inventory = [] if inventory is None else inventory # ternery operator: mandatory in Python to prevent shared inventory
        self.equip = [] if equip is None else equip
        
        self.attack = strength
        self.defense = dexterity 
    
        self.level = 1
        self.experience = 0

    @property
    def next_level_exp_req(self): 
        return int(self.level * 100 * 1.25)

    def get_mod(self, attr):
        class_mods = {
            'barbarians': {
                'strength': 6,
            }
        }
        if self.character_class not in class_mods:
            return 0
        if attr not in class_mods[self.character_class]:
            return 0
        return class_mods[self.character_class][attr]

    def alive(self):
        return self.health > 0

    def dead(self):
        return self.health <= 0

    def is_level_up(self):
        if self.experience >= self.next_level_exp_req:
            return True
        return False

    def gain_experience(self, monster):
        self.experience += monster.exp_given
        print(f'\n{self} gains {monster.exp_given} exp.')
        if self.is_level_up():
            self.level += 1
            print(f'\n{self} is now level {self.level}!')

    def equip_modifier(self):
        for item in self.equip:
            for k, v in item.modifier.items():
                new_attribute = getattr(self, k) + v
                setattr(self, k, new_attribute)
                if k == 'strength':
                    self.attack += v
                if k == 'dexterity':
                    self.defense += v

    def __repr__(self):
        return f'Entity({self.position}, {self.graphic}, {self.character_class})'

    def __str__(self):
        return f'{self.name} the {self.character_class}'

# class Barbarian(Entity): # A Hero is a kind of Entity
#     def __init__(self, position, name, graphic, strength=20, dexterity=18, health=100):
#         super().__init__(position, graphic, 'barbarian', name, strength, dexterity, health)
#         self.inventory = [HealthPotion(), ManaPotion()]
#         self.equip = [AmuletOfStrength(), Battleaxe()]

#     def __repr__(self):
#         return f'Barbarian({self.position}, {self.graphic}, {self.name})'

#     def __str__(self):
#         return self.character_class

# class Barbarian2(Entity): # A Hero is a kind of Entity
#     def __init__(self, position, name, graphic, strength=20, dexterity=18, health=100):
#         super().__init__(position, graphic, 'barbarian', name, strength, dexterity, health)
#         self.inventory = [HealthPotion(), ManaPotion()]
#         self.equip = [AmuletOfStrength(), Battleaxe()]

# class Player_Barbarian(Barbarian):
#     def __init__(self, position, name):
#         super().__init__(position, name, '@')
#         self.experience = 0
#         self.level = 1

#     @property
#     def next_level_exp_req(self): 
#         return int(self.level * 100 * 1.25)

#     def __repr__(self):
#         return f'Player_Barbarian({self.position}, {self.name})'
    
#     def __str__(self):
#         return self.name

# class Player_Barbarian2(Barbarian2):
#     def __init__(self, position, name):
#         super().__init__(position, name, '@')
#         self.experience = 0
#         self.level = 1

#     @property
#     def next_level_exp_req(self): 
#         return int(self.level * 100 * 1.25)

#     def __repr__(self):
#         return f'Player_Barbarian2({self.position}, {self.name})'

#     def __str__(self):
#         return self.name

class Monster(Entity): # A Monster is a kind of Entity
    def __init__(self, position, graphic, character_class, exp_given, name='', strength=15, dexterity=15, health=80):
        super().__init__(position, graphic, character_class, name, strength, dexterity, health)
        self.exp_given = exp_given

    def __repr__(self):
        return f'Monster({self.character_class})'

    def __str__(self):
        return 'a ' + self.character_class
        
class Zombie(Monster):
    def __init__(self, position):
        super().__init__(position, 'Z', 'zombie', 75)
        self.health = 40
        self.inventory = [HealthPotion(), ManaPotion()]
        self.equip = []

    def __repr__(self):
        return f'Zombie({self.position})'

    def __str__(self):
        return 'a ' + self.character_class