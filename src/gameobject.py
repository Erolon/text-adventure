class Object:
    # Represents an item in the game
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.tilesMoved = 0

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def clear(self): # Remove the object
        con.draw_char(self.x, self.y, ' ', self.color)