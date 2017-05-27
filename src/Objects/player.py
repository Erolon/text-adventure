import threading
from game_object import Game_Object

class Player(Game_Object):

    char = '@'
    DEFAULT_COLOR = (255, 255, 255)

    STARTING_HP = 10
    STARTING_MANA = 5

    def __init__(self, x, y):
        self.level = 1
        self.xp = 0
        self.hp = self.maxHp = self.STARTING_HP
        self.mana = self.maxMana = self.STARTING_MANA
        self.x = x
        self.y = y
        self.color = self.DEFAULT_COLOR
        self.facing = 'right'
        self.damage = 1
        self.can_attack = True
        self.attack_speed = 1.0 # In seconds
        self.canFight = True

    def attack(self):
        self.can_attack = False
        timer = threading.Timer(self.attack_speed, self.canAttackAgain)
        timer.setDaemon(True)
        timer.start()

    def canAttackAgain(self):
        self.can_attack = True
