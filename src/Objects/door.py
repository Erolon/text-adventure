class Door(): # probably should inherit Object

    char_closed = 'D'
    char_open = 'd'
    DEFAULT_COLOR = (160, 110, 50)

    def __init__(self, x, y, npcId, isOpen=False):
        self.x = x
        self.y = y
        self.id = npcId
        self.color = self.DEFAULT_COLOR
        self.isOpen = isOpen
        if isOpen:
            self.char = self.char_open
            self.blocks_movement = False
        else:
            self.char = self.char_closed
            self.blocks_movement = True

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        
    def interact(self):
        print("Interacting with " + str(self.id))
        self.isOpen = not self.isOpen
        if self.blocks_movement:
            self.char = self.char_open
            self.blocks_movement = False
        else:
            self.char = self.char_closed
            self.blocks_movement = True