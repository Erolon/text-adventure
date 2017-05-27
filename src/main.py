#!/usr/bin/python3

import tdl

import sys
sys.path.append('Objects')

from gameobject import Object
from tile import Tile
from game_map import Game_Map
from player import Player
from npc import NPC
from door import Door

screen_width = 30
screen_height = 50
LIMIT_FPS = 60

def handle_keys(player): 
    user_input = tdl.event.key_wait()
    # Movement keys
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

    elif user_input.key == 'UP': # Change the direction you're facing
        player.facing = 'up'
    elif user_input.key == 'LEFT':
        player.facing = 'left'
    elif user_input.key == 'RIGHT':
        player.facing = 'right'
    elif user_input.key == 'DOWN':
        player.facing = 'down'

    if user_input.key == 'ESCAPE':
        return True  # Exit game

def objectBlocksMovement(x, y):
    for object in objects:
        if object.x == x and object.y == y:
            if object.blocks_movement:
                return True
    return False

def interactWithObjectAt(x, y):
    for object in objects:
        if object.x == x and object.y == y:
            object.interact() # later add checks so monsters have different behaviour than npcs

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

color_wall = (128, 128, 128)
color_white = (255, 255, 255)

WALL_CHAR = '#'
GROUND_CHAR = '.'
PLAYER_CHAR = '@'
NPC_CHAR = '@'
DOOR_CHAR = 'D'

def render_all(): # Render map and UI
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

    root.blit(con, 0, 0, screen_width, screen_height, 0, 0) # move the console's contents to the root console

    # Prepare to render the UI Panel
    panel.clear(fg=color_white, bg=(45, 10, 10))

    # Render the bars here
    render_bar(1, 1, BAR_WIDTH, 'HP', player.hp, player.maxHp, (200, 0, 0), (160, 0, 0)) # HP BAR
    render_bar(1, 3, BAR_WIDTH, 'MANA', player.mana, player.maxMana, (85, 140, 255), (15, 90, 200)) # HP BAR
    render_ui_text()

    # Move panel contents to the root panel
    root.blit(panel, 0, PANEL_Y, screen_width, PANEL_HEIGHT, 0, 0)

def render_ui_text():
    y = 5
    faceX = screen_width // 4
    direction = "North"
    if player.facing == 'left':
        direction = "West"
    elif player.facing == 'right':
        direction = "East"
    elif player.facing == 'down':
        direction = "South"

    panel.draw_str(faceX, y, "Facing: " + direction)

    levelX = faceX * 1.85
    panel.draw_str(levelX, y, "Level: " + str(player.level))

    xpX = faceX * 2.5
    panel.drawStr(xpX, y, "Experience: " + str(player.xp))

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
screen_height = game_map.height
screen_width = game_map.width

BAR_WIDTH = screen_width - 2
PANEL_HEIGHT = 7
PANEL_Y = screen_height

gameIsRunning = True

root = tdl.init(screen_width, screen_height + PANEL_HEIGHT, title="Game", fullscreen=False) # Height = map + ui
tdl.setFPS(LIMIT_FPS)
con = tdl.Console(screen_width, screen_height) # Map console
panel = tdl.Console(screen_width, PANEL_HEIGHT) # UI console

while not tdl.event.is_window_closed():
    render_all()
    tdl.flush()

    for object in objects:
        con.draw_str(object.x, object.y, GROUND_CHAR, object.color)

    exit_game = handle_keys(player) # all keyboard input here
    if exit_game:
        break