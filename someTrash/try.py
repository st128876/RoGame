import pygame
import math

# Инициализация Pygame
pygame.init()

# Размеры экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Летящий мяч")

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Параметры мяча
ball_radius = 5
ball_speed = 5

# Класс для мяча
class Ball:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (self.x, self.y), ball_radius)

# Главный цикл игры
running = True
clock = pygame.time.Clock()

# Центр экрана
center_x, center_y = WIDTH // 2, HEIGHT // 2

# Мяч, который будет лететь
ball = None

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Получаем координаты мышки
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Рассчитываем направление для мяча
            dx = mouse_x - center_x
            dy = mouse_y - center_y
            distance = math.sqrt(dx**2 + dy**2)

            # Нормализуем вектор
            dx /= distance
            dy /= distance

            # Создаем мяч
            ball = Ball(center_x, center_y, dx * ball_speed, dy * ball_speed)

    # Рисуем круг в центре
    pygame.draw.circle(screen, (0, 0, 255), (center_x, center_y), 20)

    # Если мяч существует, перемещаем и рисуем его
    if ball:
        ball.move()
        ball.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
