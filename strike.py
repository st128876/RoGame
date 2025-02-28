import math
import pygame


class SwordPush(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, target_x, target_y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()

        # Рассчитываем угол между игроком и целью
        dx = target_x - start_x
        dy = target_y - start_y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        self.dx = dx / distance * 15
        self.dy = dy / distance * 15

        self.rect.center = (self.dx, self.dy)

        # Нормализуем вектор (направление пули)

    def update(self, x_to_right, x_to_left, y_to_up, y_to_down):
        self.rect.x -= x_to_right
        self.rect.x += x_to_left

        self.rect.y += y_to_up
        self.rect.y -= y_to_down

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Bullet(pygame.sprite.Sprite):

    def __init__(self, start_x, start_y, target_x, target_y, bullet_of_player_speed):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (start_x, start_y)

        # Рассчитываем угол между игроком и целью
        dx = target_x - start_x
        dy = target_y - start_y
        distance = math.sqrt(dx**2 + dy**2)

        # Нормализуем вектор (направление пули)
        self.dx = dx / distance * bullet_of_player_speed
        self.dy = dy / distance * bullet_of_player_speed

    def update(self):
        # Обновляем положение пули
        self.rect.x += self.dx
        self.rect.y += self.dy

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def give_coordinatoin(self):
        return (self.rect.x, self.rect.y)
