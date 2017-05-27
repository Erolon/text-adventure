from game_object import Game_Object

class Door(Game_Object):

    char_closed = 'D'
    char_open = 'd'
    DEFAULT_COLOR = (160, 110, 50)

    def __init__(self, x, y, isOpen=1):
        self.x = x
        self.y = y
        self.color = self.DEFAULT_COLOR
        self.isOpen = isOpen
        self.id = "DOOR"
        self.canFight = False
        if isOpen == 0:
            self.char = self.char_open
            self.blocks_movement = False
            self.name = "Door (Open)"
        else:
            self.char = self.char_closed
            self.blocks_movement = True
            self.name = "Door (Closed)"
        
    def interact(self):
        print("Interacting with " + str(self.id) + " at " + str(self.x) + ", " + str(self.y))
        self.isOpen = not self.isOpen
        if self.blocks_movement:
            self.char = self.char_open
            self.blocks_movement = False
            self.name = "Door (Open)"
        else:
            self.char = self.char_closed
            self.blocks_movement = True
            self.name = "Door (Closed)"