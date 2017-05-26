class NPC(): # probably should inherit Object

    char = '@'
    DEFAULT_COLOR = (255, 255, 0)

    def __init__(self, x, y, npcId):
        self.x = x
        self.y = y
        self.id = npcId
        self.color = self.DEFAULT_COLOR

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        
    def interact(self):
        print("Interacting with " + self.id)