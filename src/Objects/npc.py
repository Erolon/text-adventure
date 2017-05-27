from game_object import Game_Object

class NPC(Game_Object):

    char = '@'
    DEFAULT_COLOR = (255, 255, 0)
    blocks_movement = True

    def __init__(self, x, y, npcId):
        self.name = "NPC"
        self.x = x
        self.y = y
        self.id = npcId
        self.color = self.DEFAULT_COLOR
        self.dialogueStage = 1
        self.canFight = False

        if npcId == 1:
            self.name = "Guide"
        if npcId == 2:
            self.name = "Combat Tutor"

        self.name += " (NPC)"
        
    def getMessage(self):
        print("Interacting with NPC with id " + str(self.id))
        if self.id == 1: # GUIDE

            if self.dialogueStage == 1:
                self.dialogueStage += 1
                return ["Hello!",
                        "",
                        "I am a friendly NPC that is of no danger to you",
                        "",
                        "You can continue this conversation by pressing \"e\"",
                        "You can stop talking to me by pressing enter"]
            elif self.dialogueStage == 2:
                self.dialogueStage += 1
                return ["You are now free to enter the world",
                        "",
                        "Leave by interacting with the doors to open them"
                        "",
                        "You can see the controls again by talking to me anytime"]
            elif self.dialogueStage == 3:
                return ["Move with wasd",
                        "Interact with \"e\"",
                        "Face with the arrow keys",
                        "",
                        "Enter to exit a dialogue"]

        elif self.id == 2:
            return ["You should know that the world is not a safe place",
                    "The weakened goblin in the room next to me is a great learning",
                    "opportunity for you. Kill it by pressing \"r\" while facing it",
                    "", "Good luck!"]


        else:
            return ["default npc message"]