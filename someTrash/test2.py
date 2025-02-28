import pygame
import math
import random

# Инициализация Pygame
pygame.init()

# Задаем размеры экрана
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Луч на мышку с квадратом")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Размер квадрата
square_size = 50

# Генерация случайной позиции квадрата при старте
square_x = random.randint(0, screen_width - square_size)
square_y = random.randint(0, screen_height - square_size)

# Главный цикл программы
running = True
while running:
    # Обрабатываем события
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Получаем позицию мыши
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Рассчитываем координаты центра экрана
    center_x = screen_width // 2
    center_y = screen_height // 2

    # Вычисляем угол между центром экрана и мышью
    dx = mouse_x - center_x
    dy = mouse_y - center_y
    angle = math.atan2(dy, dx)

    # Длина луча
    ray_length = min(screen_width, screen_height)

    # Рассчитываем конечную точку луча
    end_x = center_x + ray_length * math.cos(angle)
    end_y = center_y + ray_length * math.sin(angle)

    # Отображаем все на экране
    screen.fill(BLACK)  # Заполняем экран черным цветом
    pygame.draw.line(screen, WHITE, (center_x, center_y), (end_x, end_y), 2)  # Рисуем луч
    pygame.draw.rect(screen, RED, (square_x, square_y, square_size, square_size))  # Рисуем квадрат

    # Обновляем экран
    pygame.display.flip()

# Закрытие Pygame
pygame.quit()
