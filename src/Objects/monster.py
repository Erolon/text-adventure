from game_object import Game_Object

class Monster(Game_Object):

    char = '@'
    DEFAULT_COLOR = (255, 0, 0)
    blocks_movement = True

    def __init__(self, x, y, monsterId):
        self.name = "Monster"
        self.x = x
        self.y = y
        self.id = monsterId
        self.color = self.DEFAULT_COLOR
       
    def attack(self):
        print("Attacking with Monster with ID " + str(self.id))