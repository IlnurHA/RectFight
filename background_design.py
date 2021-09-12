import pygame
import os
import random


pygame.init()

FPS = 60
width, height = size = 1200, 800
running = True
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height), 0)
x, y, a, b = 0, 0, 0, 0
pygame.mouse.set_visible(0)
pygame.display.set_caption('BG for ilnur)))')


def load_image(name, colorkey=pygame.Color('brown')):
    fullname = os.path.join('sprites', name)
    image = pygame.image.load(fullname)
    image.set_colorkey(colorkey)
    return image


mouse = pygame.sprite.Sprite()
mouse.image = load_image('arrow.png')


class BackgroundAnim:
    def __init__(self):
        self.geometry_list = []    # 0-цвет 1 2 расположение 3 размер 4 цикл увелич уменьш true false 5 размер макс
        self.temp_frame = 0

    def render(self, sc):
        # кубики
        del_list = []
        self.temp_frame += 1
        if self.temp_frame == 30:
            self.temp_frame = 0
            red_c = random.randint(0, 245)
            self.geometry_list.append([(10 + red_c, 10 + random.randint(0, 10),
                                        255 - red_c), random.randint(50, width - 50),
                                       random.randint(50, height - 50), 0, True, 100])
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


def turn_accept_anim(sc, color, delta_fps=1):
    global width, clock
    xm = 0
    for c in range(30):
        sc.fill((40, 40, 40))
        xm += 50
        pygame.draw.polygon(sc, (40, 40, 40),
                            [(xm + 50, height // 2), (xm + width + 50, height // 2), (xm + width, 0), (xm, 0)])
        pygame.display.flip()
        clock.tick(FPS)


bg = BackgroundAnim()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.MOUSEMOTION:
            a, b = event.pos
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            turn_accept_anim(screen, (255, 0, 0))
    screen.fill((0, 0, 0))
    bg.render(screen)

    if pygame.mouse.get_focused():
        screen.blit(mouse.image, (a, b))
    pygame.display.flip()
    clock.tick(FPS)
