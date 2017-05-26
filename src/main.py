#!/usr/bin/python3

import tdl
from gameobject import Object
from tile import Tile
from game_map import Game_Map
from player import Player
from npc import NPC

screen_width = 30
screen_height = 50
LIMIT_FPS = 30

def handle_keys(player): 
    user_input = tdl.event.key_wait()
    # Movement keys
    if user_input.key == 'UP':
        newY = player.y - 1
        if (player.x, newY) in con:
            if not game_map.map_list[newY][player.x].blocked:
                if isObjectAtPoint(player.x, newY):
                    interactWithObjectAt(player.x, newY)
                else:
                    player.move(0, -1)
    elif user_input.key == 'DOWN':
        newY = player.y + 1
        if (player.x, newY) in con:
            if not game_map.map_list[newY][player.x].blocked:
                if isObjectAtPoint(player.x, newY):
                    interactWithObjectAt(player.x, newY)
                else:
                    player.move(0, 1)
    elif user_input.key == 'LEFT':
        newX = player.x - 1
        if (newX, player.y) in con:
            if not game_map.map_list[player.y][newX].blocked:
                if isObjectAtPoint(newX, player.y):
                    interactWithObjectAt(newX, player.y)
                else:
                    player.move(-1, 0)
    elif user_input.key == 'RIGHT':
        newX = player.x + 1
        if (newX, player.y) in con:
            if not game_map.map_list[player.y][newX].blocked:
                if isObjectAtPoint(newX, player.y):
                    interactWithObjectAt(newX, player.y)
                else:
                    player.move(1, 0)

    if user_input.key == 'ESCAPE':
        return True  # Exit game

def interactWithObjectAt(x, y):
    for object in objects:
        if str(object.x) == str(x) and str(object.y) == str(y): # Strange conversions again
            # print("It's there!")
            object.interact() # later add checks so monsters have different behaviour than npcs

def isObjectAtPoint(x, y):
    for object in objects:
        if str(object.x) == str(x) and str(object.y) == str(y): # Strange conversions need to be done here
            # print("It's there!")
            return True
    return False

def tileForChar(char):
    if char is WALL_CHAR:
        return Tile(char, True)
    elif char is GROUND_CHAR or PLAYER_CHAR:
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
            identifier = line.partition(';')
            if identifier[0] == "NPC":
                # NPC;10;10;1;
                xTuple = identifier[2].partition(';')
                # xTuple = 10;10;1;
                x = xTuple[0]
                yTuple = xTuple[2].partition(';')
                # yTuple = 10;1;
                y = yTuple[0]
                idTuple = yTuple[2].partition(';')
                # idTuple = 1;
                npcId = idTuple[0]
                objects.append(NPC(x, y, npcId))
                print(x + " " + y + " " + npcId)

    return Game_Map(mapList, width, height)

color_dark_wall = (0, 0, 100)
color_light_wall = (130, 110, 50)

color_dark_ground = (50, 50, 150)
color_light_ground = (200, 180, 50)

WALL_CHAR = '#'
GROUND_CHAR = '.'
PLAYER_CHAR = '@'
NPC_CHAR = '@'

def render_all(): # Render map and UI

    for object in objects:
        con.draw_str(object.x, object.y, object.char, object.color) # Draw char doesn't work for some reason. Have to use draw_str

    for y in range(game_map.height):
        for x in range(game_map.width):
            char = game_map.map_list[y][x].char
            if char is WALL_CHAR:
                con.draw_char(x, y, None, fg=None, bg=color_dark_wall)
            else:
                con.draw_char(x, y, None, fg=None, bg=color_dark_ground)

    root.blit(con, 0, 0, screen_width, screen_height, 0, 0) # move the console's contents to the root console

    # Prepare to render the UI Panel
    panel.clear(fg=(255, 255, 255), bg=(45, 10, 10))

    # Render the bars here
    render_bar(1, 1, BAR_WIDTH, 'HP', player.hp, player.maxHp, (200, 0, 0), (160, 0, 0)) # HP BAR
    render_bar(1, 3, BAR_WIDTH, 'MANA', player.mana, player.maxMana, (85, 140, 255), (15, 90, 200)) # HP BAR

    # Move panel contents to the root panel
    root.blit(panel, 0, PANEL_Y, screen_width, PANEL_HEIGHT, 0, 0)

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

DIALOGUE_HEIGHT = 5

root = tdl.init(screen_width, screen_height + PANEL_HEIGHT, title="Game", fullscreen=False) # Height = map + ui
tdl.setFPS(LIMIT_FPS)
con = tdl.Console(screen_width, screen_height) # Map console
panel = tdl.Console(screen_width, PANEL_HEIGHT) # UI console
# dialoguePanel = tdl.Console(screen_width // 3 * 2, DIALOGUE_HEIGHT) # Dialogue console TODO Implement

# isDialogueActive = False #TODO Implement

while not tdl.event.is_window_closed():

    render_all()
    tdl.flush()

    for object in objects:
        con.draw_str(object.x, object.y, ' ', object.color)

    exit_game = handle_keys(player) # all keyboard input here
    if exit_game:
        break