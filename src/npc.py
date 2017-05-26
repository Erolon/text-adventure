class NPC(): # probably should inherit Object

    char = '@'
    DEFAULT_COLOR = (255, 255, 0)

    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.color = self.DEFAULT_COLOR

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        

    # def interact():
        # do stuff based on the id