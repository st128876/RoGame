import math
import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, some_enemy_x, some_enemy_y):
        super().__init__()

        self.image = pygame.Surface((10, 10))  # Прямоугольник 30x30 пикселей
        self.image.fill((255, 0, 0))  # Заливка белым цветом
        self.rect = self.image.get_rect()  # Получаем прямоугольник для объектов
        self.rect.center = (some_enemy_x, some_enemy_y)

        self.health = 100
        self.death = False

    def update(self, x_to_right, x_to_left, y_to_up, y_to_down):
        self.rect.x -= x_to_right
        self.rect.x += x_to_left

        self.rect.y += y_to_up
        self.rect.y -= y_to_down

    def move(self, player_x, player_y, speed=4):
        distance = math.hypot(player_x, player_y)
        # Нормализуем вектор
        self.dx = player_x / distance * speed
        self.dy = player_y / distance * speed

    def damage_to_yourself(self, hit_x, hit_y, radius_hit=12):
        if ((hit_x - self.rect.x) ** 2) + ((hit_y - self.rect.y) ** 2) <= (radius_hit ** 2):
            self.health -= 50
            if self.health <= 0:
                self.death = True
        return self.death

    def draw(self, screen):
        # Рисуем объект на экране
        screen.blit(self.image, self.rect)

    def visor_line(self, screen):
        for self.angel_visor in range(0, 360, 10):

            self.end_pos_for_tic_x = self.rect.center[0] + (170) * math.cos(math.radians(self.angel_visor))
            self.end_pos_for_tic_y = self.rect.center[1] + (170) * math.sin(math.radians(self.angel_visor))

            pygame.draw.line(screen, (255, 255, 0), self.rect.center, (self.end_pos_for_tic_x, self.end_pos_for_tic_y))
