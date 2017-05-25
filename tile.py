class Tile:
    # a tile of the map and its properties
    def __init__(self, char, blocked, block_sight = False):
        self.blocked = blocked
        self.char = char
        self.explored = False
        # By default, if a tile is blocked, it also blocks sight
        if blocked:
            block_sight = True
        self.block_sight = block_sight

    def setBlocked(self, value):
        self.blocked = value
        if value:
            self.block_sight = True