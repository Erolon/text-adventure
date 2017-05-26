#!/usr/bin/python3

import textwrap
import tdl
from gameobject import Object
from tile import Tile
from game_map import Game_Map

screen_width = 30
screen_height = 50
LIMIT_FPS = 30

def handle_keys(player): 
    user_input = tdl.event.key_wait()
    # Movement keys
    if user_input.key == 'UP':
        newY = player.y - 1
        if (player.x, newY) in con: #TODO FIX
            if not game_map.map_list[newY][player.x].blocked:
                player.move(0, -1)
    elif user_input.key == 'DOWN':
        newY = player.y + 1
        if (player.x, newY) in con:
            if not game_map.map_list[newY][player.x].blocked:
                player.move(0, 1)
    elif user_input.key == 'LEFT':
        newX = player.x - 1
        if (newX, player.y) in con:
            if not game_map.map_list[player.y][newX].blocked:
                player.move(-1, 0)
    elif user_input.key == 'RIGHT':
        newX = player.x + 1
        if (newX, player.y) in con:
            if not game_map.map_list[player.y][newX].blocked:
                player.move(1, 0)

    if user_input.key == 'ENTER' and user_input.alt:
        # Alt+Enter: toggle fullscreen
        tdl.set_fullscreen(not tdl.get_fullscreen())
    elif user_input.key == 'ESCAPE':
        return True  # Exit game

def tileForChar(char):
    if char is WALL_CHAR:
        return Tile(char, True)
    elif char is GROUND_CHAR or PLAYER_CHAR:
        return Tile(char, False)

player = None # Initialized in loadMap

def loadMap(current_level):
    global player

    with open("Maps/level" + str(current_level) + ".map") as file:
        mapList =  [[tileForChar(char) for char in list(line.rstrip())] for line in file]
    height = len(mapList) # Always reference mapList [y][x]!
    width = len(mapList[0])

    for y in range(height):
        for x in range(width):
            if mapList[y][x].char is PLAYER_CHAR:
                player = Object(x, y, PLAYER_CHAR, (255, 255, 255))


    return Game_Map(mapList, width, height)

color_dark_wall = (0, 0, 100)
color_light_wall = (130, 110, 50)

color_dark_ground = (50, 50, 150)
color_light_ground = (200, 180, 50)

WALL_CHAR = '#'
GROUND_CHAR = '.'
PLAYER_CHAR = '@'
NPC_CHAR = '@'

def render_all(): ## Needs to be modified later
    # print(str(player.x) + " " + str(player.y))

    for object in objects:
        con.draw_char(object.x, object.y, object.char, object.color)

    for y in range(game_map.height):
        for x in range(game_map.width):
            char = game_map.map_list[y][x].char
            if char is WALL_CHAR:
                con.draw_char(x, y, None, fg=None, bg=color_dark_wall)
            else:
                con.draw_char(x, y, None, fg=None, bg=color_dark_ground)

    root.blit(con, 0, 0, screen_width, screen_height, 0, 0) # move the console's contents to the root console

    # Prepare to render the UI Panel
    panel.clear(fg=(255, 255, 255), bg=(0, 0, 0))

    # Render the bars here
    render_bar(1, 1, BAR_WIDTH, 'HP', 10, 15, (200, 0, 0), (160, 0, 0)) # HP BAR
    render_bar(1, 3, BAR_WIDTH, 'MANA', 7, 12, (85, 140, 255), (15, 90, 200)) # HP BAR

    # Move panel contents to the root panel
    root.blit(panel, 0, PANEL_Y, screen_width, PANEL_HEIGHT, 0, 0)

def render_bar(x, y, total_width, name, value, maximum, bar_color, back_color):
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

root = tdl.init(screen_width, screen_height + PANEL_HEIGHT, title="Game", fullscreen=False) # Height = map + ui
tdl.setFPS(LIMIT_FPS)
con = tdl.Console(screen_width, screen_height) # Map console
panel = tdl.Console(screen_width, PANEL_HEIGHT) # UI console

# player = Object(screen_width // 2, screen_height // 2, '@', (255,255,255)) # // = integer division
npc = Object(screen_width // 2 - 5, screen_height // 2, NPC_CHAR, (255,255,0))
objects = [npc, player]

while not tdl.event.is_window_closed():

    render_all()
    tdl.flush()

    for object in objects:
        con.draw_char(object.x, object.y, ' ', object.color)

    exit_game = handle_keys(player) # all keyboard input here
    if exit_game:
        break