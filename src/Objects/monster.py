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
        self.canFight = True

        if monsterId == 1:
            self.name = "Weakened Goblin"
            self.char = "O"
            self.hp = self.maxHp = 2
            self.damage = 1
            self.attack_speed = 1
            self.xp_bounty = 5
       
    def attack(self, damage):
        self.hp -= damage