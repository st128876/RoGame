import copy
import math
import pygame
from generalOptions import *


class Ray():
    def __init__(self, angel, lenght):
        self.start_x = SCREEN_WIDTH // 2
        self.start_y = SCREEN_HEIGHT // 2
        self.angel = angel
        self.lenght = lenght
        self.rayCasting()

    ''' получаем угол в который смотрит персонаж, выпускаем по 100(условно) лучей с каждой стороны по +- 0.4 радиана
    TODO: распаралелить вычисления на видеокарте '''

    def rayCasting(self):
        self.end_x = math.cos(math.radians(self.angel)) * self.lenght + (SCREEN_WIDTH // 2)
        self.end_y = math.sin(math.radians(self.angel)) * self.lenght + (SCREEN_HEIGHT // 2)

    def draw(self, screen):
        pygame.draw.line(screen, (255, 255, 0, 100), (self.start_x, self.start_y), (self.end_x, self.end_y), 1)


def collision_light(scren, sprits, dot, v_or_h=''):
    image = pygame.Surface((5, 5))
    image.fill((255, 0, 0))
    rect = image.get_rect()
    rect.center = (dot[0], dot[1] - 2)
    for obj in sprits:
        if rect.colliderect(obj.give_rect()):
            if v_or_h == 'v':
                image1 = pygame.Surface((5, 5))
                image1.fill((150, 150, 150))
                rect1 = image1.get_rect()
                rect1.center = (dot[0] + 30, dot[1] - 2)

                flag_rect1 = False
                for obj1 in sprits:
                    if rect1.colliderect(obj1):
                        flag_rect1 = True
                        break


                image2 = pygame.Surface((5, 5))
                image2.fill((150, 150, 150))
                rect2 = image2.get_rect()
                rect2.center = (dot[0] - 30, dot[1] - 2)

                flag_rect2 = False
                for obj2 in sprits:
                    if rect2.colliderect(obj2):
                        flag_rect2 = True
                        break

                if flag_rect1 and flag_rect2:
                    return False
                else:
                    return True

            if v_or_h == 'h':
                image1 = pygame.Surface((5, 5))
                image1.fill((150, 150, 150))
                rect1 = image1.get_rect()
                rect1.center = (dot[0], dot[1] - 2 + 30)

                flag_rect1 = False
                for obj1 in sprits:
                    if rect1.colliderect(obj1):
                        flag_rect1 = True
                        break

                image2 = pygame.Surface((5, 5))
                image2.fill((150, 150, 150))
                rect2 = image2.get_rect()
                rect2.center = (dot[0], dot[1] - 2 - 30)

                flag_rect2 = False
                for obj2 in sprits:
                    if rect2.colliderect(obj2):
                        flag_rect2 = True
                        break

                if flag_rect1 and flag_rect2:
                    return False
                else:
                    return True
            return True
    return False


def ray_casting(screen, angel, visible_obj, power, st_x, st_y, x_t, y_t):
    if angel > 180:
        angel = angel - 360
    if angel < -180:
        angel = angel + 360

    for_x_t = ((((st_x - x_t) // 50) + 1) * 50 + x_t)
    for_y_t = (((st_y - y_t - 8) // 50) + 1) * 50 + y_t + 8

    self_image = pygame.Surface((5, 5))
    self_image.fill((0, 255, 0))
    self_rect = self_image.get_rect()  # Получаем прямоугольник для объектов
    self_rect.center = (for_x_t, for_y_t)
    screen.blit(self_image, self_rect)

    print(angel)
    flag_v = False
    vertical_dots = ()
    xi = 1
    while xi < 8 and not (flag_v):
        if angel > -90 and angel < 90:
            x_current = for_x_t + (xi * 50) - 50
            y_current = math.tan(math.radians(angel)) * (x_current - st_x) + st_y

            flag_v = collision_light(screen, visible_obj, (x_current, y_current), 'v')
            if flag_v and abs(x_current - st_x) > 4:
                vertical_dots = (x_current, y_current)
            else:
                flag_v = False

            # self_image = pygame.Surface((5, 5))
            # self_image.fill((74, 220, 236))
            # self_rect = self_image.get_rect()  # Получаем прямоугольник для объектов
            # self_rect.center = (x_current, y_current)
            # screen.blit(self_image, self_rect)

        else:
            x_current = for_x_t - (xi * 50)
            y_current = math.tan(math.radians(angel)) * (x_current - st_x) + st_y

            flag_v = collision_light(screen, visible_obj, (x_current, y_current), 'v')
            if flag_v and abs(x_current - st_x) > 4:
                vertical_dots = (x_current, y_current)
            else:
                flag_v = False

            # self_image = pygame.Surface((5, 5))
            # self_image.fill((74, 220, 236))
            # self_rect = self_image.get_rect()  # Получаем прямоугольник для объектов
            # self_rect.center = (x_current, y_current)
            # screen.blit(self_image, self_rect)
        xi += 1

    flag_h = False
    horizontal_dots = ()
    yi = 1
    while yi < 8 and not (flag_h):
        if angel > -180 and angel < 0:
            y_current = for_y_t - (yi * 50) - 50
            x_current = (y_current - st_y) / math.tan(math.radians(angel)) + st_x

            flag_h = collision_light(screen, visible_obj, (x_current, y_current), 'h')
            if flag_h and abs(y_current - st_y) > 4:
                horizontal_dots = (x_current, y_current)
            else:
                flag_h = False

            # self_image = pygame.Surface((5, 5))
            # self_image.fill((74, 220, 236))
            # self_rect = self_image.get_rect()  # Получаем прямоугольник для объектов
            # self_rect.center = (x_current, y_current)
            # screen.blit(self_image, self_rect)

        else:
            y_current = for_y_t + (yi * 50) - 50
            x_current = (y_current - st_y) / (math.tan(math.radians(angel) + 0.0000001)) + st_x

            flag_h = collision_light(screen, visible_obj, (x_current, y_current), 'h')
            if flag_h and abs(y_current - st_y) > 4:
                horizontal_dots = (x_current, y_current)
            else:
                flag_h = False

            # self_image = pygame.Surface((5, 5))
            # self_image.fill((74, 220, 236))
            # self_rect = self_image.get_rect()  # Получаем прямоугольник для объектов
            # self_rect.center = (x_current, y_current)
            # screen.blit(self_image, self_rect)
        yi += 1

    # image = pygame.Surface((5, 5))
    # image.fill((255, 10, 10))
    # rect = image.get_rect()
    # try:
    #     rect.center = (horizontal_dots[0], horizontal_dots[1])
    #     screen.blit(image, rect)
    # except:
    #     pass
    # try:
    #     rect.center = (vertical_dots[0], vertical_dots[1])
    #     screen.blit(image, rect)
    # except:
    #     pass

    try:
        image = pygame.Surface((5, 5))
        image.fill((255, 10, 10))
        rect = image.get_rect()
        if (math.sqrt(((vertical_dots[0] - (st_x)) ** 2) + ((vertical_dots[1] - (
                st_y)) ** 2))) < (
                math.sqrt(((horizontal_dots[0] - (st_x)) ** 2) + (
                        (horizontal_dots[1] - (st_y)) ** 2))):

            all_light_dots = vertical_dots
            power += (math.sqrt(((vertical_dots[0] - (st_x)) ** 2) + ((vertical_dots[1] - (
                st_y)) ** 2)))
            v_or_h = 'v'

        else:
            all_light_dots = horizontal_dots
            power += (math.sqrt(((horizontal_dots[0] - (st_x)) ** 2) + (
                    (horizontal_dots[1] - (st_y)) ** 2)))
            v_or_h = 'h'

        rect.center = (all_light_dots[0], all_light_dots[1])
        pygame.draw.line(screen, (255, 255, 0), (st_x, st_y), all_light_dots, 1)
        screen.blit(image, rect)
        if power <= 400:
            if v_or_h == 'v':
                ray_casting(screen, (180 - angel), visible_obj, power, vertical_dots[0], vertical_dots[1],
                            (x_t) % 50, ((y_t)) % 50)
            else:
                ray_casting(screen, (-angel), visible_obj, power, horizontal_dots[0], horizontal_dots[1],
                            (x_t) % 50, ((y_t)) % 50)

    except:
        if horizontal_dots == () and vertical_dots != ():
            all_light_dots = vertical_dots
            rect.center = (all_light_dots[0], all_light_dots[1])
            screen.blit(image, rect)
            pygame.draw.line(screen, (255, 255, 0), (st_x, st_y), all_light_dots, 1)
            power += (math.sqrt(((vertical_dots[0] - (st_x)) ** 2) + ((vertical_dots[1] - (
                st_y)) ** 2)))
            if power <= 400:
                ray_casting(screen, (180 - angel), visible_obj, power, vertical_dots[0], vertical_dots[1],
                            (x_t), (y_t))

        if horizontal_dots != () and vertical_dots == ():
            all_light_dots = horizontal_dots
            rect.center = (all_light_dots[0], all_light_dots[1])
            screen.blit(image, rect)
            pygame.draw.line(screen, (255, 255, 0), (st_x, st_y), all_light_dots, 1)
            power += (math.sqrt(((horizontal_dots[0] - (st_x)) ** 2) + ((horizontal_dots[1] - (
                st_y)) ** 2)))
            if power <= 400:
                ray_casting(screen, (-angel), visible_obj, power, horizontal_dots[0], horizontal_dots[1],
                            (x_t), (y_t))



def network(scren, x_t, y_t, angel, visible_obj, power):
    all_light_dots = []
    x_t = x_t % 50
    y_t = y_t % 50
    while x_t < 1200:
        pygame.draw.line(scren, (255, 0, 255, 100), (x_t, 0), (x_t, 720), 1)
        x_t += 50
    while y_t < 1200:
        pygame.draw.line(scren, (255, 0, 255, 100), (0, y_t), (1200, y_t), 1)
        y_t += 50

    flag_v = False
    vertical_dots = []
    xi = 0
    while xi < 8 and not (flag_v):
        if angel >= -90 and angel <= 90:
            x_s = ((x_t % 50) + (xi * 50))
            x = x_s + (SCREEN_WIDTH // 2)
            y = (math.tan(math.radians(angel)) * x_s) + (SCREEN_HEIGHT // 2)

            flag_v = collision_light(scren, visible_obj, (x, y), 'v')
            if flag_v:
                vertical_dots.append((x, y))
        else:
            x_s = ((x_t % 50) - (xi * 50)) - 50
            x = x_s + (SCREEN_WIDTH // 2)
            y = (math.tan(math.radians(angel)) * x_s) + (SCREEN_HEIGHT // 2)

            flag_v = collision_light(scren, visible_obj, (x, y), 'v')
            if flag_v:
                vertical_dots.append((x, y))
        xi += 1

    horizontal_dots = []
    flag_h = False
    yi = 0
    while yi < 8 and not (flag_h):
        if angel > -180 and angel < 0:
            y_s = (((y_t - 8) % 50) - (yi * 50)) - 50
            y = y_s + (SCREEN_HEIGHT // 2)
            x = (y_s / math.tan(math.radians(angel))) + (SCREEN_WIDTH // 2)

            flag_h = collision_light(scren, visible_obj, (x, y), 'h')
            if flag_h:
                horizontal_dots.append((x, y))

        elif angel > 0 and angel < 180:
            y_s = (((y_t - 8) % 50) + (yi * 50))
            y = y_s + (SCREEN_HEIGHT // 2)
            x = (y_s / math.tan(math.radians(angel))) + (SCREEN_WIDTH // 2)

            flag_h = collision_light(scren, visible_obj, (x, y), 'h')
            if flag_h:
                horizontal_dots.append((x, y))
        yi += 1

    # image = pygame.Surface((5, 5))
    # image.fill((255, 10, 10))
    # rect = image.get_rect()
    # try:
    #     rect.center = horizontal_dots[0]
    #     scren.blit(image, rect)
    # except:
    #     pass
    # try:
    #     rect.center = vertical_dots[0]
    #     scren.blit(image, rect)
    # except:
    #     pass



    try:
        image = pygame.Surface((5, 5))
        image.fill((255, 10, 10))
        rect = image.get_rect()

        if (math.sqrt(((vertical_dots[0][0] - (SCREEN_WIDTH // 2)) ** 2) + ((vertical_dots[0][1] - (
                SCREEN_HEIGHT // 2)) ** 2))) < (
                math.sqrt(((horizontal_dots[0][0] - (SCREEN_WIDTH // 2)) ** 2) + (
                        (horizontal_dots[0][1] - (SCREEN_HEIGHT // 2)) ** 2))):
            all_light_dots.append(vertical_dots[0])
            power += (math.sqrt(((vertical_dots[0][0] - (SCREEN_WIDTH // 2)) ** 2) + ((vertical_dots[0][1] - (
                    SCREEN_HEIGHT // 2)) ** 2)))
            v_or_h = 'v'
        else:
            all_light_dots.append(horizontal_dots[0])
            power += (math.sqrt(((horizontal_dots[0][0] - (SCREEN_WIDTH // 2)) ** 2) + (
                    (horizontal_dots[0][1] - (SCREEN_HEIGHT // 2)) ** 2)))
            v_or_h = 'h'
        rect.center = (all_light_dots[0][0], all_light_dots[0][1])
        # scren.blit(image, rect)
        pygame.draw.line(scren, (255, 255, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), (all_light_dots[0]), 1)
        if power <= 400:
            if v_or_h == 'v':
                ray_casting(scren, (180 - angel), visible_obj, power, vertical_dots[0][0], vertical_dots[0][1],
                            (x_t) % 50, ((y_t - 8)) % 50)
            else:
                ray_casting(scren, (-angel), visible_obj, power, horizontal_dots[0][0], horizontal_dots[0][1],
                            (x_t) % 50, ((y_t - 8)) % 50)\


    except:
        if horizontal_dots == [] and vertical_dots != []:
            all_light_dots.append(vertical_dots[0])
            rect.center = (all_light_dots[0][0], all_light_dots[0][1])
            scren.blit(image, rect)
            pygame.draw.line(scren, (255, 255, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), (all_light_dots[0]), 1)
            power += (math.sqrt(((vertical_dots[0][0] - (SCREEN_WIDTH // 2)) ** 2) + ((vertical_dots[0][1] - (
                    SCREEN_HEIGHT // 2)) ** 2)))
            if power <= 400:
                ray_casting(scren, (180 - angel), visible_obj, power, vertical_dots[0][0], vertical_dots[0][1],
                            (x_t) % 50, ((y_t - 8)) % 50)
        elif vertical_dots == [] and horizontal_dots != []:
            all_light_dots.append(horizontal_dots[0])
            rect.center = (all_light_dots[0][0], all_light_dots[0][1])
            scren.blit(image, rect)
            pygame.draw.line(scren, (255, 255, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), (all_light_dots[0]), 1)
            power += (math.sqrt(((horizontal_dots[0][0] - (SCREEN_WIDTH // 2)) ** 2) + (
                    (horizontal_dots[0][1] - (SCREEN_HEIGHT // 2)) ** 2)))
            if power <= 400:
                ray_casting(scren, (-angel), visible_obj, power, horizontal_dots[0][0], horizontal_dots[0][1],
                            (x_t) % 50, ((y_t - 8)) % 50)
