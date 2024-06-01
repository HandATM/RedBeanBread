import time
import math
import random
import pygame # pip install pygame
from pymsgbox import _confirmTkinter as confirm, CANCEL_TEXT # pip install pymsgbox

pygame.init()

# set game constants
WINDOW_WIDTH = 1800
WINDOW_HEIGHT = 1000
BREAD_RADIUS = 16
BREAD_LINE_THICKNESS = 8
RESULT_POSITION = [270, WINDOW_HEIGHT - 50]

PERMUTE = 'permute'
KEEP = 'keep'

# color
BGCOLOR = (244, 247, 247)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
BREAD_INCOLOR = (195, 113, 39)
BREAD_OUTCOLOR = (232, 208, 130)

# clock
FPS = 60
FPSCLOCK = pygame.time.Clock()

# font
FONT = 'consolas'
FONTSIZE = 30
BASICFONT = pygame.font.SysFont(FONT, FONTSIZE, italic=True)

# dora-emong image
cursor_img = pygame.image.load('related_files\\dora_emong.png')

# set game variables
bread_pos = [random.randrange(5, WINDOW_WIDTH - 4), random.randrange(5, WINDOW_HEIGHT - 4)]
msg = ''
start_time = time.time()
number_of_tries = 0
running = True

# create window
DISPLAY = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

pygame.display.set_caption('Look for red bean bread')
pygame.display.set_icon(cursor_img)

def setup():
    DISPLAY.fill(BGCOLOR)
    DISPLAY.blit(cursor_img, cursor_rect)

def show_bread():
    global bread_pos, msg, start_time, running, number_of_tries

    pygame.draw.circle(DISPLAY, BREAD_INCOLOR, bread_pos, BREAD_RADIUS)
    pygame.draw.circle(DISPLAY, BREAD_OUTCOLOR, bread_pos, BREAD_RADIUS + BREAD_LINE_THICKNESS, BREAD_LINE_THICKNESS)
    pygame.display.flip()

    used_time = round(time.time() - start_time, 4)
    goTo = confirm(title = 'Message:', text = f'Number of attempts: {number_of_tries}\nYou used {used_time} seconds to look for red bean bread.')

    if goTo == CANCEL_TEXT:
        running = False
        return

    bread_pos = [random.randrange(5, WINDOW_WIDTH - 4), random.randrange(5, WINDOW_HEIGHT - 4)]
    msg = ''
    start_time = time.time()
    number_of_tries = 0

    DISPLAY.fill(BGCOLOR)

def show_distance(mode):
    global msg
    if mode == PERMUTE: msg = f'Distance to bread: {round(distance, 4)}'

    msg_surf = BASICFONT.render(msg, True, BLACK)
    msg_rect = msg_surf.get_rect(center=RESULT_POSITION)

    DISPLAY.fill(BGCOLOR, msg_rect)
    DISPLAY.blit(msg_surf, msg_rect)

# main-loop
DISPLAY.fill(BGCOLOR)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE: running = False

        elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
            pos = pygame.mouse.get_pos()
            distance = math.sqrt((pos[0] - bread_pos[0]) ** 2 + (pos[1] - bread_pos[1]) ** 2)

            cursor_rect = cursor_img.get_rect(center=pos)
            setup()

            if distance < BREAD_RADIUS: show_bread()
            else:
                number_of_tries += 1
                show_distance(PERMUTE)

        elif event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            cursor_rect = cursor_img.get_rect(center=pos)
            setup()

    show_distance(KEEP)
    pygame.display.flip()
    FPSCLOCK.tick(FPS)

# exit
pygame.quit()