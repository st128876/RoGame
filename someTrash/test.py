import pygame
import math
import sys

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Выстрелы из центра")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Центр экрана
center_x, center_y = WIDTH // 2, HEIGHT // 2

# Получаем углы с консоли
angle1 = float(input("Введите первый угол в градусах: "))
angle2 = float(input("Введите второй угол в градусах: "))

# Преобразуем углы в радианы
angle1_rad = math.radians(angle1)
angle2_rad = math.radians(angle2)

# Длина луча
ray_length = 300

# Главный цикл игры
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Заполнение экрана белым
    screen.fill(WHITE)

    # Рисуем два луча
    # Первый луч
    x1 = center_x + ray_length * math.cos(angle1_rad)
    y1 = center_y + ray_length * math.sin(angle1_rad)
    pygame.draw.line(screen, BLACK, (center_x, center_y), (x1, y1), 2)

    # Второй луч
    x2 = center_x + ray_length * math.cos(angle2_rad)
    y2 = center_y + ray_length * math.sin(angle2_rad)
    pygame.draw.line(screen, BLACK, (center_x, center_y), (x2, y2), 2)

    # Обновляем экран
    pygame.display.flip()

    # Ограничение FPS
    pygame.time.Clock().tick(60)

# Закрытие Pygame
pygame.quit()
sys.exit()
