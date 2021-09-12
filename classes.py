import pygame
import random
import sprites
import func

pygame.init()


def create_board(x, y):
    return [[0] * y for _ in range(x)]


def unpack(packed):
    return [obj for obj in packed]


def revolution_settings(first, second):
    if first <= second:
        return second, first - 1, -1
    else:
        return first, second - 1, -1


class Board:
    def __init__(self, len_x, len_y):
        self.len_x, self.len_y = len_x, len_y
        self.board = create_board(len_x, len_y)

    def render(self, *obj):
        screen, screen_size, desk_rect = unpack(obj)
        width, height = screen_size
        delta = int((desk_rect[2] // len(self.board[0])) * 0.09)
        if delta == 0:
            delta = 1
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                color = (255, 255, 255)
                if self.board[i][j] == 0:
                    color = (255, 255, 255)
                elif self.board[i][j] == 1:
                    color = (255, 0, 0)
                elif self.board[i][j] == 1.5:
                    color = (255, 125, 125)
                    self.board[i][j] = 0
                elif self.board[i][j] == 2:
                    color = (0, 0, 255)
                elif self.board[i][j] == 2.5:
                    color = (125, 125, 255)
                    self.board[i][j] = 0
                pygame.draw.rect(screen, color, (width // 4 + delta + i * (desk_rect[2] // len(self.board[0])),
                                                 height // 8 + delta + j * (desk_rect[3] // len(self.board[0])),
                                                 desk_rect[3] // len(self.board[0]) - delta,
                                                 desk_rect[3] // len(self.board[0]) - delta))

    def button_down(self, *obj):
        mousepos, desk_rect, screen_size, player = unpack(obj)
        if desk_rect[0] < mousepos[0] <= desk_rect[0] + desk_rect[2] and desk_rect[1] < mousepos[1] <= desk_rect[1] + \
                desk_rect[3]:
            self.which_pos(mousepos, desk_rect, screen_size, player)
            return True
        return False

    def which_pos(self, *obj, boolean=False, first_pos=False):
        mousepos, desk_rect, screen_size, player = unpack(obj)
        width, height = screen_size
        temp_x = (mousepos[0] - width // 4 - 7) // (desk_rect[2] // len(self.board))
        temp_y = (mousepos[1] - height // 8 - 7) // (desk_rect[3] // len(self.board[0]))
        return temp_x, temp_y

    def undefined_rect(self, *obj):
        mousepos, desk_rect, screen_size, player, first_pos = unpack(obj)
        first_x, first_y = self.which_pos(first_pos, desk_rect, screen_size, player, boolean=True, first_pos=True)
        mouse_x, mouse_y = self.which_pos(mousepos, desk_rect, screen_size, player, boolean=True, first_pos=True)

        first_i, second_i, step_i = revolution_settings(first_x, mouse_x)
        first_j, second_j, step_j = revolution_settings(first_y, mouse_y)

        for i in range(first_i, second_i, step_i):
            for j in range(first_j, second_j, step_j):
                if -1 < i < len(self.board) and -1 < j < len(self.board[0]):
                    if self.board[i][j] == 0:
                        self.board[i][j] = player + 0.5
        #
        # print(first_x, first_y)
        # print(mouse_x, mouse_y)
        # print('===')

    def rect_check(self, *obj):
        second_pos, desk_rect, screen_size, player, first_pos, cubes = obj
        fx, fy = self.which_pos(first_pos, desk_rect, screen_size, player, boolean=True, first_pos=True)
        sx, sy = self.which_pos(second_pos, desk_rect, screen_size, player, boolean=True, first_pos=True)
        first_i, second_i, step_i = revolution_settings(fx, sx)
        first_j, second_j, step_j = revolution_settings(fy, sy)

        count_x, count_y = 0, 0

        check_for_another_square = False

        for i in range(first_i, second_i, step_i):
            if -1 < i < len(self.board):
                count_x += 1
                for j in range(first_j, second_j, step_j):
                    if -1 < j < len(self.board):
                        count_y += 1
                        if self.checklist(i, j):
                            check_for_another_square = True
                        if -1 < i + 1 < len(self.board):
                            if self.board[i + 1][j] == player:
                                check_for_another_square = True
                        if -1 < i - 1 < len(self.board):
                            if self.board[i - 1][j] == player:
                                check_for_another_square = True
                        if -1 < j + 1 < len(self.board):
                            if self.board[i][j + 1] == player:
                                check_for_another_square = True
                        if -1 < j - 1 < len(self.board):
                            if self.board[i][j - 1] == player:
                                check_for_another_square = True
        if count_x == 0:
            return False
        count_y //= count_x
        print(((count_y == cubes[0] and count_x == cubes[1]) or (
                count_x == cubes[0] and count_y == cubes[1])) and check_for_another_square)
        print('---------')
        if ((count_y == cubes[0] and count_x == cubes[1]) or (
                count_x == cubes[0] and count_y == cubes[1])) and check_for_another_square:
            return True
        return False

    def checklist(self, x, y):
        if (x == 0 and y == 0) or (x == len(self.board) - 1 and y == len(self.board[0]) - 1):
            return True
        return False

    def win_check(self):
        player_red, player_blue, void, winner = 0, 0, 0, 0
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 1:
                    player_red += 1
                if self.board[i][j] == 2:
                    player_blue += 1
                if self.board[i][j] == 0:
                    void += 1
        if void <= abs(player_red - player_blue):
            if player_red > player_blue:
                winner = 1
            elif player_blue > player_red:
                winner = 2
            else:
                winner = -1
        if winner == 1:
            return True, (255, 0, 0)
        elif winner == 2:
            return True, (0, 0, 255)
        elif winner == -1:
            return True, (40, 40, 40)
        else:
            return False, None

    def undefined_rect_paste(self, how_much=-1):
        if how_much == -1:
            for i in range(len(self.board)):
                for j in range(len(self.board[0])):
                    if self.board[i][j] == 1.5:
                        self.board[i][j] = 1
                    if self.board[i][j] == 2.5:
                        self.board[i][j] = 2


# def temp(self, player, pos):
#     self.board[pos[0]][pos[1]] = player


class BackgroundAnim:
    def __init__(self, screen_size):
        self.geometry_list = []  # 0-цвет 1 2 расположение 3 размер 4 цикл увелич уменьш true false 5 размер макс
        self.temp_frame = 0
        self.width, self.height = screen_size

    def render(self, sc):
        # кубики
        del_list = []
        self.temp_frame += 1
        if self.temp_frame == 30:
            self.temp_frame = 0
            red_c = random.randint(0, 245)
            self.geometry_list.append([(10 + red_c, 10 + random.randint(0, 10),
                                        255 - red_c), random.randint(50, self.width - 50),
                                       random.randint(50, self.height - 50), 0, True, 100])
        for c in range(len(self.geometry_list)):
            if self.geometry_list[c][3] <= 1 and not self.geometry_list[c][4]:
                del_list.append(c)
            else:
                pygame.draw.rect(sc, self.geometry_list[c][0], (round(self.geometry_list[c][1]),
                                                                round(self.geometry_list[c][2]),
                                                                round(self.geometry_list[c][3]),
                                                                round(self.geometry_list[c][3])))
                if not self.geometry_list[c][4]:
                    self.geometry_list[c][1] += 0.2
                    self.geometry_list[c][2] += 0.2
                    self.geometry_list[c][3] -= 0.4
                if self.geometry_list[c][3] >= self.geometry_list[c][5]:
                    self.geometry_list[c][4] = False
                elif self.geometry_list[c][4]:
                    self.geometry_list[c][1] -= 0.2
                    self.geometry_list[c][2] -= 0.2
                    self.geometry_list[c][3] += 0.4
        for c in range(len(del_list)):
            del self.geometry_list[c]


class Mouse:
    def __init__(self):
        self.pos = (0, 0)

        self.default_image = sprites.mouse.image
        self.clicked_image = sprites.mouse_clicked.image

        self.clicked_bool = False

    def change_pos(self, pos):
        self.pos = pos

    def clicked(self):
        self.clicked_bool = True

    def unclicked(self):
        self.clicked_bool = False

    def render(self, screen):
        if self.clicked_bool:
            screen.blit(self.clicked_image, self.pos)
        else:
            screen.blit(self.default_image, self.pos)


class Widget:
    def __init__(self, pos, text, pressed=False):
        self.x, self.y = pos
        self.pos = pos
        self.size = (None, None)
        self.pressed = pressed
        self.crossed = False
        self.text = text
        self.font = pygame.font.Font(None, 25)

    def press(self):
        self.pressed = True

    def crossing(self):
        if not self.pressed:
            self.crossed = True

    def check(self, mousepos):
        return func.crossing((self.x, self.y, self.size[0], self.size[1]), mousepos, full=True)

    def unpress(self):
        self.pressed = False


class Button(Widget):
    def __init__(self, pos, text, pressed=False, size=(250, 50)):
        super().__init__(pos, text, pressed=pressed)
        self.size = self.width, self.height = size[0], size[1]

    def render(self, screen):
        if self.pressed:
            color = (255, 255, 255)
            pygame.draw.rect(screen, (170, 170, 170), (self.pos[0], self.pos[1], self.size[0], self.size[1]))
        else:
            if self.crossed:
                color = (255, 255, 255)
                pygame.draw.rect(screen, (0, 0, 0), (self.pos[0], self.pos[1], self.size[0], self.size[1]))
            else:
                color = (0, 0, 0)
                pygame.draw.rect(screen, (40, 40, 40), (self.pos[0], self.pos[1], self.size[0], self.size[1]))
        screen.blit(self.font.render(self.text, True, color), (self.pos[0] + 17, self.pos[1] + 17))
