#!/usr/bin/python3

import tdl

import sys
sys.path.append('Objects')

from tile import Tile
from game_map import Game_Map
from player import Player
from npc import NPC
from door import Door
from monster import Monster

map_width = 30
map_height = 50
LIMIT_FPS = 60

def handle_keys(player): 
    global isDialogueActive
    user_input = tdl.event.key_wait()
    # Movement keys

    if user_input.key == 'ESCAPE':
        return True  # Exit game

    if isDialogueActive:
        if user_input.key == 'ENTER':
            isDialogueActive = False
        elif user_input.char == 'e':
            playerInteract(player)
        return

    if user_input.char == 'w':
        newY = player.y - 1
        player.facing = 'up' 
        if (player.x, newY) in con:
            if not game_map.map_list[newY][player.x].blocked and not isBlockingObjectAtPoint(player.x, newY):
                player.move(0, -1)
    elif user_input.char == 's':
        newY = player.y + 1
        player.facing = 'down'
        if (player.x, newY) in con:
            if not game_map.map_list[newY][player.x].blocked and not isBlockingObjectAtPoint(player.x, newY):
                player.move(0, 1)
    elif user_input.char == 'a':
        newX = player.x - 1
        player.facing = 'left'
        if (newX, player.y) in con:
            if not game_map.map_list[player.y][newX].blocked and not isBlockingObjectAtPoint(newX, player.y):
                player.move(-1, 0)
    elif user_input.char == 'd':
        newX = player.x + 1
        player.facing = 'right'
        if (newX, player.y) in con:
            if not game_map.map_list[player.y][newX].blocked and not isBlockingObjectAtPoint(newX, player.y):
                player.move(1, 0)

    elif user_input.char == 'e': # INTERACT
        playerInteract(player)

    elif user_input.key == 'UP': # Change the direction you're facing
        player.facing = 'up'
    elif user_input.key == 'LEFT':
        player.facing = 'left'
    elif user_input.key == 'RIGHT':
        player.facing = 'right'
    elif user_input.key == 'DOWN':
        player.facing = 'down'

def playerInteract(player):
    x = player.x
    y = player.y
    if player.facing == 'right':
        x += 1
    elif player.facing == 'left':
        x -= 1
    elif player.facing == 'up':
        y -= 1
    elif player.facing == 'down':
        y += 1
    if (x, y) in con:
        if isObjectAtPoint(x, y):
            interactWithObjectAt(x, y)
    
def objectBlocksMovement(x, y):
    for object in objects:
        if object.x == x and object.y == y:
            if object.blocks_movement:
                return True
    return False

def interactWithObjectAt(x, y):
    for object in objects:
        if object.x == x and object.y == y:
            if type(object) is NPC:
                message(object.getMessage())
            elif type(object) is Monster:
                object.interact() # object.attack() later
            else:
                object.interact()

def isObjectAtPoint(x, y):
    for object in objects:
        if object.x == x and object.y == y:
            return True
    return False

def isBlockingObjectAtPoint(x, y):
    for object in objects:
        if object.x == x and object.y == y and object.blocks_movement == True:
            return True
    return False

def tileForChar(char):
    if char == WALL_CHAR:
        return Tile(char, True)
    elif char == GROUND_CHAR or char == PLAYER_CHAR:
        return Tile(char, False)

player = None # Initialized in loadMap
objects = [] # Also init in loadMap

def loadMap(current_level):
    global player
    global objects

    # Read player and map
    with open("Maps/level" + str(current_level) + ".map") as file:
        mapList =  [[tileForChar(char) for char in list(line.rstrip())] for line in file]
    height = len(mapList) # Always reference mapList [y][x]!
    width = len(mapList[0])

    for y in range(height):
        for x in range(width):
            if mapList[y][x].char is PLAYER_CHAR:
                player = Player(x, y)
                objects.append(player)

    # Read objects
    with open("Maps/level" + str(current_level) + ".dat") as file:
        for line in file:
            # Handle the objects
            if line.startswith('#'):
                continue
            values = getObjectValues(line)
            if values[0] == "NPC":
                objects.append(NPC(values[1], values[2], values[3]))
            elif values[0] == "DOOR":
                objects.append(Door(values[1], values[2], values[3]))
            elif values[0] == "MONSTER":
                objects.append(Monster(values[1], values[2], values[3]))
                
    return Game_Map(mapList, width, height)

def getObjectValues(line):
    identifierTuple = line.partition(';')
    identifier = identifierTuple[0]
    xTuple = identifierTuple[2].partition(';')
    # xTuple = 10;10;1;
    x = int(xTuple[0])
    yTuple = xTuple[2].partition(';')
    # yTuple = 10;1;
    y = int(yTuple[0])
    idTuple = yTuple[2].partition(';')
    # idTuple = 1;
    objectId = int(idTuple[0])
    return (identifier, x, y, objectId)

def getNameForMapChar(char):
    if char == '#':
        return "Wall"
    elif char == ".":
        return "Ground"
    else:
        return "Unknown"

def getItemThatPlayerFaces():
    pX = player.x
    pY = player.y
    if player.facing == 'right':
        pX += 1
    elif player.facing == 'left':
        pX -= 1
    elif player.facing == 'up':
        pY -= 1
    elif player.facing == 'down':
        pY += 1

    for object in objects:
        if object.x == pX and object.y == pY:
            return object.name
    
    for y in range(game_map.height):
        for x in range(game_map.width):
            if y == pY and x == pX:
                char = game_map.map_list[y][x].char
                return getNameForMapChar(char)

color_wall = (128, 128, 128)
color_white = (255, 255, 255)
color_ui_background = (45, 10, 10)

WALL_CHAR = '#'
GROUND_CHAR = '.'
PLAYER_CHAR = '@'

def render_all(): # Render map and UI
    global messages
    for y in range(game_map.height):
        for x in range(game_map.width):
            char = game_map.map_list[y][x].char
            if char is WALL_CHAR:
                con.draw_char(x, y, WALL_CHAR, fg=color_wall)
            elif char is GROUND_CHAR:
                con.draw_char(x, y, GROUND_CHAR, fg=color_white)

    for object in objects: # Draw objects after map so they go on top
        if type(object) is not Player:
            con.draw_str(object.x, object.y, object.char, object.color) # Draw char doesn't work for some reason. Have to use draw_str

    for object in objects: # Draw player later so it's always on top
        if type(object) is Player:
            con.draw_str(object.x, object.y, object.char, object.color)

    root.blit(con, 0, TOP_PANEL_HEIGHT, map_width, map_height, 0, 0) # move the console's contents to the root console

    # Prepare to render the UI Panel
    panel.clear(fg=color_white, bg=color_ui_background)

    # Render the bars here
    render_bar(1, 1, BAR_WIDTH, 'HP', player.hp, player.maxHp, (200, 0, 0), (160, 0, 0)) # HP BAR
    render_bar(1, 3, BAR_WIDTH, 'MANA', player.mana, player.maxMana, (85, 140, 255), (15, 90, 200)) # MANA BAR
    render_ui_text()

    # Move panel contents to the root panel
    root.blit(panel, 0, PANEL_Y, map_width, PANEL_HEIGHT, 0, 0)

    # Render the top panel
    topPanel.clear(fg=color_white, bg=color_ui_background)

    render_top_bar()

    root.blit(topPanel, 0, 0, map_width, TOP_PANEL_HEIGHT, 0, 0)

    if isDialogueActive:
        dialogue_panel = tdl.Console(dialogue_width, dialogue_height)
        
        y = 2
        for message in messages:
            dialogue_panel.draw_str(2, y, message)
            y += 1

        dialogueX = (map_width - dialogue_width) / 2
        dialogueY = (map_height - dialogue_height) / 2
        root.blit(dialogue_panel, dialogueX, dialogueY, dialogue_width, dialogue_height, 0, 0)

def render_top_bar():
    topPanel.draw_rect(0, 0, map_width, TOP_PANEL_HEIGHT, None, bg=color_ui_background)
    x = map_width // 2.7
    facingItem = getItemThatPlayerFaces()
    topPanel.draw_str(x, 0, "You are facing: " + facingItem, bg=color_ui_background)

messages = []
dialogue_height = None

def message(text):
    global isDialogueActive
    global dialogue_height
    messages.clear()
    dialogue_height = len(text) + 4 # 4 for margin
    # Text is a list
    for string in text:
        messages.append(string)
    isDialogueActive = True

def render_ui_text():
    y = 5
    faceX = map_width // 4
    direction = "North"
    if player.facing == 'left':
        direction = "West"
    elif player.facing == 'right':
        direction = "East"
    elif player.facing == 'down':
        direction = "South"

    panel.draw_str(faceX, y, "Facing: " + direction, bg=color_ui_background)

    levelX = faceX * 1.85
    panel.draw_str(levelX, y, "Level: " + str(player.level), bg=color_ui_background)

    xpX = faceX * 2.5
    panel.drawStr(xpX, y, "Experience: " + str(player.xp), bg=color_ui_background)

def render_bar(x, y, total_width, name, value, maximum, bar_color, back_color): # Render UI bars
    # Calculate the width of the bar
    bar_width = int(float(value) / maximum * total_width)
 
    # Draw the background
    panel.draw_rect(x, y, total_width, 1, None, bg=back_color)
 
    # Draw the bar on top
    if bar_width > 0:
        panel.draw_rect(x, y, bar_width, 1, None, bg=bar_color)

    # Draw the actual values onto the bar
    text = name + ': ' + str(value) + '/' + str(maximum)
    x_centered = x + (total_width-len(text)) // 2
    panel.draw_str(x_centered, y, text, fg=(0, 0, 0), bg=None)

tdl.set_font('Assets/terminal8x8_gs_ro.png')

current_level = 1 # change later
game_map = loadMap(current_level)
map_height = game_map.height
map_width = game_map.width

BAR_WIDTH = map_width - 2
PANEL_HEIGHT = 7
PANEL_Y = map_height

TOP_PANEL_HEIGHT = 3

isDialogueActive = False
dialogue_width = int(round(map_width // 3 * 2.8, -1))

root = tdl.init(map_width, map_height + PANEL_HEIGHT, title="Game", fullscreen=False) # Height = map + ui
tdl.setFPS(LIMIT_FPS)
con = tdl.Console(map_width, map_height) # Map console
panel = tdl.Console(map_width, PANEL_HEIGHT) # UI console
topPanel = tdl.Console(map_width, TOP_PANEL_HEIGHT)

message(["Welcome!",
        "",
        "You can move around with wasd",
        "You can interact with objects by pressing \"e\" while facing them",
        "",
        "Try finding the guide near you and talking to him",
        "You can change the direction you face with the arrow keys",
        "",
        "Press enter to close this dialogue"])

while not tdl.event.is_window_closed():
    render_all()
    tdl.flush()

    for object in objects: # Clear all objects before they get redrawn
        con.draw_str(object.x, object.y, GROUND_CHAR, object.color)

    exit_game = handle_keys(player) # all keyboard input here
    if exit_game:
        break