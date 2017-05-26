class Tile:
    # a tile of the map and its properties
    def __init__(self, char, blocked):
        self.blocked = blocked
        self.char = char