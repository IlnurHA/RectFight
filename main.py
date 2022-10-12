import pygame
import classes
from random import randint, random

pygame.init()


def random_cubes() -> [int, int]:
    ans = [1, 1]
    temp1, temp2 = random() ** 2, random() ** 2
    for i in range(6):
        iplusone = i + 1
        if temp1 >= iplusone / 6:
            ans[0] = iplusone
        if temp2 >= iplusone / 6:
            ans[1] = iplusone
    return ans


def next_turn(player_temp, board_check):
    global winner, winner_color
    player_temp = 3 - player_temp
    cubes = random_cubes()
    check, color_temp = board_check.win_check()
    if check:
        winner = True
        winner_color = color_temp
    return player_temp, cubes


def init(*obj):
    desk_rect, board = obj

    delta = int((desk_rect[2] // len(board.board[0])) * 0.09)
    if delta == 0:
        delta = 1

    dx = int((desk_rect[2] // len(board.board[0]) + delta) * len(board.board[0]))
    if dx != desk_rect[2] - delta:
        desk_rect[2] = dx + delta

    dy = int((desk_rect[3] // len(board.board) + delta) * len(board.board))
    if dy != desk_rect[3] - delta:
        desk_rect[3] = dy + delta
    return desk_rect


# win = pygame.mixer.Sound('data/sound/Win.wav')
# next_turn_sound = pygame.mixer.Sound('data/sound/NextTurn.wav')
# set_block = pygame.mixer.Sound('data/sound/Block.wav')

screen_size = width, height = (1920, 1080)
screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
fullscreen = True

running = True
x, y = 0, 0
cube_1, cube_2 = random_cubes()
FPS = 200
pressed = False
mouse_down = False
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
desk_rect = [width // 4, height // 8, int(height / 1.5), int(height / 1.5)]
font = pygame.font.Font(None, height // 16)
player = 1
board_size = (10, 10)

bg = classes.BackgroundAnim(screen_size)
board = classes.Board(board_size[0], board_size[1])
arrow = classes.Mouse()

second_x, second_y = 0, 0
rect_x, rect_y = 0, 0
trying_rect = False
winner = False
winner_color = (0, 0, 0)

end_turn_button = classes.Button((100, height - 300), 'End Turn', pressed=False, size=(width // 11, height // 15))

desk_rect = init(desk_rect, board)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            arrow.change_pos(event.pos)
            if trying_rect:
                second_x, second_y = event.pos
            if end_turn_button.check(event.pos):
                end_turn_button.crossing()
            else:
                end_turn_button.crossed = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            arrow.clicked()
            if not winner:
                rect_x, rect_y = event.pos
                second_x, second_y = event.pos
                trying_rect = True
                if board.button_down(event.pos, desk_rect, screen_size, player):
                    pressed = True
                else:
                    if end_turn_button.check(event.pos):
                        end_turn_button.pressed = True
                    pressed = False
        if event.type == pygame.MOUSEBUTTONUP:
            arrow.unclicked()
            if not winner:
                trying_rect = False
                if end_turn_button.check(event.pos) and end_turn_button.pressed:
                    player, (cube_1, cube_2) = next_turn(player, board)
                    # set_block.play()

                if board.rect_check((second_x, second_y), desk_rect, screen_size, player, (rect_x, rect_y),
                                    (cube_1, cube_2)):
                    board.undefined_rect_paste()
                    player, (cube_1, cube_2) = next_turn(player, board)
                    # next_turn_sound.play()
                end_turn_button.pressed = False
            else:
                player = 1
                board.board = [[0] * board_size[0] for _ in range(board_size[1])]
                cube_1, cube_2 = random_cubes()
                winner = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_f:
                if fullscreen:
                    pygame.display.set_mode(screen_size)
                else:
                    pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
                fullscreen = not fullscreen
    if not winner:
        if player == 1:
            screen.fill((255, 125, 125))
        elif player == 2:
            screen.fill((125, 125, 255))
        bg.render(screen)
        pygame.draw.rect(screen, (40, 40, 40), desk_rect)
        board.render(screen, screen_size, desk_rect)

        if trying_rect:
            board.undefined_rect((second_x, second_y), desk_rect, screen_size, player, (rect_x, rect_y))
            color = pygame.Color('red')
            if player == 1:
                color = pygame.Color('red')
            elif player == 2:
                color = pygame.Color('blue')

            rect_init_x, rect_init_y = rect_x, rect_y
            draw_delta_x, draw_delta_y = arrow.pos[0] - rect_x, arrow.pos[1] - rect_y

            if draw_delta_x < 0:
                rect_init_x = arrow.pos[0]
                draw_delta_x = rect_x - arrow.pos[0]

            if draw_delta_y < 0:
                rect_init_y = arrow.pos[1]
                draw_delta_y = rect_y - arrow.pos[1]

            pygame.draw.rect(screen, color, (rect_init_x, rect_init_y, draw_delta_x, draw_delta_y), 5)

        screen.blit(font.render(f'Ваш дроп: {cube_1} {cube_2}', 0, (0, 0, 0)), (0, 0))
        screen.blit(font.render(f'В области прямоугольника?: {pressed}', 0, (0, 0, 0)), (0, 60))
        screen.blit(font.render(f'Игрок: {player}', 0, (0, 0, 0)), (0, 120))

        end_turn_button.render(screen)
    else:
        # win.play()
        screen.fill(winner_color)
        screen.blit(font.render('WIN', 0, (255, 255, 255)), (width // 2, height // 2))
    arrow.render(screen)
    clock.tick(FPS)
    pygame.display.flip()
