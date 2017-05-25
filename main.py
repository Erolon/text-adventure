#!/usr/bin/python3

import tdl
from gameobject import Object
from tile import Tile
from game_map import Game_Map

screen_width = 30
screen_height = 50
LIMIT_FPS = 30
current_level = 1

def handle_keys(player): 
    user_input = tdl.event.key_wait()
    # Movement keys
    if user_input.key == 'UP':
        newY = player.y - 1
        if not game_map.map_list[newY][player.x].blocked and (player.x, newY) in con:
            player.move(0, -1)
    elif user_input.key == 'DOWN':
        newY = player.y + 1
        if not game_map.map_list[newY][player.x].blocked and (player.x, newY) in con:
            player.move(0, 1)
    elif user_input.key == 'LEFT':
        newX = player.x - 1
        if not game_map.map_list[player.y][newX].blocked and (newX, player.y) in con:
            player.move(-1, 0)
    elif user_input.key == 'RIGHT':
        newX = player.x + 1
        if not game_map.map_list[player.y][newX].blocked and (newX, player.y) in con:
            player.move(1, 0)

    if user_input.key == 'ENTER' and user_input.alt:
        # Alt+Enter: toggle fullscreen
        tdl.set_fullscreen(not tdl.get_fullscreen())
    elif user_input.key == 'ESCAPE':
        return True  # Exit game

def tileForChar(char):
    if char is 'W':
        return Tile(char, True)
    elif char is '#':
        return Tile(char, False)
    elif char is '@':
        print("Player")
        return Tile(char, False)


player = None

def loadMap():
    global current_level
    global player

    with open("level" + str(current_level) + ".map") as file:
        mapList =  [[tileForChar(char) for char in list(line.rstrip())] for line in file]
    height = len(mapList) # Always reference mapList [y][x]!
    width = len(mapList[0])

    for y in range(height):
        for x in range(width):
            if mapList[y][x].char is '@':
                player = Object(x, y, '@', (255,255,255))


    return Game_Map(mapList, width, height)

color_dark_wall = (0, 0, 100)
color_light_wall = (130, 110, 50)

color_dark_ground = (50, 50, 150)
color_light_ground = (200, 180, 50)

def render_all(): ## Needs to be modified later
    # print(str(player.x) + " " + str(player.y))

    for object in objects:
        con.draw_char(object.x, object.y, object.char, object.color)

    for y in range(game_map.height):
        for x in range(game_map.width):
            char = game_map.map_list[y][x].char
            if char is 'W':
                con.draw_char(x, y, None, fg=None, bg=color_dark_wall)
            else:
                con.draw_char(x, y, None, fg=None, bg=color_dark_ground)

    root.blit(con, 0, 0, screen_width, screen_height, 0, 0) # move the console's contents to the root console

tdl.set_font('Assets/terminal8x8_gs_ro.png')

game_map = loadMap()
screen_height = game_map.height
screen_width = game_map.width

root = tdl.init(screen_width, screen_height, title="Game", fullscreen=False)
tdl.setFPS(LIMIT_FPS)
con = tdl.Console(screen_width, screen_height)

# player = Object(screen_width // 2, screen_height // 2, '@', (255,255,255)) # // = integer division
npc = Object(screen_width // 2 - 5, screen_height // 2, '@', (255,255,0))
objects = [npc, player]


while not tdl.event.is_window_closed():

    render_all()
    tdl.flush()

    for object in objects:
        con.draw_char(object.x, object.y, ' ', object.color)

    exit_game = handle_keys(player) # all keyboard input here
    if exit_game:
        break