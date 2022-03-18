'''
This is a game where a hero will fight a monster, taking turns, until one has 0 or less hit points. Each attack will do a random amount of damage based on the entity's strength, and will have a random chance of success based on the defender's dexterity. Fight until death.

Nouns: game, hero, monster, attacker, defender, entity
Adjectives: strength, dexterity, hp, dead, turn
Verbs: fight, attack

future: weapons, armor, treasure, inventory, accuracy, experience, stat increase
'''
from Game import Game

class Interface:
    def get_input():
        return input()

    def display_output(text):
        print(text)

game = Game()
game.play(Interface)
# game.fight()

# game.entities[0].equip_modifier()
