import pygame
import os
import sys
from button import Button


def load_image(name, color_key=None):
    try:
        image = pygame.image.load(name)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image

def main():
    pygame.init()
    screen_size = (500, 500)
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    from sprites import GameObject, SpriteGroup
    display_start_screen(screen,clock)
    draw_game_field(screen)
    global CURRENT_TURN, GAME_FIELD, WINNER
    group = SpriteGroup()
    is_game_finished = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if is_game_finished or CURRENT_TURN == 11:
                    WINNER = '-'
                    is_game_finished = False
                    CURRENT_TURN = 0
                    break
                if CURRENT_TURN == 0:
                    CURRENT_TURN += 2
                    continue
                x,y = pygame.mouse.get_pos()
                if 99 <= x <= 399 and 99 <= y <= 399 and not is_game_finished:
                    x = (x - 99) // 100
                    y = (y - 99) // 100
                    if GAME_FIELD[y][x] != '-':
                        continue
                    if CURRENT_TURN % 2 == 0:
                        GAME_FIELD[y][x] = 'x'
                    else:
                        GAME_FIELD[y][x] = 'o'
                    CURRENT_TURN += 1
                    GameObject(x * 100, y * 100, group, GAME_FIELD[y][x])
                    is_game_finished = check_end_game(y,x,GAME_FIELD[y][x])
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        group.update()
        group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
        if is_game_finished or CURRENT_TURN == 11:
            group.empty()
            end_game_image = load_end_game_image(WINNER if is_game_finished else "draw")
            screen.blit(end_game_image, (0, 0))
WINNER = '-'
GAME_MODE = 0
GAME_FIELD = [["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]]
CURRENT_TURN = 0
FPS = 60

def display_start_screen(screen,clock):
    buttons = pygame.sprite.Group()
    y = 230
    x = 160
    intro_text = [["Играть с ботом", setter_game_mode_1], ["Играть с другом", setter_game_mode_2]]
    logo = pygame.transform.scale(load_image('./textures/Logo.PNG'), (200, 200))
    pygame.display.flip()
    font = pygame.font.Font(None, 30)
    text_coord = 180
    screen.fill(pygame.Color(20, 189, 172))

    for line in intro_text:
        button = Button((x, y), line[0], 30, screen, command=line[1])
        y += 50
        x -= 4
        buttons.add(button)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if GAME_MODE == 0:
            buttons.update()
            buttons.draw(screen)
        else:
            return
        screen.blit(logo,(150,20))
        pygame.display.flip()
        clock.tick(FPS)

def check_line(x, y, dx, dy, type):
    score = 0
    global GAME_FIELD
    while 0 <= x - dx < 3 \
            and 0 <= y - dy < 3 \
            and GAME_FIELD[x - dx][y - dy] == type:
        x -= dx
        y -= dy
    while 0 <= x < 3 \
            and 0 <= y < 3 \
            and GAME_FIELD[x][y] == type:
        x += dx
        y += dy
        score += 1
    return score >= 3

def check_end_game(x, y, value):
    global WINNER
    lines = [lambda: check_line(x, y, 0, 1, value),
             lambda: check_line(x, y, 1, 0, value),
             lambda: check_line(x, y, 1, 1, value),
             lambda: check_line(x, y, 1, -1, value)]
    for line in lines:
        result = line()
        if result:
            WINNER = value
            return True
    return False

def setter_game_mode_1():
    global GAME_MODE
    GAME_MODE = 1


def setter_game_mode_2():
    global GAME_MODE
    GAME_MODE = 2


def draw_game_field(screen):
    width, height = screen.get_size()
    color = pygame.Color("cyan")
    screen.fill(color)
    coordinates1 = [[100, 200], [400, 200]]
    coordinates2 = [[100, 300], [400, 300]]
    coordinates3 = [[200, 100], [200, 400]]
    coordinates4 = [[300, 100], [300, 400]]
    pygame.draw.line(screen, pygame.Color("black"), coordinates1[0], coordinates1[1])
    pygame.draw.line(screen, pygame.Color("black"), coordinates2[0], coordinates2[1])
    pygame.draw.line(screen, pygame.Color("black"), coordinates3[0], coordinates3[1])
    pygame.draw.line(screen, pygame.Color("black"), coordinates4[0], coordinates4[1])

def load_end_game_image(winner):
    images = {
        'x': load_image('textures/cross_win.png'),
        'o': load_image('textures/circle_win.png'),
        'draw': load_image('textures/draw.png')
    }
    return images[winner]

if __name__ == "__main__":
    main()
