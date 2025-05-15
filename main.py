import copy
import math
from shapely.geometry import Polygon

import pygame
import random
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import ray

import generalOptions

from strike import SwordPush, Bullet
from enemy import Enemy
from StateObj import Walls
from RayCasting import network
from Menu import Button, MainMenu

# Инициализация Pygame
pygame.init()

# Размеры экрана
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption("Мир вокруг игрока")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


from MapGenerator import type1  # Импортируем функцию генерации карты

def save_modified_map_to_file():
    # Получаем сгенерированную карту
    game_map = type1()

    # Вырезаем угол 4x4 (заменяем на пробелы)
    for y in range(min(4, len(game_map))):
        for x in range(min(4, len(game_map[0]))):
            game_map[y][x] = ' '

    # Сохраняем в файл
    # print(game_map)
    with open("Maps/level_zero.txt", "w") as f:
        for row in game_map:
            f.write(''.join(row) + '\n')


save_modified_map_to_file()

# ray.init()


# Скорость движения


# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Создание изображения игрока (круг)
        self.image = pygame.Surface((16, 16), pygame.SRCALPHA)  # Прозрачное изображение размером 16x16
        pygame.draw.circle(self.image, (0, 0, 255), (8, 8), 8)  # Рисуем круг с радиусом 8 пикселей
        self.rect = self.image.get_rect()  # Получаем прямоугольник, который будет использоваться для обработки столкновений
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # Устанавливаем игрока в центр экрана

    def draw(self, screen):
        # Рисуем игрока в центре экрана
        screen.blit(self.image, self.rect)


class Light(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Создаем поверхность для треугольника
        self.triangle_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.triangle_surface.fill((0, 0, 0, 0))  # Прозрачный фон

    def flashlight(self, center, angle, triangle_height=900, triangle_base=200):
        # Угол в радианах
        self.rad = math.radians(angle)
        # print((self.rad * (180 / math.pi)) % 360)

        # Вершина треугольника (центр)
        self.p1 = center  # Верхняя вершина (центр)

        # Левый и правый углы
        self.p2 = (center[0] - triangle_base / 2, center[1] + triangle_height / 2)
        self.p3 = (center[0] + triangle_base / 2, center[1] + triangle_height / 2)

        # Поворот вершин p2 и p3
        self.points = [self.p1, self.p2, self.p3]
        self.rotated_points = []
        for self.point in self.points:
            if self.point == self.p1:  # Если это центр, не поворачиваем
                self.rotated_points.append(self.point)
                continue

            # Поворот вокруг центра

            self.x = self.point[0] - center[0]
            self.y = self.point[1] - center[1]
            self.new_x = self.x * math.cos(self.rad) - self.y * math.sin(self.rad)
            self.new_y = self.x * math.sin(self.rad) + self.y * math.cos(self.rad)
            self.rotated_points.append((self.new_x + center[0], self.new_y + center[1]))

        return self.rotated_points

    # Функция для отрисовки вращающегося треугольника
    def draw_flashlight(self, screen, t_height, base, alph):
        self.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        # Получаем позицию мыши
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

        # Вычисляем угол поворота
        self.angle = math.degrees(math.atan2(self.mouse_y - self.center[1], self.mouse_x - self.center[0]) - 1.603599)
        # print(self.angle)

        # Получаем координаты треугольника
        self.triangle_points = self.flashlight(self.center, self.angle, t_height, base)

        # Рисуем треугольник на поверхности
        pygame.draw.polygon(self.triangle_surface, (255, 230, 181), self.triangle_points)

        # Устанавливаем уровень прозрачности
        self.triangle_surface.set_alpha(alph)  # Полупрозрачный (0-255)

        # Отрисовка
        screen.blit(self.triangle_surface, (0, 0))
        pygame.display.flip()

    def give_flash_coordination(self):
        self.given_points = [(int(self.pt[0]), int(self.pt[1])) for self.pt in self.triangle_points]
        return self.given_points

    def give_angel(self):
        return (((self.rad * (180 / math.pi)) % 360) > 180)


def check_intersection(triangle_points, square_points):
    """
    Проверяет, пересекаются ли треугольник и квадрат.
    :param triangle_points: список из 3 кортежей (x, y) - координаты вершин треугольника
    :param square_points: список из 4 кортежей (x, y) - координаты вершин квадрата
    :return: True, если есть пересечение, иначе False
    """
    triangle = Polygon(triangle_points)
    square = Polygon(square_points)

    return triangle.intersects(square)


menu = MainMenu(screen)


# Основная функция игры
def main():
    while generalOptions.menu_flag:
        menu.run()

    clock = pygame.time.Clock()  # Для контроля частоты кадров

    # Создаем игрока
    player = Player()

    bullets_some = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    all_objects_on_map_now = pygame.sprite.Group()

    player_bullet_time = 0

    first_enemy = Enemy(800, 200)
    enemies.add(first_enemy)

    xwall = 0
    for str_of_wall in open('Maps/level_zero.txt'):
        xwall += 1
        ywall = 0
        for obj_in_str in str_of_wall:
            ywall += 1
            if obj_in_str == 'x':
                all_objects_on_map_now.add(Walls(xwall * 50 + 500, ywall * 50 + 300))

    # Главный игровой цикл
    running = True
    ticks = 0
    bullets_death = []
    while running:
        screen.fill(BLACK)  # Очистка экрана

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Если закрываем окно, завершить игру
                running = False

        # Движение игрока (сдвиг мира)
        keys = pygame.key.get_pressed()  # Получаем все нажатые клавиши

        if keys[pygame.K_a]:  # Двигаемся влево
            generalOptions.x_to_left = generalOptions.move_speed_player
            generalOptions.x_to_right = 0
        elif keys[pygame.K_d]:  # Двигаемся вправо
            generalOptions.x_to_right = generalOptions.move_speed_player
            generalOptions.x_to_left = 0
        else:
            generalOptions.x_to_right = 0
            generalOptions.x_to_left = 0

        if keys[pygame.K_w]:  # Двигаемся вверх
            generalOptions.y_to_up = generalOptions.move_speed_player
            generalOptions.y_to_down = 0
        elif keys[pygame.K_s]:  # Двигаемся вниз
            generalOptions.y_to_down = generalOptions.move_speed_player
            generalOptions.y_to_up = 0
        else:
            generalOptions.y_to_down = 0
            generalOptions.y_to_up = 0

        if keys[pygame.K_SPACE]:
            generalOptions.move_speed_player = 6
        else:
            generalOptions.move_speed_player = 4

        # Отображаем объекты\

        may_be_visible = pygame.sprite.Group()
        for obj in all_objects_on_map_now:
            if obj.give_centre()[0] > 0 and obj.give_centre()[0] < 1200:
                if obj.give_centre()[1] > 0 and obj.give_centre()[1] < 720:
                    may_be_visible.add(obj)
                    obj.draw(screen)
                    obj.collision(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, player, screen)

        # for obj in may_be_visible:
        # obj.draw(screen)
        # obj.collision(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, player, screen)a

        for obj in all_objects_on_map_now:  # Обновляем объекты в мире
            obj.update(generalOptions.x_to_right, generalOptions.x_to_left, generalOptions.y_to_up,
                       generalOptions.y_to_down)

        if pygame.mouse.get_pressed()[0]:  # Проверяем, нажата ли левая кнопка мыши
            if ticks - player_bullet_time >= 50:
                mouse_x, mouse_y = pygame.mouse.get_pos()  # Получаем позицию мыши
                bullet = Bullet(player.rect.centerx, player.rect.centery, mouse_x, mouse_y, 13)
                bullets_some.add(bullet)
                bullets_death.append(ticks)
                player_bullet_time = ticks

        # Обновляем и рисуем пули
        for bullet in bullets_some:
            bullet.update()  # Обновляем положение пули
            bullet.draw(screen)  # Рисуем пулю

        bullets_death_amount = 0
        for bullet in range(len(bullets_death)):
            if ticks - bullets_death[bullet] >= 60:  # время жизни пули
                bullets_some.remove(bullets_some.sprites()[0])
                bullets_death_amount += 1

        # проверка на попадание пули во врага
        for bullet in bullets_some:
            for en in enemies:
                if en.damage_to_yourself(bullet.give_coordinatoin()[0], bullet.give_coordinatoin()[1]):
                    print('death')
                    enemies.remove(en)

        for r in range(bullets_death_amount):
            del bullets_death[0]

        # отрисовка врагов
        for en in enemies:
            en.update(generalOptions.x_to_right, generalOptions.x_to_left, generalOptions.y_to_up,
                      generalOptions.y_to_down)
            en.draw(screen)
            # en.visor_line(screen)

        player.draw(screen)  # Игрок всегда рисуется в центре экрана
        # strong_light = Light()
        # midle_light = Light()
        # week_light = Light()

        # strong_light.draw_flashlight(screen, 900, 230, 80)
        # midle_light.draw_flashlight(screen, 900 * 1.1, 230 * 1.5, 60)
        # week_light.draw_flashlight(screen, 900 * 1.1 * 1.1, 230 * 1.5 * 1.5, 40)
        # print(len(may_be_visible), all_objects_on_map_now)

        # fo_light_rect = pygame.Surface((100, 100))
        # light_rect = fo_light_rect.get_rect()
        # light_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        # for obj in may_be_visible:
        #     if check_intersection(week_light.give_flash_coordination(),
        #                           obj.give_coordinations_wall()) or light_rect.colliderect(obj.give_rect()):
        #         obj.draw(screen)

        # dist_to_net = network(screen, may_be_visible.sprites()[0].give_centre()[0], may_be_visible.sprites()[0].give_centre()[1])

        mouse_x, mouse_y = pygame.mouse.get_pos()
        # print(mouse_x - (SCREEN_WIDTH // 2), mouse_y - (SCREEN_HEIGHT // 2))

        # Вычисляем угол поворота
        angel = math.degrees(math.atan2(mouse_y - (SCREEN_HEIGHT // 2), mouse_x - (SCREEN_WIDTH // 2)))
        for r in range(-15, 15):
            try:
                network(screen, may_be_visible.sprites()[0].give_centre()[0], may_be_visible.sprites()[0].give_centre()[1], angel + (r * 1), may_be_visible, 0)
            except:
                pass


        # angel = math.degrees(math.atan2(mouse_y - (SCREEN_HEIGHT // 2), mouse_x - (SCREEN_WIDTH // 2)))
        # try:
        #     with ProcessPoolExecutor() as executor:
        #         [executor.submit(network, screen,
        #                          may_be_visible.sprites()[0].give_centre()[0],
        #                          may_be_visible.sprites()[0].give_centre()[1],
        #                          angel + (r * 0.5),
        #                          may_be_visible,
        #                          0)
        #          for r in range(-40, 40)]
        # except:
        #     pass

        # Обновление экрана
        pygame.display.flip()

        fps = clock.get_fps()
        pygame.display.set_caption(f'fps:{fps}')

        ticks += 1

        # Ограничение кадров в секунду
        clock.tick(60)  # 60 кадров в секунду

        if keys[pygame.K_ESCAPE]:
            generalOptions.menu_flag = True
            while generalOptions.menu_flag:
                menu.run()

        # print(bullets_death)
    pygame.quit()  # Завершаем работу Pygame
    # ray.shutdown()


# Запуск игры
if __name__ == "__main__":
    main()
