class Player(): # probably should inherit Object

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

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        


