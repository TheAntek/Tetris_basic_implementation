import pygame
import sys
from pygame.locals import *
import random
import time
from collections import Counter

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (249, 249, 249)
RED = (255, 22, 22)
GREEN = (0, 255, 0)
colors = [WHITE, GREY, RED, GREEN]
pygame.init()
x = 200
y = 400
display = pygame.display.set_mode((x, y))
pygame.display.set_caption('Tetris!')

shape_t = [[1, 1, 1],
           [0, 1, 0]]
shape_p = [[1, 1, 1, 1],
           [0, 0, 0, 0]]
shape_b = [[1, 1],
           [1, 1]]
shape_horse = [[1, 1, 1],
               [0, 0, 1]]
shape_z = [[1, 1, 0],
           [0, 1, 1]]


def random_xset():
    x = random.choice([x for x in range(20, 121) if x % 20 == 0])
    return x


def rotate(shape):
    colums = len(shape[0])
    rows = len(shape)
    new_shape = []
    if colums > rows and rows != 4:
        for i in list(zip(shape[1], shape[0])):
            i = list(i)
            new_shape.append(i)
    elif colums < rows and rows != 4:
        for i in list(zip(shape[2], shape[1], shape[0])):
            i = list(i)
            new_shape.append(i)
    elif rows == 4:
        for i in list(zip(shape[3], shape[2], shape[1], shape[0])):
            i = list(i)
            new_shape.append(i)
    else:
        new_shape = shape
    return new_shape


def get_cords_shape(x, y, shape):
    start_x = x
    pack = []
    for set in shape:
        for number in set:
            if number != 0:
                pack.append([x, y])
            x += 20
        y += 20
        x = start_x
    return pack


def draw_shape(cords):
    for i in cords:
        pygame.draw.rect(display, WHITE, (i[0], i[1], 20, 20))


def collision(retire, list_of_cords):
    for l in list_of_cords:
        if l[1] + 20 >= y:
            return False
    for i in retire:
        for z in i:
            for l in list_of_cords:
                if (l[1] + 20 == z[1] and z[0] == l[0]):
                    return False


def collision_sides(list_of_cords, move, retire):
    if move == "up" and len(retire) > 0:
        for i in retire:
            for z in i:
                for l in list_of_cords:
                    if (l[0] == z[0] and l[1] == z[1]) or l[0] <= 0 or l[0] >= x - 20 or l[1] >= y:
                        return False
    elif move == "up" and len(retire) == 0:
        for l in list_of_cords:
            if l[0] <= 0 or l[0] >= x - 20 or l[1] == y - 20:
                return False
    elif move == "left" and len(retire) > 0:
        for i in retire:
            for z in i:
                for i in list_of_cords:
                    if i[0] == 0 or (i[0] - 20 == z[0] and i[1] == z[1]):
                        return False
    elif move == "right" and len(retire) > 0:
        for i in retire:
            for z in i:
                for i in list_of_cords:
                    if i[0] == x - 20 or (i[0] + 20 == z[0] and i[1] == z[1]):
                        return False
    elif move == "right" and len(retire) == 0:
        for i in list_of_cords:
            if i[0] == x - 20:
                return False
    elif move == "left" and len(retire) == 0:
        for i in list_of_cords:
            if i[0] == 0:
                return False


def burn(retire):
    burn_row = - 247
    l = Counter([z[1] for i in retire for z in i])
    for i in l:
        if l[i] == 10:
            burn_row = i
            break
    if burn_row > 0:
        rm = ([z for i in retire for z in i if z[1] == burn_row])
        for i in rm:
            for z in retire:
                if i in z:
                    z.remove(i)
        for i in retire:
            for z in i:
                if i == []:
                    retire.remove(i)
                if z[1] < burn_row:
                    z[1] += 20
    return retire


shapes = [shape_p, shape_z, shape_horse, shape_b, shape_t]
object_shape = random.choice(shapes)
start_y = 0
start_x = random_xset()

retire = []
last_shape = []
top_blocks = []

while True:

    display.fill(BLACK)
    list_of_cords = get_cords_shape(start_x, start_y, object_shape)
    draw_shape(list_of_cords)

    for i in list_of_cords:
        if i in top_blocks:
            pygame.quit()
            sys.exit()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if collision_sides(list_of_cords, "left", retire) != False:
                    start_x -= 20
            if event.key == pygame.K_RIGHT:
                if collision_sides(list_of_cords, "right", retire) != False:
                    start_x += 20
            if event.key == pygame.K_UP:
                temp_shape = rotate(object_shape)
                temp_cords = get_cords_shape(start_x, start_y, temp_shape)
                if collision_sides(temp_cords, "up", retire) != False:
                    object_shape = rotate(object_shape)
            if event.key == pygame.K_DOWN:
                if collision(retire, list_of_cords) == False:
                    retire.append(list_of_cords)
                    object_shape = random.choice(shapes)
                    start_y = 0
                    start_x = random_xset()
                else:
                    start_y += 20

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    list_of_cords = get_cords_shape(start_x, start_y, object_shape)

    if collision(retire, list_of_cords) == False:
        retire.append(list_of_cords)
        object_shape = random.choice(shapes)
        start_y = 0
        start_x = random_xset()

    start_y += 20

    if len(retire) > 0:
        color = RED
        top_blocks = []
        for i in burn(retire):
            for z in i:
                if z[1] == 20:
                    top_blocks.append(z)
                pygame.draw.rect(display, color, (z[0], z[1], 20, 20))

    time.sleep(150 / 1000.0)
    pygame.display.update()
