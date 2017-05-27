class Player(): # probably should inherit Object

    char = '@'
    DEFAULT_COLOR = (255, 255, 255)

    STARTING_HP = 10
    STARTING_MANA = 5
    STARTING_STAMINA = 2
    STARING_STAMINA_REGEN = 1

    def __init__(self, x, y):
        self.level = 1
        self.xp = 0
        self.hp = self.maxHp = self.STARTING_HP
        self.mana = self.maxMana = self.STARTING_MANA
        self.stamina = self.maxStamina = self.STARTING_STAMINA
        self.stamina_regen = self.STARING_STAMINA_REGEN
        self.x = x
        self.y = y
        self.color = self.DEFAULT_COLOR
        self.facing = 'right'
        self.damage = 1
        self.attack_stamina_cost = 1
        self.attack_speed = 120 # in frames
        self.attack_speed_in_seconds = self.attack_speed / 60

    def move(self, dx, dy):
        self.x += dx
        self.y += dy